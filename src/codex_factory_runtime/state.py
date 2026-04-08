from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from .config import RuntimeSettings

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

    def create_request(
        self,
        *,
        app_id: str,
        title: str,
        request_text: str,
        source: str,
        status: str = "pending",
    ) -> dict[str, Any]:
        request_id = utc_now().replace(":", "-")
        payload = {
            "request_id": request_id,
            "app_id": app_id,
            "status": status,
            "title": title,
            "request_text": request_text,
            "source": source,
            "created_at": utc_now(),
            "updated_at": utc_now(),
        }
        requests_dir = self.settings.requests_root / app_id
        self._write_json(requests_dir / f"{request_id}.json", payload)
        self.append_memory(
            app_id,
            f"Runtime Request {request_id}",
            f"source: {source}\nstatus: {status}\n\n{request_text}",
        )
        return payload

    def create_job(self, *, app_id: str, request_id: str, title: str) -> dict[str, Any]:
        job_id = uuid4().hex
        payload = {
            "job_id": job_id,
            "app_id": app_id,
            "request_id": request_id,
            "title": title,
            "status": "queued",
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "started_at": "",
            "completed_at": "",
            "error": "",
            "result_summary": "",
        }
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
