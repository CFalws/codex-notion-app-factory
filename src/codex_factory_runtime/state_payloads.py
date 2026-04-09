from __future__ import annotations

from typing import Any
from uuid import uuid4


def build_conversation(*, app_id: str, title: str, source: str, now: str) -> dict[str, Any]:
    conversation_id = uuid4().hex
    return {
        "conversation_id": conversation_id,
        "app_id": app_id,
        "title": title.strip() or app_id,
        "source": source,
        "status": "active",
        "created_at": now,
        "updated_at": now,
        "latest_job_id": "",
        "messages": [],
        "events": [],
    }


def build_conversation_message(
    *,
    role: str,
    body: str,
    now: str,
    title: str = "",
    job_id: str = "",
    message_type: str = "message",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "message_id": uuid4().hex,
        "role": role,
        "type": message_type,
        "title": title,
        "body": body,
        "job_id": job_id,
        "created_at": now,
        "metadata": metadata or {},
    }


def build_conversation_event(
    *,
    event_type: str,
    body: str,
    now: str,
    status: str = "info",
    job_id: str = "",
    data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "event_id": uuid4().hex,
        "type": event_type,
        "status": status,
        "body": body,
        "job_id": job_id,
        "created_at": now,
        "data": data or {},
    }


def build_request(
    *,
    request_id: str,
    app_id: str,
    title: str,
    request_text: str,
    source: str,
    now: str,
    status: str = "pending",
    conversation_id: str = "",
    intent_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "request_id": request_id,
        "app_id": app_id,
        "conversation_id": conversation_id,
        "status": status,
        "title": title,
        "request_text": request_text,
        "source": source,
        "intent_summary": intent_summary or {},
        "created_at": now,
        "updated_at": now,
    }


def build_job(
    *,
    job_id: str,
    app_id: str,
    request_id: str,
    title: str,
    now: str,
    conversation_id: str = "",
    intent_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "job_id": job_id,
        "app_id": app_id,
        "request_id": request_id,
        "conversation_id": conversation_id,
        "title": title,
        "intent_summary": intent_summary or {},
        "status": "queued",
        "created_at": now,
        "updated_at": now,
        "started_at": "",
        "completed_at": "",
        "runner_pid": 0,
        "runner_started_at": "",
        "error": "",
        "result_summary": "",
        "decision_summary": {},
        "goal_review": {},
    }


def build_goal(
    *,
    app_id: str,
    title: str,
    objective: str,
    source: str,
    conversation_id: str,
    now: str,
    max_iterations: int,
    auto_apply_proposals: bool,
    auto_resume_after_apply: bool,
) -> dict[str, Any]:
    return {
        "goal_id": uuid4().hex,
        "app_id": app_id,
        "conversation_id": conversation_id,
        "title": title.strip() or app_id,
        "objective": objective,
        "source": source,
        "status": "queued",
        "created_at": now,
        "updated_at": now,
        "started_at": "",
        "completed_at": "",
        "max_iterations": max_iterations,
        "current_iteration": 0,
        "last_job_id": "",
        "best_job_id": "",
        "best_summary": "",
        "stop_reason": "",
        "halt_requested": False,
        "awaiting_restart_resume": False,
        "awaiting_restart_iteration": 0,
        "awaiting_restart_job_id": "",
        "last_resume_reason": "",
        "last_resumed_at": "",
        "policy": {
            "require_verification": True,
            "auto_apply_proposals": auto_apply_proposals,
            "auto_resume_after_apply": auto_resume_after_apply,
            "pause_on_proposal": not auto_apply_proposals,
            "pause_on_failed_job": True,
            "pause_on_safety_no": True,
            "pause_on_alignment_no": True,
            "continue_on_review_failure": True,
            "continue_on_verification_failure": True,
            "open_ended": max_iterations == 0,
        },
        "iterations": [],
    }
