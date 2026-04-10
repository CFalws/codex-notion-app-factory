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
    require(html, 'id="selected-app-summary"', label="selected app summary")
    require(html, 'data-primary-surface="conversation"', label="primary conversation surface")
    require(html, 'id="thread-scroller"', label="thread scroller")
    require(html, 'data-session-workspace="conversation-first"', label="conversation-first session workspace")
    require(html, 'id="session-summary-row"', label="session summary row")
    require(html, 'id="session-summary-path"', label="session summary path")
    require(html, 'id="session-summary-state"', label="session summary state")
    require(html, 'id="conversation-footer-dock"', label="footer dock")
    require(html, 'id="session-strip"', label="session strip")
    require(html, 'id="composer-owner-row"', label="composer owner row")
    require(html, 'id="composer-owner-state"', label="composer owner state")
    require(html, 'id="composer-owner-target"', label="composer owner target")
    require(html, 'id="composer-utility-menu"', label="composer utility menu")
    require(html, 'id="composer-utility-toggle"', label="composer utility toggle")
    require(html, 'id="composer-utility-cluster"', label="composer utility cluster")
    require(html, 'data-composer-layout="chat-first"', label="chat-first composer footer")
    require(html, 'id="secondary-panel"', label="secondary panel")
    require(html, 'data-secondary-panel-mode="compact-sidecar"', label="compact side panel mode")
    require_absent(html, 'id="hero-conversation-state"', label="legacy header conversation state")
    require_absent(html, 'id="autonomy-context-strip"', label="legacy autonomy context strip")

    require(styles, 'grid-template-columns: 15rem minmax(0, 1fr);', label="desktop two-pane shell")
    require(styles, 'body[data-mobile-workspace="conversation"] .main-stage', label="phone conversation-first surface")
    require(styles, 'body[data-secondary-panel-open="true"] .desktop-shell', label="secondary panel overlay shell")
    require(styles, ".sidebar-app-summary", label="compact app summary CSS")
    require(styles, ".nav-ops-summary", label="operator summary toggle CSS")
    require(styles, "position: sticky;", label="sticky footer dock")
    require(styles, "env(safe-area-inset-bottom)", label="safe-area footer padding")
    require(styles, ".composer-utility-menu", label="composer utility menu CSS")
    require(styles, ".composer-utility-toggle-button", label="composer utility toggle CSS")
    require(styles, ".composer-utility-cluster", label="composer utility cluster CSS")
    require(styles, ".session-summary-row", label="session summary row CSS")
    require(styles, ".composer-owner-row", label="composer owner row CSS")
    require(styles, ".composer-owner-chip", label="composer owner chip CSS")
    require(styles, ".session-inline-block", label="inline session block CSS")
    require(styles, ".timeline-transition", label="thread transition CSS")

    require(render_js, "renderSessionSummary", label="session summary helper")
    require(render_js, "composerOwnerState", label="composer owner state helper")
    require(render_js, "syncComposerOwnership", label="composer ownership sync helper")
    require(render_js, "phaseChip", label="live phase chip helper")
    require(render_js, "transportChip", label="live transport chip helper")
    require(render_js, "renderInlineSessionBlock", label="inline session block helper")
    require(render_js, "renderThreadTransition", label="thread transition helper")
    require(render_js, 'data-thread-transition="loading"', label="thread transition DOM")
    require(render_js, 'dom.conversationTimeline.innerHTML = isThreadTransition', label="thread transition placeholder render branch")
    require(render_js, '? renderThreadTransition(currentState)', label="thread transition placeholder render path")
    require(render_js, "dataset.threadTransitionState", label="thread transition state dataset")
    require(render_js, 'data-selected-thread-live-block="true"', label="inline session block DOM")
    require(render_js, "dataset.liveRunPhase", label="phase dataset")
    require(render_js, "dataset.liveRunSource", label="live run source dataset")
    require(render_js, "dataset.streamState", label="stream state dataset")
    require(render_js, "dataset.composerOwnerState", label="composer owner state dataset")
    require(render_js, "pendingAppendCount", label="follow control unseen append state")
    require(render_js, 'const followState = renderSource === "sse" ? "new" : "paused";', label="follow control state mapping")
    require(render_js, 'dom.jumpToLatestButton.dataset.followState = isVisible ? followState : "hidden";', label="follow control state dataset")
    require(render_js, 'dom.jumpToLatestButton.dataset.followCount = String(isVisible ? unseenCount : 0);', label="follow control count dataset")
    require(render_js, "새 live append", label="follow control new copy")
    require(render_js, "live follow paused", label="follow control paused copy")
    require(render_js, 'phase: "PROPOSAL"', label="proposal phase mapping")
    require(render_js, 'phase: "REVIEW"', label="review phase mapping")
    require(render_js, 'phase: "VERIFY"', label="verify phase mapping")
    require(render_js, 'phase: "READY"', label="proposal ready phase mapping")
    require(render_js, "session-chip", label="chip-first session rail")
    require(conversations_js, "appendEnvelope.conversation_id !== activeConversationId", label="selected-thread SSE guard")
    require(conversations_js, "data-conversation-live-state", label="selected card live dataset")
    require(conversations_js, "data-conversation-live-owner-row", label="selected card live owner row")
    require(conversations_js, "data-conversation-live-detail", label="selected card live detail")
    require(conversations_js, "data-conversation-live-follow", label="selected card live follow")
    require(conversations_js, "liveOwnerDetail", label="selected card live detail helper")
    require(conversations_js, "liveOwnerFollowLabel", label="selected card live follow helper")
    require(conversations_js, "liveOwnerState", label="selected card live owner state helper")
    require(conversations_js, "liveOwnerMarkerLabel", label="selected card live owner marker helper")
    require(conversations_js, "startThreadTransition", label="thread transition start helper")
    require(conversations_js, "clearThreadTransition", label="thread transition clear helper")
    require(conversations_js, 'const selectedThreadSseOwned = selectedConversationId && selectedConversationId === liveConversationId && renderSource === "sse";', label="selected card sse ownership guard")
    require(conversations_js, 'card.dataset.liveOwner = isSelected && showLiveMirror ? "true" : "false";', label="selected live owner dataset")
    require(conversations_js, 'card.dataset.liveOwnerState = isSelected && showLiveMirror ? liveOwnerStateLabel : "idle";', label="selected live owner state dataset")
    require(conversations_js, 'state.appendStream.transport = "sse"', label="selected-thread sse transport")
    require(styles, ".conversation-card-live-owner-row", label="selected card live owner row CSS")
    require(styles, '.conversation-card[data-live-owner-state="handoff"] .conversation-card-marker', label="selected handoff owner marker CSS")
    require(styles, '.conversation-card[data-live-owner-state="new"] .conversation-card-marker', label="selected new owner marker CSS")
    require(styles, '.conversation-card[data-live-owner-state="paused"] .conversation-card-marker', label="selected paused owner marker CSS")
    require(index_html, 'class="jump-to-latest-chip"', label="follow control chip DOM")
    require(index_html, 'class="jump-to-latest-copy"', label="follow control copy DOM")
    require(styles, '.jump-to-latest[data-follow-state="new"] .jump-to-latest-chip', label="follow control new state CSS")
    require(styles, '.jump-to-latest[data-follow-state="paused"] .jump-to-latest-chip', label="follow control paused state CSS")


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
