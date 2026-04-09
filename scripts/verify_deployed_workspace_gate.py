#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from typing import Any
from urllib import parse, request


DEFAULT_REQUEST_TEXT = (
    "Prepare a minimal docs-only proposal through the normal proposal flow. "
    "Change only docs/factory-runtime/tasks.md in the proposal, do not apply it, "
    "and stop when proposal review and verification are complete."
)


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


def http_text(url: str, *, api_key: str = "") -> str:
    headers: dict[str, str] = {}
    if api_key:
        headers["X-API-Key"] = api_key
    req = request.Request(url, headers=headers)
    with request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def require(content: str, needle: str, *, label: str) -> None:
    if needle not in content:
        raise RuntimeError(f"missing {label}: {needle}")


def require_absent(content: str, needle: str, *, label: str) -> None:
    if needle in content:
        raise RuntimeError(f"unexpected {label}: {needle}")


class SSERecorder:
    def __init__(self, url: str, api_key: str, timeout_seconds: float) -> None:
        self._url = url
        self._api_key = api_key
        self._timeout_seconds = timeout_seconds
        self._process: subprocess.Popen[str] | None = None
        self._thread: threading.Thread | None = None
        self.events: list[dict[str, Any]] = []
        self.errors: list[str] = []

    def start(self) -> None:
        command = ["curl", "-sS", "-N", "--max-time", str(int(self._timeout_seconds)), self._url]
        if self._api_key:
            command.extend(["-H", f"X-API-Key: {self._api_key}"])
        command.extend(["-H", "Accept: text/event-stream"])
        self._process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
        self._thread = threading.Thread(target=self._read_stream, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._process is not None and self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=5)
        if self._thread is not None:
            self._thread.join(timeout=5)
        if self._process is not None and self._process.stderr is not None:
            stderr_output = self._process.stderr.read().strip()
            if stderr_output and "Operation timed out" not in stderr_output:
                self.errors.append(stderr_output)

    def _read_stream(self) -> None:
        assert self._process is not None
        assert self._process.stdout is not None
        event_name = "message"
        data_lines: list[str] = []
        for raw_line in self._process.stdout:
            line = raw_line.rstrip("\n")
            if not line:
                if data_lines:
                    data_text = "\n".join(data_lines)
                    try:
                        payload = json.loads(data_text)
                    except json.JSONDecodeError:
                        payload = {"raw": data_text}
                    self.events.append(
                        {
                            "event": event_name,
                            "data": payload,
                            "received_at": time.time(),
                        }
                    )
                event_name = "message"
                data_lines = []
                continue
            if line.startswith("event:"):
                event_name = line.split(":", 1)[1].strip()
                continue
            if line.startswith("data:"):
                data_lines.append(line.split(":", 1)[1].lstrip())


def wait_for_job(base_url: str, job_id: str, api_key: str, *, timeout_seconds: float = 420.0) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        payload = http_json("GET", f"{base_url}/api/jobs/{job_id}", api_key=api_key)
        if payload.get("status") in {"completed", "failed"}:
            return payload
        time.sleep(2)
    raise RuntimeError(f"timed out waiting for job {job_id}")


def assert_console_contract(ops_url: str, api_key: str) -> None:
    html = http_text(ops_url, api_key=api_key)
    styles = http_text(parse.urljoin(ops_url, "styles.css"), api_key=api_key)
    render_js = http_text(parse.urljoin(ops_url, "ops-render.js"), api_key=api_key)
    conversations_js = http_text(parse.urljoin(ops_url, "ops-conversations.js"), api_key=api_key)

    require(html, 'id="nav-sheet"', label="phone nav sheet")
    require(html, 'data-primary-surface="conversation"', label="primary conversation surface")
    require(html, 'id="thread-scroller"', label="thread scroller")
    require(html, 'data-session-workspace="conversation-first"', label="conversation-first session workspace")
    require(html, 'id="conversation-footer-dock"', label="footer dock")
    require(html, 'id="session-strip"', label="session strip")
    require(html, 'id="secondary-panel"', label="secondary panel")
    require(html, 'data-secondary-panel-mode="compact-sidecar"', label="compact side panel mode")
    require_absent(html, 'id="hero-conversation-state"', label="legacy header conversation state")
    require_absent(html, 'id="autonomy-context-strip"', label="legacy autonomy context strip")

    require(styles, 'grid-template-columns: 15rem minmax(0, 1fr);', label="desktop two-pane shell")
    require(styles, 'body[data-mobile-workspace="conversation"] .main-stage', label="phone conversation-first surface")
    require(styles, 'body[data-secondary-panel-open="true"] .desktop-shell', label="secondary panel overlay shell")
    require(styles, "position: sticky;", label="sticky footer dock")
    require(styles, "env(safe-area-inset-bottom)", label="safe-area footer padding")
    require(styles, ".session-inline-block", label="inline session block CSS")

    require(render_js, "phaseChip", label="live phase chip helper")
    require(render_js, "transportChip", label="live transport chip helper")
    require(render_js, "renderInlineSessionBlock", label="inline session block helper")
    require(render_js, 'data-selected-thread-live-block="true"', label="inline session block DOM")
    require(render_js, "dataset.liveRunPhase", label="phase dataset")
    require(render_js, "dataset.liveRunSource", label="live run source dataset")
    require(render_js, "dataset.streamState", label="stream state dataset")
    require(render_js, 'phase: "PROPOSAL"', label="proposal phase mapping")
    require(render_js, 'phase: "REVIEW"', label="review phase mapping")
    require(render_js, 'phase: "VERIFY"', label="verify phase mapping")
    require(render_js, 'phase: "READY"', label="proposal ready phase mapping")
    require(render_js, "session-chip", label="chip-first session rail")
    require(conversations_js, "appendEnvelope.conversation_id !== activeConversationId", label="selected-thread SSE guard")
    require(conversations_js, "data-conversation-live-state", label="selected card live dataset")
    require(conversations_js, 'state.appendStream.transport = "sse"', label="selected-thread sse transport")


def assert_conversation_events(
    conversation: dict[str, Any],
    *,
    conversation_id: str,
    expect_terminal: str,
) -> None:
    events = conversation.get("events", [])
    event_types = [str(event.get("type", "")) for event in events]
    for required in (
        "conversation.created",
        "message.accepted",
        "intent.interpreted",
        "job.queued",
        "job.running",
        "goal.proposal.phase.started",
        "goal.review.phase.started",
        "goal.verify.phase.started",
        "proposal.ready",
    ):
        if required not in event_types:
            raise RuntimeError(f"missing conversation event: {required}")
    if expect_terminal not in event_types:
        raise RuntimeError(f"missing terminal conversation event: {expect_terminal}")
    for forbidden in ("codex.exec.retrying", "runtime.exception"):
        if forbidden in event_types:
            raise RuntimeError(f"unexpected degraded event: {forbidden}")
    if conversation.get("conversation_id") != conversation_id:
        raise RuntimeError("conversation payload does not match selected-thread conversation")


def assert_sse_capture(recorder: SSERecorder, conversation_id: str) -> list[str]:
    if recorder.errors:
        raise RuntimeError(f"SSE capture errors: {recorder.errors}")
    append_events = [event for event in recorder.events if event.get("event") == "conversation.append"]
    if not append_events:
        raise RuntimeError("no conversation.append events were captured from the selected-thread stream")

    captured_types: list[str] = []
    for event in append_events:
        payload = event.get("data", {})
        if not isinstance(payload, dict):
            continue
        payload_conversation_id = str(payload.get("conversation_id", "")).strip()
        if payload_conversation_id and payload_conversation_id != conversation_id:
            raise RuntimeError(f"append stream leaked another conversation_id: {payload_conversation_id}")
        append_id = payload.get("append_id")
        if append_id is None:
            raise RuntimeError("captured append event did not include append_id")
        inner = payload.get("payload", {})
        if not isinstance(inner, dict):
            continue
        event_type = str(inner.get("type", "")).strip()
        if event_type:
            captured_types.append(event_type)
    for required in (
        "goal.proposal.phase.started",
        "goal.review.phase.started",
        "goal.verify.phase.started",
        "proposal.ready",
    ):
        if required not in captured_types:
            raise RuntimeError(f"missing SSE phase event: {required}")
    ordering = [
        captured_types.index("goal.proposal.phase.started"),
        captured_types.index("goal.review.phase.started"),
        captured_types.index("goal.verify.phase.started"),
        captured_types.index("proposal.ready"),
    ]
    if ordering != sorted(ordering):
        raise RuntimeError(f"SSE phase ordering regressed: {captured_types}")
    for forbidden in ("codex.exec.retrying", "runtime.exception"):
        if forbidden in captured_types:
            raise RuntimeError(f"unexpected degraded SSE event: {forbidden}")
    return captured_types


def main() -> int:
    base_url = os.environ.get("BASE_URL", "https://codex-factory-vm.tail1b6dd1.ts.net").rstrip("/")
    ops_url = os.environ.get("OPS_URL", f"{base_url}/ops/")
    app_id = os.environ.get("APP_ID", "factory-runtime").strip() or "factory-runtime"
    api_key = os.environ.get("API_KEY", os.environ.get("CODEX_FACTORY_API_KEY", "")).strip()
    request_text = os.environ.get("VERIFY_REQUEST_TEXT", DEFAULT_REQUEST_TEXT).strip() or DEFAULT_REQUEST_TEXT
    source = os.environ.get("VERIFY_SOURCE", "verify-deployed-workspace-gate").strip() or "verify-deployed-workspace-gate"

    assert_console_contract(ops_url, api_key)

    apps = http_json("GET", f"{base_url}/api/apps", api_key=api_key)
    if not any(str(item.get("app_id", "")) == app_id for item in apps):
        raise RuntimeError(f"app_id not available for workspace gate: {app_id}")

    app_before = http_json("GET", f"{base_url}/api/apps/{app_id}", api_key=api_key)
    before_session_id = str(app_before.get("session_id", "") or "")

    conversation = http_json(
        "POST",
        f"{base_url}/api/conversations",
        {"app_id": app_id, "source": source},
        api_key=api_key,
    )
    conversation_id = str(conversation["conversation_id"])

    recorder = SSERecorder(
        f"{base_url}/api/internal/conversations/{conversation_id}/append-stream",
        api_key,
        timeout_seconds=180,
    )
    recorder.start()
    time.sleep(1)

    message_response = http_json(
        "POST",
        f"{base_url}/api/conversations/{conversation_id}/messages",
        {"message_text": request_text, "source": source},
        api_key=api_key,
    )
    job_id = str(message_response["job"]["job_id"])
    job = wait_for_job(base_url, job_id, api_key)

    time.sleep(2)
    recorder.stop()

    conversation_after = http_json("GET", f"{base_url}/api/conversations/{conversation_id}", api_key=api_key)
    terminal_event = "job.completed" if job.get("status") == "completed" else "job.failed"
    assert_conversation_events(conversation_after, conversation_id=conversation_id, expect_terminal=terminal_event)
    captured_types = assert_sse_capture(recorder, conversation_id)

    app_after = http_json("GET", f"{base_url}/api/apps/{app_id}", api_key=api_key)
    after_session_id = str(app_after.get("session_id", "") or "")
    if before_session_id and after_session_id and before_session_id != after_session_id:
        raise RuntimeError(f"unexpected session rotation: {before_session_id} -> {after_session_id}")

    print(
        json.dumps(
            {
                "workspace_gate": "ok",
                "app_id": app_id,
                "conversation_id": conversation_id,
                "job_id": job_id,
                "job_status": job.get("status"),
                "sse_phase_events": captured_types,
                "terminal_event": terminal_event,
                "ops_url": ops_url,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:  # noqa: BLE001
        print(f"workspace gate failed: {error}", file=sys.stderr)
        raise SystemExit(1)
