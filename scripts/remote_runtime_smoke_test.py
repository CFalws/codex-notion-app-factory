#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib import request


def load_env_file(path: Path) -> None:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


def http_json(method: str, url: str, payload: dict[str, Any] | None = None, *, api_key: str = "") -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, method=method, data=data, headers=headers)
    with request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_job(base_url: str, job_id: str, api_key: str, timeout_seconds: float = 180.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        payload = http_json("GET", f"{base_url}/api/jobs/{job_id}", api_key=api_key)
        if payload.get("status") in {"completed", "failed"}:
            return payload
        time.sleep(2)
    raise RuntimeError(f"Timed out waiting for job {job_id}")


def resolve_scratch_file(base_url: str, app_id: str, api_key: str, configured_scratch_file: str) -> str:
    if configured_scratch_file:
        return configured_scratch_file
    app_record = http_json("GET", f"{base_url}/api/apps/{app_id}", api_key=api_key)
    source_path = str(app_record.get("source_path") or "").strip().rstrip("/")
    workspace_path = str(app_record.get("workspace_path") or "").strip().rstrip("/")
    if source_path:
        return f"{source_path}/runtime-api-verification/phone-ops-check.md"
    if workspace_path:
        return f"{workspace_path}/runtime-api-verification/phone-ops-check.md"
    return f"workspaces/{app_id}/runtime-api-verification/phone-ops-check.md"


def main() -> None:
    env_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/etc/codex-factory.env")
    load_env_file(env_file)

    api_key = os.environ.get("CODEX_FACTORY_API_KEY", "").strip()
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1")
    app_id = os.environ.get("APP_ID", "habit-tracker-pwa")
    configured_scratch_file = os.environ.get("SCRATCH_FILE", "").strip()

    health_req = request.Request(f"{base_url}/health", method="GET")
    with request.urlopen(health_req, timeout=30) as response:
        health = json.loads(response.read().decode("utf-8"))
    repo_root = Path(health["repo_root"])
    scratch_file = resolve_scratch_file(base_url, app_id, api_key, configured_scratch_file)

    ping = http_json(
        "POST",
        f"{base_url}/api/requests",
        {
            "app_id": app_id,
            "title": "Phone ops ping",
            "request_text": "Reply with exactly one line: PHONE_OPS_OK. Do not inspect files and do not make any changes.",
            "source": "remote-runtime-smoke-test",
            "execute_now": True,
        },
        api_key=api_key,
    )
    ping_job = wait_for_job(base_url, ping["job"]["job_id"], api_key)
    if ping_job.get("status") != "completed":
        raise RuntimeError(f"Ping job failed: {ping_job}")

    scratch_path = Path(scratch_file)
    if not scratch_path.is_absolute():
        scratch_path = repo_root / scratch_path
    scratch_path.parent.mkdir(parents=True, exist_ok=True)
    scratch_path.write_text("# Phone Ops Check\n\nmarker: unchanged\n", encoding="utf-8")

    edit = http_json(
        "POST",
        f"{base_url}/api/requests",
        {
            "app_id": app_id,
            "title": "Phone ops file edit",
            "request_text": (
                f"Update only {scratch_file}. "
                "Replace `marker: unchanged` with `marker: phone_ops_verified`. "
                "Do not modify any other file, and summarize the exact edit."
            ),
            "source": "remote-runtime-smoke-test",
            "execute_now": True,
        },
        api_key=api_key,
    )
    edit_job = wait_for_job(base_url, edit["job"]["job_id"], api_key)
    if edit_job.get("status") != "completed":
        raise RuntimeError(f"Edit job failed: {edit_job}")

    scratch_content = scratch_path.read_text(encoding="utf-8")
    if "marker: phone_ops_verified" not in scratch_content:
        raise RuntimeError(f"Scratch file not updated as expected: {scratch_content!r}")

    print(
        json.dumps(
            {
                "health_ok": bool(health.get("ok")),
                "api_key_required": bool(health.get("api_key_required")),
                "ping_job_id": ping["job"]["job_id"],
                "ping_result": ping_job.get("result_summary", "").strip(),
                "edit_job_id": edit["job"]["job_id"],
                "edit_status": edit_job.get("status"),
                "scratch_file": str(scratch_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
