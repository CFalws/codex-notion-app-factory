#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib import request


REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run an end-to-end verification against the runtime HTTP API and local Codex CLI.",
    )
    parser.add_argument("--app-id", default="habit-tracker-pwa", help="Registered app id to target.")
    parser.add_argument("--host", default="127.0.0.1", help="Runtime host to bind and call.")
    parser.add_argument("--port", type=int, default=8787, help="Runtime port to bind and call.")
    parser.add_argument(
        "--codex-command",
        default=os.getenv("CODEX_COMMAND", "codex"),
        help="Codex CLI command to use for the runtime server.",
    )
    parser.add_argument(
        "--startup-timeout",
        type=float,
        default=20.0,
        help="Seconds to wait for the runtime server to become healthy.",
    )
    parser.add_argument(
        "--job-timeout",
        type=float,
        default=180.0,
        help="Seconds to wait for each runtime job to complete.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=2.0,
        help="Seconds between job status polls.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("CODEX_FACTORY_API_KEY", ""),
        help="Optional runtime X-API-Key header value.",
    )
    return parser.parse_args()


def http_json(
    method: str,
    url: str,
    payload: dict[str, Any] | None = None,
    *,
    api_key: str = "",
) -> dict[str, Any] | list[Any]:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if api_key:
        headers["X-API-Key"] = api_key
    req = request.Request(url, method=method, data=data, headers=headers)
    with request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_for_health(base_url: str, timeout_seconds: float, *, api_key: str = "") -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    last_error = ""
    while time.monotonic() < deadline:
        try:
            payload = http_json("GET", f"{base_url}/health", api_key=api_key)
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            time.sleep(0.5)
            continue
        if isinstance(payload, dict) and payload.get("ok") is True:
            return payload
        last_error = f"Unexpected health payload: {payload!r}"
        time.sleep(0.5)
    raise RuntimeError(f"Runtime server did not become healthy in time. Last error: {last_error}")


def wait_for_job(
    base_url: str,
    job_id: str,
    timeout_seconds: float,
    poll_interval: float,
    *,
    api_key: str = "",
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        payload = http_json("GET", f"{base_url}/api/jobs/{job_id}", api_key=api_key)
        if not isinstance(payload, dict):
            raise RuntimeError(f"Unexpected job payload: {payload!r}")
        if payload.get("status") in {"completed", "failed"}:
            return payload
        time.sleep(poll_interval)
    raise RuntimeError(f"Job {job_id} did not finish within {timeout_seconds} seconds.")


def ensure_app_record(base_url: str, app_id: str, *, api_key: str = "") -> dict[str, Any]:
    payload = http_json("GET", f"{base_url}/api/apps/{app_id}", api_key=api_key)
    if not isinstance(payload, dict):
        raise RuntimeError(f"Unexpected app payload: {payload!r}")
    return payload


def build_verification_file(app_record: dict[str, Any]) -> Path:
    workspace_path = REPO_ROOT / app_record["workspace_path"]
    verification_dir = workspace_path / "runtime-api-verification"
    verification_dir.mkdir(parents=True, exist_ok=True)
    verification_path = verification_dir / "scratch.md"
    verification_path.write_text(
        "# Runtime API Verification\n\nstatus: pending\nmarker: unchanged\n",
        encoding="utf-8",
    )
    return verification_path


def create_request(base_url: str, payload: dict[str, Any], *, api_key: str = "") -> dict[str, Any]:
    response = http_json("POST", f"{base_url}/api/requests", payload, api_key=api_key)
    if not isinstance(response, dict):
        raise RuntimeError(f"Unexpected request response: {response!r}")
    return response


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def summarize_result(summary: dict[str, Any]) -> None:
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def launch_server(args: argparse.Namespace) -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["CODEX_COMMAND"] = args.codex_command
    env["CODEX_FACTORY_HOST"] = args.host
    env["CODEX_FACTORY_PORT"] = str(args.port)
    return subprocess.Popen(
        [sys.executable, str(REPO_ROOT / "scripts" / "run_codex_agents_api.py")],
        cwd=REPO_ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def stop_server(process: subprocess.Popen[str]) -> str:
    if process.poll() is None:
        process.terminate()
        try:
            output, _ = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            output, _ = process.communicate(timeout=10)
        return output
    output, _ = process.communicate(timeout=10)
    return output


def main() -> None:
    args = parse_args()
    base_url = f"http://{args.host}:{args.port}"
    process = launch_server(args)
    server_output = ""

    try:
        health = wait_for_health(base_url, args.startup_timeout, api_key=args.api_key)
        app_record_before = ensure_app_record(base_url, args.app_id, api_key=args.api_key)
        verification_path = build_verification_file(app_record_before)
        relative_verification_path = verification_path.relative_to(REPO_ROOT)

        ping_request = create_request(
            base_url,
            {
                "app_id": args.app_id,
                "title": "Runtime ping",
                "request_text": "Reply with exactly one line: RUNTIME_OK. Do not inspect files and do not make any changes.",
                "source": "runtime-api-verification-script",
                "execute_now": True,
            },
            api_key=args.api_key,
        )
        ping_job = wait_for_job(
            base_url,
            ping_request["job"]["job_id"],
            args.job_timeout,
            args.poll_interval,
            api_key=args.api_key,
        )
        require(ping_job["status"] == "completed", f"Ping job failed: {ping_job}")
        require(ping_job["result_summary"].strip() == "RUNTIME_OK", f"Unexpected ping output: {ping_job['result_summary']!r}")

        edit_request = create_request(
            base_url,
            {
                "app_id": args.app_id,
                "title": "Runtime scratch edit verification",
                "request_text": (
                    f"Update only {relative_verification_path}. "
                    "Replace `marker: unchanged` with `marker: runtime_api_verified`. "
                    "Do not modify any other file, and summarize the exact edit."
                ),
                "source": "runtime-api-verification-script",
                "execute_now": True,
            },
            api_key=args.api_key,
        )
        edit_job = wait_for_job(
            base_url,
            edit_request["job"]["job_id"],
            args.job_timeout,
            args.poll_interval,
            api_key=args.api_key,
        )
        require(edit_job["status"] == "completed", f"Edit job failed: {edit_job}")

        verification_content = verification_path.read_text(encoding="utf-8")
        require(
            "marker: runtime_api_verified" in verification_content,
            f"Verification file was not updated as expected: {verification_content!r}",
        )

        app_record_after = ensure_app_record(base_url, args.app_id, api_key=args.api_key)
        require(bool(app_record_after.get("session_id")), "App record is missing a persisted session_id after verification.")
        require(
            app_record_after.get("last_summary", "").strip() == edit_job["result_summary"].strip(),
            "App record last_summary was not updated to the latest job summary.",
        )

        summary = {
            "health": health,
            "app_id": args.app_id,
            "verification_file": str(relative_verification_path),
            "ping_job_id": ping_request["job"]["job_id"],
            "ping_result": ping_job["result_summary"],
            "edit_job_id": edit_request["job"]["job_id"],
            "edit_result_excerpt": edit_job["result_summary"].splitlines()[0] if edit_job["result_summary"] else "",
            "session_id": app_record_after["session_id"],
        }
        summarize_result(summary)
    finally:
        server_output = stop_server(process)
        if process.returncode not in {0, -15}:
            print(server_output)
            raise RuntimeError(f"Runtime server exited with code {process.returncode}.")


if __name__ == "__main__":
    main()
