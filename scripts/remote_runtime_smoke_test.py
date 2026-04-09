#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, request


def load_env_file(path: Path) -> None:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key, value)


def http_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
    *,
    api_key: str = "",
    retries: int = 0,
    retry_delay_seconds: float = 2.0,
) -> dict[str, Any]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, method=method, data=data, headers=headers)
    attempts = max(1, retries + 1)
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except (error.URLError, TimeoutError, ConnectionError) as exc:
            last_error = exc
            if attempt == attempts - 1:
                raise
            time.sleep(retry_delay_seconds)
    if last_error is not None:
        raise last_error
    raise RuntimeError("http_json reached an unreachable state")


def wait_for_health(base_url: str, timeout_seconds: float = 90.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            return http_json("GET", f"{base_url}/health", retries=0)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"Timed out waiting for runtime health: {last_error}")


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
    return f"state/runtime/smoke/{app_id}/phone-ops-check.md"


def main() -> None:
    env_file = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/etc/codex-factory.env")
    load_env_file(env_file)

    api_key = os.environ.get("CODEX_FACTORY_API_KEY", "").strip()
    base_url = os.environ.get("BASE_URL", "http://127.0.0.1")
    app_id = os.environ.get("APP_ID", "habit-tracker-pwa")
    configured_scratch_file = os.environ.get("SCRATCH_FILE", "").strip()

    health = wait_for_health(base_url)
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
        retries=8,
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
        retries=8,
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
