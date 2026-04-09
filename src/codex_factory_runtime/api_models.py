from __future__ import annotations

from pydantic import BaseModel, Field


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
