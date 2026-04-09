from __future__ import annotations

from pydantic import BaseModel, Field


class AttachmentRefBody(BaseModel):
    attachment_id: str = Field(..., description="Previously uploaded conversation attachment id.")
    filename: str = Field(default="", description="Original filename for UI continuity.")
    content_type: str = Field(default="", description="Attachment content type.")
    size_bytes: int = Field(default=0, ge=0, description="Attachment size in bytes.")
    api_path: str = Field(default="", description="Runtime API path for retrieving the attachment.")


class UXContextBody(BaseModel):
    affected_surface: str = Field(default="", description="What part of the UI feels uncomfortable.")
    pain_points: list[str] = Field(default_factory=list, description="Structured UX pain-point tags.")
    note: str = Field(default="", description="Free-form description of the friction.")
    desired_feel: str = Field(default="", description="How the user wants the UI to feel instead.")


class CreateRequestBody(BaseModel):
    app_id: str = Field(..., description="Registered app id to continue.")
    title: str = Field(default="", description="Optional short label for compatibility with older clients.")
    request_text: str = Field(..., description="Full natural-language change request.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")
    execute_now: bool = Field(default=True, description="Whether to start the agent run immediately.")
    conversation_id: str = Field(default="", description="Existing conversation id for continuity.")
    ux_context: UXContextBody | None = Field(default=None, description="Optional structured UX discomfort signal.")
    attachments: list[AttachmentRefBody] = Field(default_factory=list, description="Previously uploaded screenshot refs.")


class CreateConversationBody(BaseModel):
    app_id: str = Field(..., description="Registered app id to continue.")
    title: str = Field(default="", description="Optional conversation title.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")


class ConversationMessageBody(BaseModel):
    title: str = Field(default="", description="Optional short label for compatibility with older clients.")
    message_text: str = Field(..., description="Full natural-language message for the conversation.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")
    execute_now: bool = Field(default=True, description="Whether to start the agent run immediately.")
    ux_context: UXContextBody | None = Field(default=None, description="Optional structured UX discomfort signal.")
    attachments: list[AttachmentRefBody] = Field(default_factory=list, description="Previously uploaded screenshot refs.")


class CreateGoalBody(BaseModel):
    app_id: str = Field(..., description="Registered app id to improve.")
    objective: str = Field(..., description="Higher-level user objective the agent should keep improving toward.")
    title: str = Field(default="", description="Optional goal label.")
    source: str = Field(default="ops-console", description="Origin label for traceability.")
    max_iterations: int = Field(default=0, ge=0, le=1000, description="0 means open-ended autonomy until a policy stop condition is hit.")
    autostart: bool = Field(default=True, description="Whether to start the autonomous goal loop immediately.")
    auto_apply_proposals: bool = Field(
        default=True,
        description="Whether proposal-mode iterations should auto-apply instead of pausing for manual approval.",
    )
    auto_resume_after_apply: bool = Field(
        default=True,
        description="Whether a running goal should resume automatically after an auto-applied proposal and service restart.",
    )
