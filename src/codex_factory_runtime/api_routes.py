from __future__ import annotations

from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException

from .api_models import ConversationMessageBody, CreateConversationBody, CreateRequestBody
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

    @app.post("/api/conversations/{conversation_id}/messages")
    async def create_conversation_message(
        conversation_id: str,
        body: ConversationMessageBody,
        background_tasks: BackgroundTasks,
    ) -> dict[str, Any]:
        conversation = context.require_conversation(conversation_id)
        context.state.append_conversation_message(
            conversation_id,
            role="user",
            title=context.resolve_request_title(body.title, body.message_text),
            body=body.message_text,
            message_type="request",
            metadata={"source": body.source},
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
