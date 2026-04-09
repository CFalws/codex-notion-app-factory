from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import BackgroundTasks, HTTPException

from .agent_runtime import CodexAgentsRuntime
from .config import RuntimeSettings
from .state import RuntimeState, utc_now


@dataclass(slots=True)
class RuntimeApiContext:
    settings: RuntimeSettings
    state: RuntimeState
    runtime: CodexAgentsRuntime

    def append_event(
        self,
        conversation_id: str,
        *,
        event_type: str,
        body: str,
        status: str = "info",
        job_id: str = "",
        data: dict[str, Any] | None = None,
    ) -> None:
        if not conversation_id:
            return
        self.state.append_conversation_event(
            conversation_id,
            event_type=event_type,
            body=body,
            status=status,
            job_id=job_id,
            data=data,
        )

    def append_assistant_message(
        self,
        conversation_id: str,
        *,
        title: str,
        body: str,
        job_id: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        if not conversation_id:
            return
        self.state.append_conversation_message(
            conversation_id,
            role="assistant",
            title=title,
            body=body,
            job_id=job_id,
            message_type="result",
            metadata=metadata,
        )

    def resolve_conversation_title(self, app_id: str, explicit_title: str) -> str:
        if explicit_title.strip():
            return explicit_title.strip()
        app_record = self.state.get_app(app_id)
        return f"{app_record.get('title') or app_id} Conversation"

    def resolve_request_title(self, explicit_title: str, request_text: str) -> str:
        if explicit_title.strip():
            return explicit_title.strip()
        first_line = next((line.strip() for line in request_text.splitlines() if line.strip()), "")
        compact = " ".join(first_line.split())
        if len(compact) > 72:
            compact = compact[:69].rstrip() + "..."
        return compact or "Conversation update"

    def require_app(self, app_id: str) -> dict[str, Any]:
        try:
            return self.state.get_app(app_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def require_conversation(self, conversation_id: str) -> dict[str, Any]:
        try:
            return self.state.get_conversation(conversation_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def get_job_or_404(self, job_id: str) -> dict[str, Any]:
        try:
            return self.state.get_job(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def get_proposal_or_404(self, job_id: str) -> dict[str, Any]:
        try:
            return self.state.get_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc

    def build_health_payload(self) -> dict[str, Any]:
        return {
            "ok": True,
            "repo_root": str(self.settings.repo_root),
            "codex_command": self.settings.codex_command,
            "codex_home": str(self.settings.codex_home) if self.settings.codex_home is not None else "(default ~/.codex)",
            "codex_profile": self.settings.codex_profile,
            "codex_model": self.settings.codex_model or "(default)",
            "auth_providers": self.settings.auth_providers,
            "api_key_required": "api_key" in self.settings.auth_providers,
            "iap_enabled": "iap" in self.settings.auth_providers,
            "allowed_user_emails": self.settings.allowed_user_emails,
        }

    def enqueue_request(
        self,
        *,
        app_id: str,
        title: str,
        request_text: str,
        source: str,
        execute_now: bool,
        background_tasks: BackgroundTasks,
        conversation_id: str = "",
    ) -> dict[str, Any]:
        resolved_title = self.resolve_request_title(title, request_text)
        request_payload = self.state.create_request(
            app_id=app_id,
            title=resolved_title,
            request_text=request_text,
            source=source,
            conversation_id=conversation_id,
        )
        job = self.state.create_job(
            app_id=app_id,
            request_id=request_payload["request_id"],
            title=resolved_title,
            conversation_id=conversation_id,
        )
        self.append_event(
            conversation_id,
            event_type="job.queued",
            status="queued",
            body=f"요청이 접수되어 job {job['job_id']}를 만들었습니다.",
            job_id=job["job_id"],
            data={"title": resolved_title, "request_id": request_payload["request_id"]},
        )
        if execute_now and self.settings.auto_execute_requests:
            background_tasks.add_task(self.run_job, job["job_id"], app_id, request_payload)
        return {
            "request": request_payload,
            "job": job,
            "execute_now": bool(execute_now and self.settings.auto_execute_requests),
        }

    async def run_job(self, job_id: str, app_id: str, request_payload: dict[str, Any]) -> None:
        conversation_id = str(request_payload.get("conversation_id") or "").strip()
        self.append_event(
            conversation_id,
            event_type="job.running",
            status="running",
            body=f"job {job_id}가 실행을 시작했습니다.",
            job_id=job_id,
            data={"title": request_payload.get("title", "")},
        )
        try:
            await self.runtime.run_request(
                app_id,
                job_id,
                request_payload,
                event_callback=lambda **event: self.append_event(conversation_id, **event),
            )
        except Exception as exc:  # noqa: BLE001
            self.state.update_job(
                job_id,
                status="failed",
                completed_at=utc_now(),
                error=str(exc),
            )

        job = self.state.get_job(job_id)
        if job["status"] == "completed":
            self.append_event(
                conversation_id,
                event_type="job.completed",
                status="completed",
                body=f"job {job_id}가 완료되었습니다.",
                job_id=job_id,
                data={"summary": job.get("result_summary", "")},
            )
            self.append_assistant_message(
                conversation_id,
                title=job.get("title") or "작업 결과",
                body=job.get("result_summary") or "작업이 완료되었습니다.",
                job_id=job_id,
                metadata={"decision_summary": job.get("decision_summary") or {}, "status": job.get("status")},
            )
            if job.get("proposal"):
                self.append_event(
                    conversation_id,
                    event_type="proposal.ready",
                    status="proposal",
                    body=f"proposal branch {job['proposal']['branch_name']}가 준비되었습니다.",
                    job_id=job_id,
                    data=job["proposal"],
                )
            return

        self.append_event(
            conversation_id,
            event_type="job.failed",
            status="failed",
            body=f"job {job_id}가 실패했습니다. {job.get('error', '')}".strip(),
            job_id=job_id,
            data={"error": job.get("error", "")},
        )
        self.append_assistant_message(
            conversation_id,
            title=job.get("title") or "작업 실패",
            body=job.get("error") or "작업이 실패했습니다.",
            job_id=job_id,
            metadata={"decision_summary": job.get("decision_summary") or {}, "status": job.get("status")},
        )

    async def apply_proposal(self, job_id: str) -> dict[str, Any]:
        try:
            proposal = await self.runtime.apply_proposal(job_id)
        except KeyError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc

        job = self.state.get_job(job_id)
        conversation_id = str(job.get("conversation_id") or "").strip()
        self.append_event(
            conversation_id,
            event_type="proposal.applied",
            status="applied",
            body=f"proposal {job_id}가 적용되었습니다.",
            job_id=job_id,
            data={"branch_name": proposal.get("branch_name", ""), "head_commit": proposal.get("head_commit", "")},
        )
        self.append_assistant_message(
            conversation_id,
            title=f"Proposal applied · {proposal.get('title') or job_id}",
            body=proposal.get("push_message") or proposal.get("result_summary") or "proposal이 적용되었습니다.",
            job_id=job_id,
            metadata={"decision_summary": proposal.get("decision_summary") or {}, "status": proposal.get("status")},
        )
        return proposal
