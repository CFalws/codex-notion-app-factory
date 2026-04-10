#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from importlib import import_module
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


def load_playwright() -> tuple[Any, Any]:
    try:
        playwright = import_module("playwright.sync_api")
    except ImportError as exc:
        raise RuntimeError(
            "browser runtime verification requires the Python playwright package and installed browser binaries"
        ) from exc
    return playwright.sync_playwright, playwright.TimeoutError


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


def browser_snapshot_script() -> str:
    return """
() => {
  const summary = document.querySelector("#session-summary-row");
  const healthyBlock = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-block-owner="selected-thread"]');
  const degradedBlock = document.querySelector('.session-inline-block[data-selected-thread-degraded-block="true"][data-live-block-owner="selected-thread"]');
  const follow = document.querySelector("#jump-to-latest");
  const composerDock = document.querySelector("#conversation-footer-dock");
  const composerOwnerRow = document.querySelector("#composer-owner-row");
  const sendRequest = document.querySelector("#send-request");
  const transition = document.querySelector('[data-thread-transition="loading"]');
  return {
    summary: summary ? {
      hidden: !!summary.hidden,
      dataset: { ...summary.dataset },
      text: (summary.textContent || "").trim(),
    } : null,
    healthyBlock: healthyBlock ? {
      dataset: { ...healthyBlock.dataset },
      text: (healthyBlock.textContent || "").trim(),
    } : null,
    degradedBlock: degradedBlock ? {
      dataset: { ...degradedBlock.dataset },
      text: (degradedBlock.textContent || "").trim(),
    } : null,
    follow: follow ? {
      hidden: !!follow.hidden,
      dataset: { ...follow.dataset },
      text: (follow.textContent || "").trim(),
    } : null,
    composerDock: composerDock ? {
      dataset: { ...composerDock.dataset },
      position: getComputedStyle(composerDock).position,
    } : null,
    composerOwnerRow: composerOwnerRow ? {
      dataset: { ...composerOwnerRow.dataset },
      text: (composerOwnerRow.textContent || "").trim(),
    } : null,
    sendRequest: sendRequest ? {
      dataset: { ...sendRequest.dataset },
      text: (sendRequest.textContent || "").trim(),
      disabled: !!sendRequest.disabled,
    } : null,
    transition: transition ? {
      dataset: { ...transition.dataset },
      text: (transition.textContent || "").trim(),
    } : null,
  };
}
"""


def assert_browser_runtime_surface(
    *,
    base_url: str,
    ops_url: str,
    api_key: str,
    app_id: str,
    conversation_id: str,
    switch_conversation_id: str,
    request_text: str,
    source: str,
) -> dict[str, Any]:
    sync_playwright, playwright_timeout = load_playwright()

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 960},
            extra_http_headers={"X-API-Key": api_key} if api_key else {},
        )
        context.add_init_script(
            """
(() => {
  const NativeEventSource = window.EventSource;
  if (!NativeEventSource) {
    return;
  }
  window.__verifyForceDegrade = false;
  window.__verifyDegraded = false;
  window.EventSource = class VerifyEventSource extends NativeEventSource {
    constructor(...args) {
      super(...args);
      this.addEventListener("conversation.append", () => {
        if (!window.__verifyForceDegrade || window.__verifyDegraded) {
          return;
        }
        window.__verifyDegraded = true;
        try {
          this.close();
          this.dispatchEvent(new Event("error"));
        } catch (_) {
          // Let the app fallback path recover.
        }
      });
    }
  };
})();
"""
        )
        page = context.new_page()
        try:
            page.goto(ops_url, wait_until="domcontentloaded", timeout=30000)
            page.wait_for_selector("#app-select", timeout=30000)
            page.select_option("#app-select", app_id)
            page.wait_for_function(
                """([primaryId, switchId]) => {
                  return Boolean(
                    document.querySelector(`[data-conversation-id="${primaryId}"]`) &&
                    document.querySelector(`[data-conversation-id="${switchId}"]`)
                  );
                }""",
                [conversation_id, switch_conversation_id],
                timeout=30000,
            )
            page.click(f'[data-conversation-id="{conversation_id}"]')
            page.wait_for_function(
                """conversationId => {
                  const summary = document.querySelector("#session-summary-row");
                  const sendRequest = document.querySelector("#send-request");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  return Boolean(
                    summary &&
                    sendRequest &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    document.querySelector(`[data-conversation-id="${conversationId}"]`)
                  );
                }""",
                conversation_id,
                timeout=30000,
            )

            page.fill("#request-text", request_text)
            page.click("#send-request")

            deadline = time.monotonic() + 60
            job_id = ""
            while time.monotonic() < deadline:
                payload = http_json("GET", f"{base_url}/api/conversations/{conversation_id}", api_key=api_key)
                job_id = str(payload.get("latest_job_id", "") or "")
                if job_id:
                    break
                time.sleep(1)
            if not job_id:
                raise RuntimeError("browser runtime verifier could not observe latest_job_id after composer submit")

            page.wait_for_function(
                """conversationId => {
                  const block = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-owned="true"]');
                  const summary = document.querySelector("#session-summary-row");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const sendRequest = document.querySelector("#send-request");
                  const follow = document.querySelector("#jump-to-latest");
                  return Boolean(
                    block &&
                    block.dataset.liveBlockOwner === "selected-thread" &&
                    block.dataset.liveBlockSource === "sse" &&
                    block.dataset.liveBlockPhase &&
                    block.dataset.liveBlockPhase !== "IDLE" &&
                    summary &&
                    summary.dataset.liveSessionOwned === "true" &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    sendRequest &&
                    sendRequest.dataset.composerOwnerState &&
                    follow &&
                    follow.dataset.followOwned !== undefined
                  );
                }""",
                conversation_id,
                timeout=120000,
            )
            healthy_snapshot = page.evaluate(browser_snapshot_script())

            page.evaluate("() => { window.__verifyForceDegrade = true; }")
            page.wait_for_function(
                """() => {
                  const degraded = document.querySelector('.session-inline-block[data-selected-thread-degraded-block="true"][data-live-owned="false"]');
                  const healthy = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-owned="true"]');
                  const summary = document.querySelector("#session-summary-row");
                  const follow = document.querySelector("#jump-to-latest");
                  if (!degraded || healthy || !summary || !follow) {
                    return false;
                  }
                  const reason = degraded.dataset.liveBlockReason || "";
                  const phase = degraded.dataset.liveBlockPhase || "";
                  return (
                    ["retrying", "reconnecting", "polling-fallback", "session-rotation"].includes(reason) &&
                    ["RECONNECT", "POLLING"].includes(phase) &&
                    summary.dataset.liveSessionOwned === "false" &&
                    follow.dataset.followOwned !== "selected-thread"
                  );
                }""",
                timeout=120000,
            )
            degraded_snapshot = page.evaluate(browser_snapshot_script())

            page.click(f'[data-conversation-id="{switch_conversation_id}"]')
            page.wait_for_function(
                """targetConversationId => {
                  const transition = document.querySelector('[data-thread-transition="loading"]');
                  const summary = document.querySelector("#session-summary-row");
                  const sendRequest = document.querySelector("#send-request");
                  const healthy = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-owned="true"]');
                  const degraded = document.querySelector('.session-inline-block[data-selected-thread-degraded-block="true"]');
                  return Boolean(
                    transition &&
                    transition.dataset.threadTransitionConversationId === targetConversationId &&
                    summary &&
                    summary.dataset.summaryPath === "switching" &&
                    sendRequest &&
                    sendRequest.dataset.composerOwnerState === "switching" &&
                    !healthy &&
                    !degraded
                  );
                }""",
                switch_conversation_id,
                timeout=30000,
            )
            switch_snapshot = page.evaluate(browser_snapshot_script())
            return {
                "job_id": job_id,
                "healthy": healthy_snapshot,
                "degraded": degraded_snapshot,
                "switch": switch_snapshot,
            }
        except playwright_timeout as exc:
            raise RuntimeError(f"browser runtime verification timed out: {exc}") from exc
        finally:
            context.close()
            browser.close()


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
    require(html, 'id="recent-thread-rail"', label="recent-thread rail")
    require(html, 'id="recent-thread-rail-list"', label="recent-thread rail list")
    require(html, 'id="session-live-indicator"', label="session live indicator")
    require(html, 'data-live-session-source="none"', label="session live indicator source default")
    require(html, 'data-live-session-owned="false"', label="session live indicator ownership default")
    require(html, 'data-live-session-reason="idle"', label="session live indicator reason default")
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
    require(styles, ".recent-thread-rail", label="recent-thread rail CSS")
    require(styles, ".recent-thread-rail-list", label="recent-thread rail list CSS")
    require(styles, ".recent-thread-chip", label="recent-thread chip CSS")
    require(styles, '.recent-thread-chip[data-thread-state="switching"] .recent-thread-token[data-recent-thread-state]', label="recent-thread switching chip CSS")
    require(styles, '.recent-thread-chip[data-live-owner="true"] .recent-thread-token[data-recent-thread-owner]', label="recent-thread owner chip CSS")
    require(styles, '.recent-thread-chip[data-live-owner-state="new"] .recent-thread-token[data-recent-thread-follow]', label="recent-thread new follow chip CSS")
    require(styles, ".session-live-indicator", label="session live indicator CSS")
    require(styles, '.session-live-indicator[data-live-session-tone="healthy"]', label="session live indicator healthy CSS")
    require(styles, '.session-live-indicator[data-live-session-tone="warning"]', label="session live indicator warning CSS")
    require(styles, '.session-live-indicator[data-live-session-tone="danger"]', label="session live indicator danger CSS")
    require(styles, ".composer-owner-row", label="composer owner row CSS")
    require(styles, ".composer-owner-chip", label="composer owner chip CSS")
    require(styles, ".session-inline-block", label="inline session block CSS")
    require(styles, ".session-inline-autonomy", label="inline autonomy row CSS")
    require(styles, ".timeline-transition", label="thread transition CSS")
    require(styles, '.session-strip[data-stream-state="reconnecting"]', label="reconnecting session strip CSS")
    require(styles, '.session-strip[data-stream-state="offline"]', label="offline session strip CSS")
    require(styles, '.session-strip[data-stream-state="connecting"]', label="connecting session strip CSS")

    require(render_js, "renderSessionSummary", label="session summary helper")
    require(render_js, "selectedThreadLiveSessionIndicator", label="session live indicator helper")
    require(render_js, "latestSessionIndicatorEvent", label="session live indicator event helper")
    require(render_js, "composerOwnerState", label="composer owner state helper")
    require(render_js, "syncComposerOwnership", label="composer ownership sync helper")
    require(render_js, "compactTargetLabel", label="compact target label helper")
    require(render_js, "summaryHint", label="summary hint helper")
    require(render_js, "phaseChip", label="live phase chip helper")
    require(render_js, "transportChip", label="live transport chip helper")
    require(render_js, "shouldShowComposerLiveStrip", label="session strip visibility helper")
    require(render_js, "selectedThreadInlineSessionState", label="inline session visibility helper")
    require(render_js, "const degradedVisible =", label="inline degraded visibility helper")
    require(render_js, 'sessionIndicator.state === "reconnecting" || sessionIndicator.state === "polling"', label="inline degraded state scope")
    require(render_js, "summarizeInlineAutonomy", label="inline autonomy summary helper")
    require(render_js, "buildAutonomySummary", label="shared autonomy summary builder")
    require(render_js, "if (inlineState.visible) {", label="composer strip suppression guard")
    require(render_js, "renderInlineSessionBlock", label="inline session block helper")
    require(render_js, "INLINE_TERMINAL_RETENTION_MS = 12000", label="inline terminal retention window")
    require(render_js, "shouldRetainInlineTerminalPhase", label="inline terminal retention helper")
    require(render_js, "renderThreadTransition", label="thread transition helper")
    require(render_js, "pendingHandoffState", label="pending handoff helper")
    require(render_js, 'data-thread-transition="loading"', label="thread transition DOM")
    require(render_js, 'dom.conversationTimeline.innerHTML = isThreadTransition', label="thread transition placeholder render branch")
    require(render_js, '? renderThreadTransition(currentState)', label="thread transition placeholder render path")
    require(
        render_js,
        ": '<p class=\"timeline-empty\">새 대화를 만들면 요청과 이벤트가 여기 쌓입니다.</p>';",
        label="generic empty state fallback path",
    )
    require(render_js, 'conversationState: isThreadTransition ? "새 대화 스냅샷을 연결하는 중입니다." : "아직 대화 세션이 없습니다.",', label="thread transition conversation state copy")
    require(render_js, 'threadTitle: isThreadTransition ? String(threadTransition.targetTitle || "대화 전환 중") : "새 대화를 시작하세요",', label="thread transition title copy")
    require(render_js, "dataset.threadTransitionState", label="thread transition state dataset")
    require(render_js, 'renderSessionStrip(dom, currentState, null);', label="thread transition composer shell render path")
    require(render_js, 'syncComposerOwnership(dom, currentState, null);', label="thread transition composer owner switching path")
    require(render_js, 'data-selected-thread-live-block="${degradedVisible ? "false" : "true"}"', label="inline session block DOM")
    require(render_js, 'data-selected-thread-degraded-block="${degradedVisible ? "true" : "false"}"', label="inline degraded session block DOM")
    require(render_js, 'data-live-block-owner="selected-thread"', label="inline session block owner DOM")
    require(render_js, 'data-live-owned="${degradedVisible ? "false" : "true"}"', label="inline session block ownership DOM")
    require(render_js, 'data-live-block-phase="', label="inline session block phase DOM")
    require(render_js, 'data-live-block-reason="${escapeHtml(degradedVisible ? String(sessionIndicator.reason || "polling-fallback") : "healthy")}"', label="inline degraded session reason DOM")
    require(render_js, 'data-live-autonomy="true"', label="inline autonomy DOM")
    require(render_js, 'data-autonomy-path-verdict="', label="inline autonomy path verdict dataset")
    require(render_js, 'data-autonomy-verifier-acceptability="', label="inline autonomy verifier dataset")
    require(render_js, 'data-autonomy-blocker-reason="', label="inline autonomy blocker dataset")
    require(render_js, 'data-autonomy-iteration="', label="inline autonomy iteration dataset")
    require(render_js, 'data-live-block-terminal="', label="inline session block terminal DOM")
    require(render_js, 'sessionIndicator.reason === "session-rotation"', label="inline session rotation degraded copy")
    require(render_js, 'sessionIndicator.reason === "retrying"', label="inline retrying degraded copy")
    require(render_js, '${degradedVisible ? "" : autonomySummary}', label="inline degraded autonomy suppression")
    require(render_js, 'const retainedTerminalVisible = shouldRetainInlineTerminalPhase(', label="inline terminal retention wiring")
    require(render_js, '(!liveRun.terminal || retainedTerminalVisible);', label="inline terminal visibility guard")
    require(render_js, 'liveRun.terminal ? "terminal" : String(liveRun.state || "live")', label="inline terminal stage mapping")
    require(render_js, 'Date.now() - createdAtMs <= INLINE_TERMINAL_RETENTION_MS;', label="inline terminal retention deadline")
    require(render_js, "(liveRun.phase !== \"READY\" && liveRun.phase !== \"APPLIED\")", label="inline terminal phase scope")
    require(render_js, "latestAppendId > terminalAppendId", label="inline terminal next-append clear guard")
    require(render_js, "dataset.liveRunPhase", label="phase dataset")
    require(render_js, "dataset.liveRunSource", label="live run source dataset")
    require(render_js, "dataset.streamState", label="stream state dataset")
    require(render_js, "dataset.sessionOwner", label="session owner dataset")
    require(render_js, "dataset.liveOwned", label="live ownership dataset")
    require(render_js, "dataset.composerOwnerState", label="composer owner state dataset")
    require(render_js, "dataset.followState", label="follow-state dataset")
    require(render_js, "export function renderJobActivity(dom, conversation, currentJobId, jobPayload = null, currentState = null)", label="job activity current-state signature")
    require(render_js, "const selectedThreadSseOwned =", label="job activity selected-thread SSE ownership guard")
    require(render_js, "const liveRun = currentState ? deriveLiveRunState(conversation, currentState)", label="job activity live-run ownership source")
    require(render_js, "const phase = selectedThreadSseOwned", label="job activity phase ownership switch")
    require(render_js, 'String(liveRun.phase || "IDLE").toUpperCase()', label="job activity SSE phase label")
    require(render_js, 'phaseLabel(jobPayload?.status || latestEvent?.status || "", latestEvent?.type || "")', label="job activity polling fallback phase label")
    require(render_js, "currentState.latestProposalJobId =", label="apply readiness from selected-thread live state")
    require(render_js, "updateProposalButton(dom, currentState.latestProposalJobId);", label="apply button updated from selected-thread live state")
    require(render_js, "dataset.liveSessionState", label="live-session state dataset")
    require(render_js, "dataset.liveSessionSource", label="live-session source dataset")
    require(render_js, "dataset.liveSessionReason", label="live-session reason dataset")
    require(render_js, "dataset.liveSessionOwned", label="live-session owned dataset")
    require(render_js, 'dom.sessionLiveIndicator.dataset.liveSessionSource = sessionIndicator.source;', label="header indicator source dataset")
    require(render_js, 'dom.sessionLiveIndicator.dataset.liveSessionOwned = sessionIndicator.owned ? "true" : "false";', label="header indicator ownership dataset")
    require(render_js, 'dom.sessionLiveIndicator.dataset.liveSessionReason = sessionIndicator.reason;', label="header indicator reason dataset")
    require(render_js, 'label: "SSE OWNER"', label="live-session healthy ownership label")
    require(render_js, 'label: "RECONNECT"', label="live-session reconnect label")
    require(render_js, 'label: "POLLING"', label="live-session polling label")
    require(render_js, 'type === "codex.exec.retrying"', label="live-session retry degradation mapping")
    require(render_js, "selectedThreadSseOwned", label="selected-thread SSE handoff guard")
    require(render_js, 'const handoffVisible = handoffState.stage === "pending-assistant" && selectedThreadSseOwned;', label="inline handoff visibility guard")
    require(render_js, "const liveVisible =", label="inline live visibility guard")
    require(render_js, 'status !== "live"', label="healthy-only composer strip guard")
    require(render_js, 'return inlineState.renderSource === "sse";', label="healthy-only composer strip render-source guard")
    require(render_js, 'const liveOwned = inlineState.selectedThreadSseOwned && inlineState.status === "live" && inlineState.renderSource === "sse";', label="composer strip ownership decoupled from strip visibility")
    require(render_js, 'dom.sessionStrip.dataset.sessionOwner = liveOwned ? "selected-thread" : "none";', label="composer strip selected-thread owner dataset")
    require(render_js, 'dom.sessionStrip.dataset.followState = sessionOwnerState.state;', label="composer strip follow-state dataset")
    require_absent(render_js, 'status === "reconnecting" || status === "connecting" || status === "offline"', label="legacy degraded strip visibility guard")
    require(render_js, 'return { label: "ACCEPTED", tone: "neutral" };', label="accepted handoff chip")
    require(render_js, '"RECONNECT"', label="reconnecting provenance label")
    require(render_js, '"OPEN"', label="connecting provenance label")
    require(render_js, '"OFFLINE"', label="offline provenance label")
    require(render_js, 'const stage = degradedVisible', label="inline degraded stage mapping")
    require(render_js, 'const phaseLabel = degradedVisible', label="inline degraded phase mapping")
    require(render_js, 'const sourceLabel = degradedVisible ? String(sessionIndicator.source || "polling") : handoffVisible ? "handoff" : "sse";', label="inline degraded source mapping")
    require(render_js, "const renderedItems = items", label="transcript render item join")
    require(render_js, 'dom.conversationTimeline.innerHTML = renderedItems + inlineSessionBlock;', label="transcript tail inline block render")
    require_absent(render_js, 'dom.conversationTimeline.innerHTML = inlineSessionBlock + items', label="legacy inline block prepended render")
    require_absent(render_js, "In Flight Assistant", label="duplicate accepted status block copy")
    require(render_js, "pendingAppendCount", label="follow control unseen append state")
    require(render_js, 'const terminalIdle = String(dom.threadScroller?.dataset.sessionTerminal || "false") === "true";', label="follow control terminal-idle guard")
    require(render_js, 'const detached = !Boolean(liveFollow.isFollowing);', label="follow control detached-state guard")
    require(render_js, 'const hasBacklog = unseenCount > 0;', label="follow control backlog guard")
    require(render_js, 'const pausedVisible = liveOwned && detached && !hasBacklog;', label="follow control paused visibility guard")
    require(render_js, 'const followState = hasBacklog ? "new" : "paused";', label="follow control state mapping")
    require(render_js, 'const isVisible = Boolean(liveOwned && detached);', label="follow control visibility mapping")
    require(render_js, 'dom.jumpToLatestButton.dataset.followOwned = liveOwned ? "selected-thread" : "none";', label="follow control owner dataset")
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
    require(conversations_js, "syncSelectedAppSession", label="selected app session sync helper")
    require(conversations_js, 'option.dataset.sessionId = app.session_id || "";', label="selected app session id option dataset")
    require(conversations_js, "rotationDetected", label="selected app session rotation detection")
    require(conversations_js, "renderRecentThreadRail", label="recent-thread rail render helper")
    require(conversations_js, "RECENT_THREAD_LIMIT = 4", label="bounded recent-thread rail limit")
    require(conversations_js, "data-recent-thread-chip", label="recent-thread chip DOM")
    require(conversations_js, "data-recent-thread-owner", label="recent-thread owner DOM")
    require(conversations_js, "data-recent-thread-state", label="recent-thread state DOM")
    require(conversations_js, "data-recent-thread-follow", label="recent-thread follow DOM")
    require(conversations_js, 'chip.dataset.liveOwner = isSelected && showLiveMirror ? "true" : "false";', label="recent-thread live owner dataset")
    require(conversations_js, 'follow.textContent = isSwitching ? "ATTACH" : isSelected && showLiveMirror ? liveFollowLabel : "";', label="recent-thread attach follow wiring")
    require(conversations_js, "syncActiveSessionRow", label="active session row helper")
    require(conversations_js, "data-conversation-live-state", label="selected card live dataset")
    require(conversations_js, "data-conversation-live-owner-row", label="selected card live owner row")
    require(conversations_js, "data-conversation-live-detail", label="selected card live detail")
    require(conversations_js, "data-conversation-live-follow", label="selected card live follow")
    require(conversations_js, "liveOwnerDetail", label="selected card live detail helper")
    require(conversations_js, "liveOwnerFollowLabel", label="selected card live follow helper")
    require(conversations_js, "liveOwnerState", label="selected card live owner state helper")
    require(conversations_js, "liveOwnerMarkerLabel", label="selected card live owner marker helper")
    require(conversations_js, 'return "OWNER";', label="selected card live owner session chip label")
    require(conversations_js, 'return "PROPOSAL";', label="compact proposal rail label")
    require(conversations_js, 'return "WAITING";', label="compact waiting rail label")
    require(conversations_js, 'return "ACTIVE";', label="compact active rail label")
    require(conversations_js, "메시지가 접수되어 첫 응답을 기다리는 중입니다.", label="accepted event preview copy")
    require(conversations_js, "작업이 대기열에 올라 있습니다.", label="queued event preview copy")
    require(conversations_js, "최근 작업이 현재 진행 중입니다.", label="running event preview copy")
    require(conversations_js, "startThreadTransition", label="thread transition start helper")
    require(conversations_js, "clearThreadTransition", label="thread transition clear helper")
    require(conversations_js, 'state.currentConversationId = "";', label="thread switch clears current conversation before attach")
    require(conversations_js, 'const selectedThreadSseOwned = selectedConversationId && selectedConversationId === liveConversationId && renderSource === "sse";', label="selected card sse ownership guard")
    require(conversations_js, 'card.dataset.liveOwner = isSelected && showLiveMirror ? "true" : "false";', label="selected live owner dataset")
    require(conversations_js, 'card.dataset.liveOwnerState = isSelected && showLiveMirror ? liveOwnerStateLabel : "idle";', label="selected live owner state dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionState = visible ? rowState : "idle";', label="active session row state dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionConversationId = visible ? conversationId : "";', label="active session row conversation dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionFollow = visible ? followLabel.toLowerCase() : "idle";', label="active session row follow dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionOwned = visible ? String(rowOwned) : "false";', label="active session row ownership dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionSource = visible ? rowSource : "none";', label="active session row source dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionPhase = visible ? rowPhase : "IDLE";', label="active session row phase dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionUnseenCount = String(visible ? rowUnseenCount : 0);', label="active session row unseen dataset")
    require(conversations_js, 'rowSource = "thread-transition";', label="active session switching source")
    require(conversations_js, 'rowSource = pendingStage === "pending-user" ? "local-handoff" : pendingStage === "pending-assistant" ? "selected-thread-handoff" : "selected-thread-sse";', label="active session selected-thread source")
    require(conversations_js, 'presentation === "live"', label="active session healthy live gate")
    require_absent(conversations_js, 'meta = "selected thread · reconnecting";', label="active session reconnecting copy")
    require(conversations_js, "syncSelectedSessionFromLiveAppend", label="selected-thread live append sync helper")
    require(conversations_js, "shouldRefreshGoalSummaryFromLiveAppend", label="goal summary append refresh helper")
    require(conversations_js, "liveJobMetaLabel", label="live append job meta helper")
    require(conversations_js, "refreshGoalSummary().catch(() => {});", label="append-driven autonomy summary refresh")
    require(conversations_js, "setJobMeta(dom, immediateMeta);", label="append-driven job meta refresh")
    require(conversations_js, "ensurePollingForJob();", label="reconnect polling resume")
    require(conversations_js, 'state.appendStream.transport = "sse"', label="selected-thread sse transport")
    require(styles, ".conversation-card-live-owner-row", label="selected card live owner row CSS")
    require(styles, ".active-session-row", label="active session row CSS")
    require(styles, ".active-session-chip", label="active session chip CSS")
    require(styles, '.active-session-row[data-active-session-state="switching"] .active-session-chip[data-active-chip="state"]', label="active session switching chip CSS")
    require(styles, '.active-session-row[data-active-session-follow="new"] .active-session-chip[data-active-chip="follow"]', label="active session new chip CSS")
    require(styles, '.conversation-card[data-live-owner-state="handoff"] .conversation-card-marker', label="selected handoff owner marker CSS")
    require(styles, '.conversation-card[data-live-owner-state="new"] .conversation-card-marker', label="selected new owner marker CSS")
    require(styles, '.conversation-card[data-live-owner-state="paused"] .conversation-card-marker', label="selected paused owner marker CSS")
    require(index_html, 'class="jump-to-latest-chip"', label="follow control chip DOM")
    require(index_html, 'class="jump-to-latest-copy"', label="follow control copy DOM")
    require(index_html, 'id="active-session-row"', label="active session row DOM")
    require(index_html, 'id="active-session-owner"', label="active session owner DOM")
    require(index_html, 'id="active-session-state"', label="active session state DOM")
    require(index_html, 'id="active-session-follow"', label="active session follow DOM")
    require(index_html, 'data-active-session-owned="false"', label="active session owned default")
    require(index_html, 'data-active-session-source="none"', label="active session source default")
    require(index_html, 'data-active-session-phase="IDLE"', label="active session phase default")
    require(index_html, 'data-active-session-unseen-count="0"', label="active session unseen default")
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
    verify_browser_runtime = os.environ.get("VERIFY_BROWSER_RUNTIME", "1").strip().lower() not in {"0", "false", "no"}

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
    switch_conversation = http_json(
        "POST",
        f"{base_url}/api/conversations",
        {"app_id": app_id, "source": f"{source}-switch-target"},
        api_key=api_key,
    )
    switch_conversation_id = str(switch_conversation["conversation_id"])

    recorder = SSERecorder(
        f"{base_url}/api/internal/conversations/{conversation_id}/append-stream",
        api_key,
        timeout_seconds=180,
    )
    recorder.start()
    time.sleep(1)

    browser_runtime = (
        assert_browser_runtime_surface(
            base_url=base_url,
            ops_url=ops_url,
            api_key=api_key,
            app_id=app_id,
            conversation_id=conversation_id,
            switch_conversation_id=switch_conversation_id,
            request_text=request_text,
            source=source,
        )
        if verify_browser_runtime
        else None
    )
    if not browser_runtime:
        raise RuntimeError("browser runtime verification is required for the deployed workspace gate")

    job_id = str(browser_runtime["job_id"])
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
                "switch_conversation_id": switch_conversation_id,
                "job_id": job_id,
                "job_status": job.get("status"),
                "sse_phase_events": captured_types,
                "terminal_event": terminal_event,
                "browser_runtime": "ok",
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
