from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .config import RuntimeSettings
from .state_payloads import (
    build_conversation,
    build_conversation_event,
    build_conversation_message,
    build_goal,
    build_job,
    build_request,
)

logger = logging.getLogger(__name__)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class RuntimeState:
    def __init__(self, settings: RuntimeSettings) -> None:
        self.settings = settings
        self.ensure_layout()

    def ensure_layout(self) -> None:
        paths = [
            self.settings.registry_root,
            self.settings.requests_root,
            self.settings.runtime_root,
            self.settings.jobs_root,
            self.settings.proposals_root,
            self.settings.worktrees_root,
            self.settings.conversations_root,
            self.settings.goals_root,
        ]
        if self.settings.codex_home is not None:
            paths.append(self.settings.codex_home)
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)

    def _read_json(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def list_apps(self) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for path in sorted(self.settings.registry_root.glob("*.json")):
            try:
                records.append(self._read_json(path))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                logger.warning("Skipping unreadable app registry file %s: %s", path, exc)
        return records

    def get_app(self, app_id: str) -> dict[str, Any]:
        path = self.settings.registry_root / f"{app_id}.json"
        if not path.exists():
            raise KeyError(f"Unknown app_id: {app_id}")
        return self._read_json(path)

    def save_app(self, record: dict[str, Any]) -> dict[str, Any]:
        record["updated_at"] = utc_now()
        self._write_json(self.settings.registry_root / f"{record['app_id']}.json", record)
        return record

    def ensure_session_id(self, app_id: str) -> str:
        record = self.get_app(app_id)
        session_id = str(record.get("session_id", "")).strip()
        if session_id:
            return session_id
        session_id = f"codex-session-{app_id}"
        record["session_id"] = session_id
        self.save_app(record)
        return session_id

    def append_memory(self, app_id: str, heading: str, body: str) -> None:
        memory_path = self.settings.state_root / "memory" / f"{app_id}.md"
        existing = memory_path.read_text(encoding="utf-8") if memory_path.exists() else f"# {app_id} Memory\n"
        updated = existing.rstrip() + f"\n\n## {heading}\n\n{body.strip()}\n"
        memory_path.parent.mkdir(parents=True, exist_ok=True)
        memory_path.write_text(updated, encoding="utf-8")

    def append_engineering_log(
        self,
        *,
        app_id: str,
        title: str,
        job_id: str,
        request_id: str,
        summary: dict[str, Any],
    ) -> None:
        log_path = self.settings.state_root / "engineering-log.md"
        existing = (
            log_path.read_text(encoding="utf-8")
            if log_path.exists()
            else "# Engineering Log\n\nThis file is appended automatically after runtime jobs and proposal applies.\n"
        )
        sections = [
            f"## {utc_now()} · {app_id} · {title}",
            f"- job_id: `{job_id}`",
            f"- request_id: `{request_id}`",
            f"- goal: {summary.get('goal', '').strip() or '(not provided)'}",
            f"- system_area: {summary.get('system_area', '').strip() or '(not provided)'}",
            f"- decision: {summary.get('decision', '').strip() or '(not provided)'}",
            f"- why: {summary.get('why', '').strip() or '(not provided)'}",
            f"- tradeoff: {summary.get('tradeoff', '').strip() or '(not provided)'}",
            f"- issue_encountered: {summary.get('issue_encountered', '').strip() or '(none)'}",
            f"- verification: {summary.get('verification', '').strip() or '(not provided)'}",
            f"- follow_up: {summary.get('follow_up', '').strip() or '(none)'}",
        ]
        updated = existing.rstrip() + "\n\n" + "\n".join(sections) + "\n"
        log_path.write_text(updated, encoding="utf-8")

    def conversation_path(self, conversation_id: str) -> Path:
        return self.settings.conversations_root / f"{conversation_id}.json"

    def create_conversation(self, *, app_id: str, title: str, source: str) -> dict[str, Any]:
        payload = build_conversation(app_id=app_id, title=title, source=source, now=utc_now())
        self._write_json(self.conversation_path(payload["conversation_id"]), payload)
        return payload

    def get_conversation(self, conversation_id: str) -> dict[str, Any]:
        path = self.conversation_path(conversation_id)
        if not path.exists():
            raise KeyError(f"Unknown conversation_id: {conversation_id}")
        return self._read_json(path)

    def save_conversation(self, conversation: dict[str, Any]) -> dict[str, Any]:
        conversation["updated_at"] = utc_now()
        self._write_json(self.conversation_path(conversation["conversation_id"]), conversation)
        return conversation

    def list_conversations(self, *, app_id: str | None = None) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for path in sorted(self.settings.conversations_root.glob("*.json")):
            try:
                payload = self._read_json(path)
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                logger.warning("Skipping unreadable conversation file %s: %s", path, exc)
                continue
            if app_id and payload.get("app_id") != app_id:
                continue
            records.append(payload)
        records.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return records

    def append_conversation_message(
        self,
        conversation_id: str,
        *,
        role: str,
        body: str,
        title: str = "",
        job_id: str = "",
        message_type: str = "message",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        conversation = self.get_conversation(conversation_id)
        message = build_conversation_message(
            role=role,
            body=body,
            now=utc_now(),
            title=title,
            job_id=job_id,
            message_type=message_type,
            metadata=metadata,
        )
        conversation.setdefault("messages", []).append(message)
        if job_id:
            conversation["latest_job_id"] = job_id
        self.save_conversation(conversation)
        return message

    def append_conversation_event(
        self,
        conversation_id: str,
        *,
        event_type: str,
        body: str,
        status: str = "info",
        job_id: str = "",
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        conversation = self.get_conversation(conversation_id)
        event = build_conversation_event(
            event_type=event_type,
            body=body,
            now=utc_now(),
            status=status,
            job_id=job_id,
            data=data,
        )
        conversation.setdefault("events", []).append(event)
        if job_id:
            conversation["latest_job_id"] = job_id
        self.save_conversation(conversation)
        return event

    def create_request(
        self,
        *,
        app_id: str,
        title: str,
        request_text: str,
        source: str,
        status: str = "pending",
        conversation_id: str = "",
        intent_summary: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        request_id = utc_now().replace(":", "-")
        payload = build_request(
            request_id=request_id,
            app_id=app_id,
            title=title,
            request_text=request_text,
            source=source,
            now=utc_now(),
            status=status,
            conversation_id=conversation_id,
            intent_summary=intent_summary,
        )
        requests_dir = self.settings.requests_root / app_id
        self._write_json(requests_dir / f"{request_id}.json", payload)
        self.append_memory(
            app_id,
            f"Runtime Request {request_id}",
            f"source: {source}\nstatus: {status}\n\n{request_text}",
        )
        return payload

    def create_job(
        self,
        *,
        app_id: str,
        request_id: str,
        title: str,
        conversation_id: str = "",
        intent_summary: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        job_id = uuid4().hex
        payload = build_job(
            job_id=job_id,
            app_id=app_id,
            request_id=request_id,
            title=title,
            now=utc_now(),
            conversation_id=conversation_id,
            intent_summary=intent_summary,
        )
        self._write_json(self.settings.jobs_root / f"{job_id}.json", payload)
        return payload

    def get_job(self, job_id: str) -> dict[str, Any]:
        path = self.settings.jobs_root / f"{job_id}.json"
        if not path.exists():
            raise KeyError(f"Unknown job_id: {job_id}")
        return self._read_json(path)

    def update_job(self, job_id: str, **fields: Any) -> dict[str, Any]:
        payload = self.get_job(job_id)
        payload.update(fields)
        payload["updated_at"] = utc_now()
        self._write_json(self.settings.jobs_root / f"{job_id}.json", payload)
        return payload

    def proposal_path(self, job_id: str) -> Path:
        return self.settings.proposals_root / f"{job_id}.json"

    def save_proposal(self, proposal: dict[str, Any]) -> dict[str, Any]:
        proposal["updated_at"] = utc_now()
        self._write_json(self.proposal_path(proposal["job_id"]), proposal)
        return proposal

    def get_proposal(self, job_id: str) -> dict[str, Any]:
        path = self.proposal_path(job_id)
        if not path.exists():
            raise KeyError(f"Unknown proposal job_id: {job_id}")
        return self._read_json(path)

    def goal_path(self, goal_id: str) -> Path:
        return self.settings.goals_root / f"{goal_id}.json"

    def create_goal(
        self,
        *,
        app_id: str,
        title: str,
        objective: str,
        source: str,
        conversation_id: str,
        max_iterations: int,
    ) -> dict[str, Any]:
        payload = build_goal(
            app_id=app_id,
            title=title,
            objective=objective,
            source=source,
            conversation_id=conversation_id,
            now=utc_now(),
            max_iterations=max_iterations,
        )
        self._write_json(self.goal_path(payload["goal_id"]), payload)
        return payload

    def save_goal(self, goal: dict[str, Any]) -> dict[str, Any]:
        goal["updated_at"] = utc_now()
        self._write_json(self.goal_path(goal["goal_id"]), goal)
        return goal

    def get_goal(self, goal_id: str) -> dict[str, Any]:
        path = self.goal_path(goal_id)
        if not path.exists():
            raise KeyError(f"Unknown goal_id: {goal_id}")
        return self._read_json(path)

    def list_goals(self, *, app_id: str | None = None) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for path in sorted(self.settings.goals_root.glob("*.json")):
            try:
                payload = self._read_json(path)
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                logger.warning("Skipping unreadable goal file %s: %s", path, exc)
                continue
            if app_id and payload.get("app_id") != app_id:
                continue
            records.append(payload)
        records.sort(key=lambda item: item.get("updated_at", ""), reverse=True)
        return records
