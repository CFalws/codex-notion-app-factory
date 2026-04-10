from __future__ import annotations

from typing import Any

import asyncio
import json

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse

from .api_models import ConversationMessageBody, CreateConversationBody, CreateGoalBody, CreateRequestBody
from .api_runtime_context import RuntimeApiContext


def register_routes(app: FastAPI, context: RuntimeApiContext) -> None:
    @app.get("/health")
    async def health() -> dict[str, Any]:
        return context.build_health_payload()

    @app.get("/api/apps")
    async def list_apps() -> list[dict[str, Any]]:
        return context.state.list_apps()

    @app.get("/api/apps/{app_id}")
    async def get_app(app_id: str) -> dict[str, Any]:
        context.require_app(app_id)
        return context.state.get_app(app_id)

    @app.get("/api/apps/{app_id}/conversations")
    async def list_app_conversations(app_id: str) -> list[dict[str, Any]]:
        context.require_app(app_id)
        return context.state.list_conversations(app_id=app_id)

    @app.get("/api/apps/{app_id}/goals")
    async def list_app_goals(app_id: str) -> list[dict[str, Any]]:
        context.require_app(app_id)
        return context.state.list_goals(app_id=app_id)

    @app.post("/api/conversations")
    async def create_conversation(body: CreateConversationBody) -> dict[str, Any]:
        context.require_app(body.app_id)
        conversation = context.state.create_conversation(
            app_id=body.app_id,
            title=context.resolve_conversation_title(body.app_id, body.title),
            source=body.source,
        )
        context.append_event(
            conversation["conversation_id"],
            event_type="conversation.created",
            body="대화 세션이 시작되었습니다.",
            status="created",
            data={"app_id": body.app_id},
        )
        return conversation

    @app.get("/api/conversations/{conversation_id}")
    async def get_conversation(conversation_id: str) -> dict[str, Any]:
        return context.require_conversation(conversation_id)

    @app.get("/api/internal/conversations/{conversation_id}/append-stream")
    async def conversation_append_stream(conversation_id: str, request: Request) -> StreamingResponse:
        context.require_conversation(conversation_id)
        last_event_id = request.headers.get("last-event-id", "").strip()
        try:
            after_append_id = int(last_event_id or "0")
        except ValueError:
            after_append_id = 0

        async def stream() -> Any:
            queue = context.subscribe_conversation_appends(conversation_id)
            try:
                for envelope in context.conversation_append_snapshot(conversation_id, after_append_id=after_append_id):
                    append_id = int(envelope["append_id"])
                    yield f"id: {append_id}\n".encode()
                    yield b"event: conversation.append\n"
                    yield f"data: {json.dumps(envelope, ensure_ascii=False)}\n\n".encode()

                while True:
                    if await request.is_disconnected():
                        break
                    try:
                        envelope = await asyncio.wait_for(queue.get(), timeout=15)
                    except asyncio.TimeoutError:
                        yield b": keepalive\n\n"
                        continue
                    append_id = int(envelope["append_id"])
                    yield f"id: {append_id}\n".encode()
                    yield b"event: conversation.append\n"
                    yield f"data: {json.dumps(envelope, ensure_ascii=False)}\n\n".encode()
            finally:
                context.unsubscribe_conversation_appends(conversation_id, queue)

        return StreamingResponse(
            stream(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
        )

    @app.post("/api/goals")
    async def create_goal(body: CreateGoalBody) -> dict[str, Any]:
        context.require_app(body.app_id)
        return context.create_goal(
            app_id=body.app_id,
            title=body.title,
            objective=body.objective,
            source=body.source,
            max_iterations=body.max_iterations,
            autostart=body.autostart,
            auto_apply_proposals=body.auto_apply_proposals,
            auto_resume_after_apply=body.auto_resume_after_apply,
        )

    @app.get("/api/goals/{goal_id}")
    async def get_goal(goal_id: str) -> dict[str, Any]:
        return context.get_goal_or_404(goal_id)

    @app.post("/api/goals/{goal_id}/start")
    async def start_goal(goal_id: str) -> dict[str, Any]:
        return context.start_goal(goal_id)

    @app.post("/api/goals/{goal_id}/halt")
    async def halt_goal(goal_id: str) -> dict[str, Any]:
        return context.halt_goal(goal_id)

    @app.post("/api/conversations/{conversation_id}/messages")
    async def create_conversation_message(
        conversation_id: str,
        body: ConversationMessageBody,
        background_tasks: BackgroundTasks,
    ) -> dict[str, Any]:
        conversation = context.require_conversation(conversation_id)
        intent_summary = context.interpret_intent(
            app_id=str(conversation["app_id"]),
            title=context.resolve_request_title(body.title, body.message_text),
            request_text=body.message_text,
            source=body.source,
            conversation_id=conversation_id,
        )
        context.append_user_message(
            conversation_id,
            title=context.resolve_request_title(body.title, body.message_text),
            body=body.message_text,
            metadata={
                "source": body.source,
                "intent_summary": intent_summary,
            },
        )
        context.append_event(
            conversation_id,
            event_type="message.accepted",
            body="새 사용자 메시지를 작업 요청으로 등록합니다.",
            status="accepted",
        )
        payload = context.enqueue_request(
            app_id=str(conversation["app_id"]),
            title=body.title,
            request_text=body.message_text,
            source=body.source,
            execute_now=body.execute_now,
            background_tasks=background_tasks,
            conversation_id=conversation_id,
            intent_summary=intent_summary,
        )
        return {
            "conversation": context.state.get_conversation(conversation_id),
            **payload,
        }

    @app.get("/api/jobs/{job_id}")
    async def get_job(job_id: str) -> dict[str, Any]:
        return context.get_job_or_404(job_id)

    @app.get("/api/proposals/{job_id}")
    async def get_proposal(job_id: str) -> dict[str, Any]:
        return context.get_proposal_or_404(job_id)

    @app.post("/api/proposals/{job_id}/apply")
    async def apply_proposal(job_id: str) -> dict[str, Any]:
        return await context.apply_proposal(job_id)

    @app.post("/api/requests")
    async def create_request(body: CreateRequestBody, background_tasks: BackgroundTasks) -> dict[str, Any]:
        context.require_app(body.app_id)
        conversation_id = body.conversation_id.strip()
        if conversation_id:
            conversation = context.require_conversation(conversation_id)
            if conversation.get("app_id") != body.app_id:
                raise HTTPException(status_code=409, detail="Conversation app_id does not match request app_id.")
        return context.enqueue_request(
            app_id=body.app_id,
            title=body.title,
            request_text=body.request_text,
            source=body.source,
            execute_now=body.execute_now,
            background_tasks=background_tasks,
            conversation_id=conversation_id,
        )
