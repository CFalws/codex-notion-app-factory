from __future__ import annotations

import secrets
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .agent_runtime import CodexAgentsRuntime
from .config import RuntimeSettings, load_settings
from .state import RuntimeState, utc_now


class CreateRequestBody(BaseModel):
    app_id: str = Field(..., description="Registered app id to continue.")
    title: str = Field(default="", description="Optional short label for compatibility with older clients.")
    request_text: str = Field(..., description="Full natural-language change request.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")
    execute_now: bool = Field(default=True, description="Whether to start the agent run immediately.")
    conversation_id: str = Field(default="", description="Existing conversation id for continuity.")


class CreateConversationBody(BaseModel):
    app_id: str = Field(..., description="Registered app id to continue.")
    title: str = Field(default="", description="Optional conversation title.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")


class ConversationMessageBody(BaseModel):
    title: str = Field(default="", description="Optional short label for compatibility with older clients.")
    message_text: str = Field(..., description="Full natural-language message for the conversation.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")
    execute_now: bool = Field(default=True, description="Whether to start the agent run immediately.")


def _requires_api_key(request: Request, settings: RuntimeSettings) -> bool:
    return (
        request.method != "OPTIONS"
        and request.url.path.startswith("/api/")
        and bool(settings.runtime_api_key)
    )


def create_app(settings: RuntimeSettings | None = None) -> FastAPI:
    settings = settings or load_settings()
    state = RuntimeState(settings)
    runtime = CodexAgentsRuntime(settings, state)

    app = FastAPI(
        title="Codex App Factory Runtime",
        version="0.2.0",
        summary="Conversation-aware Codex CLI runtime for personal app maintenance.",
    )

    if settings.cors_allowed_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_allowed_origins,
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        app.add_middleware(
            CORSMiddleware,
            allow_origin_regex=".*",
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    @app.middleware("http")
    async def require_api_key(request: Request, call_next):  # type: ignore[no-untyped-def]
        if not _requires_api_key(request, settings):
            return await call_next(request)

        api_key = request.headers.get("x-api-key", "")
        if not secrets.compare_digest(api_key, settings.runtime_api_key):
            return JSONResponse(status_code=401, content={"detail": "Invalid or missing X-API-Key header."})
        return await call_next(request)

    def append_event(conversation_id: str, *, event_type: str, body: str, status: str = "info", job_id: str = "", data: dict[str, Any] | None = None) -> None:
        if not conversation_id:
            return
        state.append_conversation_event(
            conversation_id,
            event_type=event_type,
            body=body,
            status=status,
            job_id=job_id,
            data=data,
        )

    def append_assistant_message(conversation_id: str, *, title: str, body: str, job_id: str, metadata: dict[str, Any] | None = None) -> None:
        if not conversation_id:
            return
        state.append_conversation_message(
            conversation_id,
            role="assistant",
            title=title,
            body=body,
            job_id=job_id,
            message_type="result",
            metadata=metadata,
        )

    def _resolve_conversation_title(app_id: str, explicit_title: str) -> str:
        if explicit_title.strip():
            return explicit_title.strip()
        app_record = state.get_app(app_id)
        return f"{app_record.get('title') or app_id} Conversation"

    def _resolve_request_title(explicit_title: str, request_text: str) -> str:
        if explicit_title.strip():
            return explicit_title.strip()
        first_line = next((line.strip() for line in request_text.splitlines() if line.strip()), "")
        compact = " ".join(first_line.split())
        if len(compact) > 72:
            compact = compact[:69].rstrip() + "..."
        return compact or "Conversation update"

    def enqueue_request(
        *,
        app_id: str,
        title: str,
        request_text: str,
        source: str,
        execute_now: bool,
        background_tasks: BackgroundTasks,
        conversation_id: str = "",
    ) -> dict[str, Any]:
        resolved_title = _resolve_request_title(title, request_text)
        request_payload = state.create_request(
            app_id=app_id,
            title=resolved_title,
            request_text=request_text,
            source=source,
            conversation_id=conversation_id,
        )
        job = state.create_job(
            app_id=app_id,
            request_id=request_payload["request_id"],
            title=resolved_title,
            conversation_id=conversation_id,
        )
        append_event(
            conversation_id,
            event_type="job.queued",
            status="queued",
            body=f"요청이 접수되어 job {job['job_id']}를 만들었습니다.",
            job_id=job["job_id"],
            data={"title": resolved_title, "request_id": request_payload["request_id"]},
        )
        if execute_now and settings.auto_execute_requests:
            background_tasks.add_task(run_job, job["job_id"], app_id, request_payload)
        return {
            "request": request_payload,
            "job": job,
            "execute_now": bool(execute_now and settings.auto_execute_requests),
        }

    async def run_job(job_id: str, app_id: str, request_payload: dict[str, Any]) -> None:
        conversation_id = str(request_payload.get("conversation_id") or "").strip()
        append_event(
            conversation_id,
            event_type="job.running",
            status="running",
            body=f"job {job_id}가 실행을 시작했습니다.",
            job_id=job_id,
            data={"title": request_payload.get("title", "")},
        )
        try:
            await runtime.run_request(app_id, job_id, request_payload)
        except Exception as exc:  # noqa: BLE001
            state.update_job(
                job_id,
                status="failed",
                completed_at=utc_now(),
                error=str(exc),
            )

        job = state.get_job(job_id)
        if job["status"] == "completed":
            append_event(
                conversation_id,
                event_type="job.completed",
                status="completed",
                body=f"job {job_id}가 완료되었습니다.",
                job_id=job_id,
                data={"summary": job.get("result_summary", "")},
            )
            append_assistant_message(
                conversation_id,
                title=job.get("title") or "작업 결과",
                body=job.get("result_summary") or "작업이 완료되었습니다.",
                job_id=job_id,
                metadata={"decision_summary": job.get("decision_summary") or {}, "status": job.get("status")},
            )
            if job.get("proposal"):
                append_event(
                    conversation_id,
                    event_type="proposal.ready",
                    status="proposal",
                    body=f"proposal branch {job['proposal']['branch_name']}가 준비되었습니다.",
                    job_id=job_id,
                    data=job["proposal"],
                )
        else:
            append_event(
                conversation_id,
                event_type="job.failed",
                status="failed",
                body=f"job {job_id}가 실패했습니다. {job.get('error', '')}".strip(),
                job_id=job_id,
                data={"error": job.get("error", "")},
            )
            append_assistant_message(
                conversation_id,
                title=job.get("title") or "작업 실패",
                body=job.get("error") or "작업이 실패했습니다.",
                job_id=job_id,
                metadata={"decision_summary": job.get("decision_summary") or {}, "status": job.get("status")},
            )

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "ok": True,
            "repo_root": str(settings.repo_root),
            "codex_command": settings.codex_command,
            "codex_home": str(settings.codex_home) if settings.codex_home is not None else "(default ~/.codex)",
            "codex_profile": settings.codex_profile,
            "codex_model": settings.codex_model or "(default)",
            "api_key_required": bool(settings.runtime_api_key),
        }

    @app.get("/api/apps")
    async def list_apps() -> list[dict[str, Any]]:
        return state.list_apps()

    @app.get("/api/apps/{app_id}")
    async def get_app(app_id: str) -> dict[str, Any]:
        try:
            return state.get_app(app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/apps/{app_id}/conversations")
    async def list_app_conversations(app_id: str) -> list[dict[str, Any]]:
        try:
            state.get_app(app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return state.list_conversations(app_id=app_id)

    @app.post("/api/conversations")
    async def create_conversation(body: CreateConversationBody) -> dict[str, Any]:
        try:
            state.get_app(body.app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        conversation = state.create_conversation(
            app_id=body.app_id,
            title=_resolve_conversation_title(body.app_id, body.title),
            source=body.source,
        )
        append_event(
            conversation["conversation_id"],
            event_type="conversation.created",
            body="대화 세션이 시작되었습니다.",
            status="created",
            data={"app_id": body.app_id},
        )
        return conversation

    @app.get("/api/conversations/{conversation_id}")
    async def get_conversation(conversation_id: str) -> dict[str, Any]:
        try:
            return state.get_conversation(conversation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/api/conversations/{conversation_id}/messages")
    async def create_conversation_message(
        conversation_id: str,
        body: ConversationMessageBody,
        background_tasks: BackgroundTasks,
    ) -> dict[str, Any]:
        try:
            conversation = state.get_conversation(conversation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        state.append_conversation_message(
            conversation_id,
            role="user",
            title=_resolve_request_title(body.title, body.message_text),
            body=body.message_text,
            message_type="request",
            metadata={"source": body.source},
        )
        append_event(
            conversation_id,
            event_type="message.accepted",
            body="새 사용자 메시지를 작업 요청으로 등록합니다.",
            status="accepted",
        )
        payload = enqueue_request(
            app_id=str(conversation["app_id"]),
            title=body.title,
            request_text=body.message_text,
            source=body.source,
            execute_now=body.execute_now,
            background_tasks=background_tasks,
            conversation_id=conversation_id,
        )
        return {
            "conversation": state.get_conversation(conversation_id),
            **payload,
        }

    @app.get("/api/jobs/{job_id}")
    async def get_job(job_id: str) -> dict[str, Any]:
        try:
            return state.get_job(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.get("/api/proposals/{job_id}")
    async def get_proposal(job_id: str) -> dict[str, Any]:
        try:
            return state.get_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    @app.post("/api/proposals/{job_id}/apply")
    async def apply_proposal(job_id: str) -> dict[str, Any]:
        try:
            proposal = await runtime.apply_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        job = state.get_job(job_id)
        conversation_id = str(job.get("conversation_id") or "").strip()
        append_event(
            conversation_id,
            event_type="proposal.applied",
            status="applied",
            body=f"proposal {job_id}가 적용되었습니다.",
            job_id=job_id,
            data={"branch_name": proposal.get("branch_name", ""), "head_commit": proposal.get("head_commit", "")},
        )
        append_assistant_message(
            conversation_id,
            title=f"Proposal applied · {proposal.get('title') or job_id}",
            body=proposal.get("push_message") or proposal.get("result_summary") or "proposal이 적용되었습니다.",
            job_id=job_id,
            metadata={"decision_summary": proposal.get("decision_summary") or {}, "status": proposal.get("status")},
        )
        return proposal

    @app.post("/api/requests")
    async def create_request(body: CreateRequestBody, background_tasks: BackgroundTasks) -> dict[str, Any]:
        try:
            state.get_app(body.app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

        conversation_id = body.conversation_id.strip()
        if conversation_id:
            try:
                conversation = state.get_conversation(conversation_id)
            except KeyError as exc:
                raise HTTPException(status_code=404, detail=str(exc)) from exc
            if conversation.get("app_id") != body.app_id:
                raise HTTPException(status_code=409, detail="Conversation app_id does not match request app_id.")

        return enqueue_request(
            app_id=body.app_id,
            title=body.title,
            request_text=body.request_text,
            source=body.source,
            execute_now=body.execute_now,
            background_tasks=background_tasks,
            conversation_id=conversation_id,
        )

    return app


app = create_app()
