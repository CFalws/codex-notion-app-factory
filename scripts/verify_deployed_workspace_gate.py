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
  const liveActivity = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="true"]');
  const follow = document.querySelector("#jump-to-latest");
  const activeSessionRow = document.querySelector("#active-session-row");
  const sessionStrip = document.querySelector("#session-strip");
  const composerDock = document.querySelector("#conversation-footer-dock");
  const composerOwnerRow = document.querySelector("#composer-owner-row");
  const sendRequest = document.querySelector("#send-request");
  const autonomyDetailCard = document.querySelector(".autonomy-detail-card");
  const autonomyDetail = document.querySelector("#autonomy-detail");
  const statusOutput = document.querySelector("#status-output");
  const executionStatusCard = statusOutput ? statusOutput.closest(".inspector-card") : null;
  const transition = document.querySelector('[data-thread-transition="switching"]');
  const emptyState = document.querySelector(".timeline-empty");
  const threadScroller = document.querySelector("#thread-scroller");
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
    liveActivity: liveActivity ? {
      dataset: { ...liveActivity.dataset },
      text: (liveActivity.textContent || "").trim(),
    } : null,
    follow: follow ? {
      hidden: !!follow.hidden,
      dataset: { ...follow.dataset },
      text: (follow.textContent || "").trim(),
    } : null,
    activeSessionRow: activeSessionRow ? {
      hidden: !!activeSessionRow.hidden,
      dataset: { ...activeSessionRow.dataset },
      text: (activeSessionRow.textContent || "").trim(),
    } : null,
    sessionStrip: sessionStrip ? {
      hidden: !!sessionStrip.hidden,
      dataset: { ...sessionStrip.dataset },
      text: (sessionStrip.textContent || "").trim(),
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
    autonomyDetailCard: autonomyDetailCard ? {
      hidden: !!autonomyDetailCard.hidden,
      dataset: { ...autonomyDetailCard.dataset },
      text: (autonomyDetailCard.textContent || "").trim(),
    } : null,
    autonomyDetail: autonomyDetail ? {
      dataset: { ...autonomyDetail.dataset },
      text: (autonomyDetail.textContent || "").trim(),
    } : null,
    executionStatusCard: executionStatusCard ? {
      hidden: !!executionStatusCard.hidden,
      dataset: { ...executionStatusCard.dataset },
      text: (executionStatusCard.textContent || "").trim(),
    } : null,
    statusOutput: statusOutput ? {
      dataset: { ...statusOutput.dataset },
      text: (statusOutput.textContent || "").trim(),
    } : null,
    transition: transition ? {
      dataset: { ...transition.dataset },
      text: (transition.textContent || "").trim(),
    } : null,
    emptyState: emptyState ? {
      text: (emptyState.textContent || "").trim(),
    } : null,
    threadScroller: threadScroller ? {
      dataset: { ...threadScroller.dataset },
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
  const nativeFetch = window.fetch ? window.fetch.bind(window) : null;
  window.__verifyFetchLog = [];
  window.__verifySseEvents = [];
  window.__verifySseUrls = [];
  window.__verifyAppendLog = [];
  window.__verifyDelayedConversationId = "";
  window.__verifyDelayedConversationConsumed = false;
  window.__verifyConversationDelayMs = 0;
  if (nativeFetch) {
    window.fetch = (...args) => {
      const request = args[0];
      const url = typeof request === "string" ? request : request?.url || "";
      const method = typeof request === "object" && request?.method ? request.method : (args[1]?.method || "GET");
      window.__verifyFetchLog.push({ url, method });
      const delayedConversationId = String(window.__verifyDelayedConversationId || "");
      const shouldDelay =
        delayedConversationId &&
        !window.__verifyDelayedConversationConsumed &&
        url.includes(`/api/conversations/${delayedConversationId}`);
      if (shouldDelay) {
        window.__verifyDelayedConversationConsumed = true;
        return new Promise((resolve, reject) => {
          window.setTimeout(() => {
            nativeFetch(...args).then(resolve).catch(reject);
          }, Number(window.__verifyConversationDelayMs || 0));
        });
      }
      return nativeFetch(...args);
    };
  }
  if (!NativeEventSource) {
    return;
  }
  window.__verifyForceDegrade = false;
  window.__verifyDegraded = false;
  window.__verifyLatestEventSource = null;
  window.__verifyTriggerDisconnect = () => {
    const source = window.__verifyLatestEventSource;
    if (!source) {
      return false;
    }
    try {
      source.close();
      source.dispatchEvent(new Event("error"));
      return true;
    } catch (_) {
      return false;
    }
  };
  window.EventSource = class VerifyEventSource extends NativeEventSource {
    constructor(...args) {
      super(...args);
      this.__verifyUrl = String(args[0] || "");
      window.__verifyLatestEventSource = this;
      window.__verifySseUrls.push(this.__verifyUrl);
      if (window.__verifyForceDegrade) {
        queueMicrotask(() => {
          try {
            this.close();
            this.dispatchEvent(new Event("error"));
          } catch (_) {
            // Let the app retry and eventually fall back.
          }
        });
      }
      this.addEventListener("session.bootstrap", (event) => {
        try {
          window.__verifySseEvents.push({ event: "session.bootstrap", data: JSON.parse(event.data || "{}") });
        } catch (_) {
          window.__verifySseEvents.push({ event: "session.bootstrap", data: {} });
        }
      });
      this.addEventListener("conversation.append", (event) => {
        try {
          const data = JSON.parse(event.data || "{}");
          window.__verifyAppendLog.push({
            conversationId: String(data.conversation_id || ""),
            appendId: Number(data.append_id || 0),
          });
        } catch (_) {
          window.__verifyAppendLog.push({ conversationId: "", appendId: 0 });
        }
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
            page.evaluate("() => { window.__verifyFetchMark = window.__verifyFetchLog.length; window.__verifySseMark = window.__verifySseEvents.length; }")
            page.click(f'[data-conversation-id="{conversation_id}"]')
            page.wait_for_function(
                """([appId, conversationId]) => {
                  const summary = document.querySelector("#session-summary-row");
                  const sendRequest = document.querySelector("#send-request");
                  const sessionStrip = document.querySelector("#session-strip");
                  const threadScroller = document.querySelector("#thread-scroller");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const emptyState = document.querySelector(".timeline-empty");
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const sseMark = Number(window.__verifySseMark || 0);
                  const bootstrapEvents = (window.__verifySseEvents || []).slice(sseMark).filter(
                    item => item.event === "session.bootstrap" && String(item.data?.conversation_id || "") === conversationId
                  );
                  const conversationFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/conversations/${conversationId}`)
                  );
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  const goalsFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/apps/${appId}/goals`)
                  );
                  return Boolean(
                    summary &&
                    sendRequest &&
                    sessionStrip &&
                    sessionStrip.dataset.attachMode === "sse-bootstrap" &&
                    sessionStrip.dataset.bootstrapVersion === "2" &&
                    sessionStrip.dataset.resumeMode === "bootstrap" &&
                    sessionStrip.dataset.resumeCursor === "0" &&
                    threadScroller &&
                    threadScroller.dataset.attachMode === "sse-bootstrap" &&
                    threadScroller.dataset.bootstrapVersion === "2" &&
                    threadScroller.dataset.resumeMode === "bootstrap" &&
                    threadScroller.dataset.resumeCursor === "0" &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    document.querySelector(`[data-conversation-id="${conversationId}"]`) &&
                    bootstrapEvents.length >= 1 &&
                    conversationFetches.length === 0 &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0 &&
                    !emptyState
                  );
                }""",
                [app_id, conversation_id],
                timeout=30000,
            )

            page.fill("#request-text", request_text)
            page.evaluate("() => { window.__verifyFetchMark = window.__verifyFetchLog.length; }")
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
                  const healthyBlock = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-block-owner="selected-thread"][data-live-owned="true"]');
                  const liveActivity = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="true"]');
                  const summary = document.querySelector("#session-summary-row");
                  const liveIndicator = document.querySelector("#session-live-indicator");
                  const summaryCopy = document.querySelector("#session-summary-copy");
                  const threadPhase = document.querySelector("#thread-phase-chip");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const sessionStripDetail = document.querySelector("#session-strip-detail");
                  const stripChips = sessionStripState ? sessionStripState.querySelectorAll(".session-chip") : [];
                  const threadScroller = document.querySelector("#thread-scroller");
                  const composerOwnerRow = document.querySelector("#composer-owner-row");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const sendRequest = document.querySelector("#send-request");
                  const autonomyDetailCard = document.querySelector(".autonomy-detail-card");
                  const autonomyDetail = document.querySelector("#autonomy-detail");
                  const statusOutput = document.querySelector("#status-output");
                  const executionStatusCard = statusOutput ? statusOutput.closest(".inspector-card") : null;
                  const follow = document.querySelector("#jump-to-latest");
                  const sessionEvent = document.querySelector('.timeline-item.session-event[data-append-source="sse"]');
                  const milestoneLane = liveActivity ? liveActivity.querySelector('[data-live-milestones="true"]') : null;
                  const legacyLaneMeta = liveActivity ? liveActivity.querySelector(".session-inline-autonomy-meta") : null;
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  return Boolean(
                    !healthyBlock &&
                    liveActivity &&
                    liveActivity.dataset.liveOwned === "true" &&
                    liveActivity.dataset.liveSessionEvent === "true" &&
                    liveActivity.dataset.liveSessionLane === "selected-thread" &&
                    liveActivity.dataset.liveMilestonesVisible === "true" &&
                    ["EXPECTED", "ACCEPTABLE"].includes(liveActivity.dataset.livePathVerdict || "") &&
                    ["ACCEPTABLE", "PENDING"].includes(liveActivity.dataset.liveVerifierAcceptability || "") &&
                    (liveActivity.dataset.liveBlockerReason || "").length > 0 &&
                    ["PROPOSAL", "REVIEW", "VERIFY", "READY", "APPLIED"].includes(liveActivity.dataset.liveRunPhase || "") &&
                    milestoneLane &&
                    milestoneLane.dataset.liveMilestones === "true" &&
                    milestoneLane.dataset.liveMilestonesPhase === liveActivity.dataset.liveMilestonesPhase &&
                    !legacyLaneMeta &&
                    summary &&
                    summary.hidden &&
                    summary.dataset.summaryPath === "session" &&
                    summary.dataset.liveSessionOwned === "true" &&
                    summary.dataset.footerDockOwned === "true" &&
                    summary.dataset.summaryState === "attached" &&
                    summaryCopy &&
                    summaryCopy.textContent.trim().length > 0 &&
                    !summaryCopy.textContent.includes("OWNER") &&
                    liveIndicator &&
                    liveIndicator.hidden &&
                    liveIndicator.textContent.trim() === "SSE OWNER" &&
                    liveIndicator.dataset.liveSessionOwned === "true" &&
                    liveIndicator.dataset.liveSessionSource === "sse" &&
                    threadPhase &&
                    threadPhase.hidden &&
                    threadPhase.dataset.threadPhase === summary.dataset.summaryPhase &&
                    threadPhase.dataset.threadPhaseDetail &&
                    threadPhase.dataset.threadPhaseDetail !== "idle" &&
                    activeSessionRow &&
                    !activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "true" &&
                    activeSessionRow.dataset.activeSessionSource === "sse" &&
                    ["live", "paused", "new"].includes(activeSessionRow.dataset.activeSessionState || "") &&
                    activeSessionRow.dataset.activeSessionPhase === summary.dataset.summaryPhase &&
                    ["live", "paused", "new"].includes(activeSessionRow.dataset.activeSessionFollow || "") &&
                    activeSessionRow.textContent.includes("OWNER") &&
                    sessionStrip &&
                    !sessionStrip.hidden &&
                    sessionStrip.dataset.liveOwned === "true" &&
                    sessionStrip.dataset.sessionOwner === "selected-thread" &&
                    sessionStrip.dataset.footerDockOwned === "true" &&
                    sessionStrip.dataset.footerDockMilestones === "true" &&
                    sessionStrip.dataset.footerDockPhase === summary.dataset.summaryPhase &&
                    sessionStrip.dataset.footerDockSource === "sse" &&
                    threadScroller &&
                    sessionStrip.dataset.phaseValue === summary.dataset.summaryPhase &&
                    threadScroller.dataset.phaseValue === summary.dataset.summaryPhase &&
                    sessionStripState &&
                    stripChips.length >= 1 &&
                    sessionStripState.dataset.sessionStripRole === "live-dock" &&
                    ["PROPOSAL", "REVIEW", "VERIFY", "READY", "APPLIED", "NEW", "PAUSED"].includes(sessionStripState.dataset.sessionStripLabel || "") &&
                    sessionStripState.textContent.trim().length > 0 &&
                    ["HANDOFF", "PROPOSAL", "REVIEW", "VERIFY", "AUTO APPLY", "READY", "APPLIED", "FAILED", "LIVE", "UNKNOWN"].includes(summary.dataset.summaryPhase || "") &&
                    sessionStripDetail &&
                    sessionStripDetail.textContent.trim().length > 0 &&
                    !sessionStripDetail.textContent.includes("OWNER") &&
                    !sessionStripDetail.textContent.includes("authoritative") &&
                    composerOwnerRow &&
                    composerOwnerRow.hidden &&
                    composerOwnerRow.dataset.composerOwnerMerged === "true" &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    sendRequest &&
                    sendRequest.dataset.composerOwnerState &&
                    autonomyDetailCard &&
                    autonomyDetailCard.hidden &&
                    autonomyDetailCard.dataset.autonomySurface === "center-lane" &&
                    autonomyDetail &&
                    autonomyDetail.dataset.surface === "center-lane" &&
                    executionStatusCard &&
                    executionStatusCard.hidden &&
                    executionStatusCard.dataset.executionSurface === "center-lane" &&
                    statusOutput &&
                    statusOutput.dataset.surface === "center-lane" &&
                    !sessionEvent &&
                    follow &&
                    follow.dataset.followOwned !== undefined &&
                    jobFetches.length === 0
                  );
                }""",
                conversation_id,
                timeout=120000,
            )
            healthy_snapshot = page.evaluate(browser_snapshot_script())

            page.evaluate(
                """() => {
                  const scroller = document.querySelector("#thread-scroller");
                  if (scroller) {
                    scroller.scrollTop = 0;
                    scroller.dispatchEvent(new Event("scroll", { bubbles: true }));
                  }
                }"""
            )
            page.wait_for_function(
                """conversationId => {
                  const follow = document.querySelector("#jump-to-latest");
                  const sessionStripToggle = document.querySelector("#session-strip-toggle");
                  return Boolean(
                    follow &&
                    follow.hidden &&
                    follow.dataset.followOwned === "none" &&
                    follow.dataset.followState === "hidden" &&
                    follow.dataset.followCount === "0" &&
                    sessionStripToggle &&
                    !sessionStripToggle.hidden &&
                    sessionStripToggle.dataset.sessionAction === "jump-latest" &&
                    ["new", "paused"].includes(sessionStripToggle.dataset.followState || "") &&
                    Number(sessionStripToggle.dataset.followCount || "0") >= 0 &&
                    sessionStripToggle.textContent.trim().length > 0
                  );
                }""",
                conversation_id,
                timeout=30000,
            )
            page.click("#session-strip-toggle")
            page.wait_for_function(
                """() => {
                  const follow = document.querySelector("#jump-to-latest");
                  const sessionStripToggle = document.querySelector("#session-strip-toggle");
                  return Boolean(
                    follow &&
                    follow.hidden &&
                    follow.dataset.followOwned === "none" &&
                    follow.dataset.followState === "hidden" &&
                    follow.dataset.followCount === "0" &&
                    follow.dataset.followConversationId === "" &&
                    sessionStripToggle &&
                    sessionStripToggle.hidden &&
                    sessionStripToggle.dataset.sessionAction === "toggle-session-rail" &&
                    sessionStripToggle.dataset.followState === "idle" &&
                    sessionStripToggle.dataset.followCount === "0"
                  );
                }""",
                timeout=30000,
            )

            page.evaluate(
                "() => { window.__verifyFetchMark = window.__verifyFetchLog.length; window.__verifySseMark = window.__verifySseEvents.length; window.__verifyUrlMark = window.__verifySseUrls.length; window.__verifyAppendMark = window.__verifyAppendLog.length; window.__verifyTriggerDisconnect(); }"
            )
            page.wait_for_function(
                """conversationId => {
                  const sessionStrip = document.querySelector("#session-strip");
                  const threadScroller = document.querySelector("#thread-scroller");
                  const summary = document.querySelector("#session-summary-row");
                  const composerOwnerRow = document.querySelector("#composer-owner-row");
                  const healthyBlock = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-block-owner="selected-thread"]');
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const statusOutput = document.querySelector("#status-output");
                  const executionStatusCard = statusOutput ? statusOutput.closest(".inspector-card") : null;
                  const emptyState = document.querySelector(".timeline-empty");
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const sseMark = Number(window.__verifySseMark || 0);
                  const urlMark = Number(window.__verifyUrlMark || 0);
                  const appendMark = Number(window.__verifyAppendMark || 0);
                  const bootstrapEvents = (window.__verifySseEvents || []).slice(sseMark).filter(
                    item => item.event === "session.bootstrap" && String(item.data?.conversation_id || "") === conversationId
                  );
                  const resumeEvents = bootstrapEvents.filter(
                    item => String(item.data?.attach_mode || "") === "sse-resume"
                  );
                  const conversationFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/conversations/${conversationId}`)
                  );
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  const goalsFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/apps/${appId}/goals`)
                  );
                  const resumeUrls = (window.__verifySseUrls || []).slice(urlMark).filter(
                    url => String(url || "").includes(`/api/internal/conversations/${conversationId}/append-stream?after=`)
                  );
                  const appendIds = (window.__verifyAppendLog || []).slice(appendMark).filter(
                    item => String(item.conversationId || "") === conversationId && Number(item.appendId || 0) > 0
                  ).map(item => Number(item.appendId || 0));
                  const deduped = new Set(appendIds);
                  const lastResume = resumeEvents.length ? resumeEvents[resumeEvents.length - 1].data : {};
                  return Boolean(
                    sessionStrip &&
                    sessionStrip.dataset.attachMode === "sse-resume" &&
                    sessionStrip.dataset.bootstrapVersion === "2" &&
                    sessionStrip.dataset.resumeMode === "resumed" &&
                    sessionStrip.dataset.restorePath === "resume" &&
                    sessionStrip.dataset.restoreProvenance === "sse-bootstrap" &&
                    Number(sessionStrip.dataset.resumeCursor || "0") > 0 &&
                    threadScroller &&
                    threadScroller.dataset.attachMode === "sse-resume" &&
                    threadScroller.dataset.bootstrapVersion === "2" &&
                    threadScroller.dataset.resumeMode === "resumed" &&
                    threadScroller.dataset.restorePath === "resume" &&
                    threadScroller.dataset.restoreProvenance === "sse-bootstrap" &&
                    Number(threadScroller.dataset.resumeCursor || "0") > 0 &&
                    summary &&
                    !summary.hidden &&
                    summary.dataset.restorePath === "resume" &&
                    summary.dataset.restoreProvenance === "sse-bootstrap" &&
                    summary.dataset.restoreStage === "none" &&
                    composerOwnerRow &&
                    composerOwnerRow.dataset.composerRestoreStage === "none" &&
                    liveActivity &&
                    executionStatusCard &&
                    executionStatusCard.hidden &&
                    executionStatusCard.dataset.executionSurface === "center-lane" &&
                    statusOutput &&
                    statusOutput.dataset.surface === "center-lane" &&
                    sessionStrip.dataset.phaseValue === liveActivity.dataset.liveRunPhase &&
                    sessionStrip.dataset.phaseProvenance === liveActivity.dataset.liveRunSource &&
                    threadScroller.dataset.phaseValue === liveActivity.dataset.liveRunPhase &&
                    threadScroller.dataset.phaseProvenance === liveActivity.dataset.liveRunSource &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    resumeEvents.length >= 1 &&
                    Number(lastResume.resume_from_append_id || 0) > 0 &&
                    resumeUrls.length >= 1 &&
                    conversationFetches.length === 0 &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0 &&
                    appendIds.length === deduped.size &&
                    !emptyState
                  );
                }""",
                [app_id, conversation_id],
                timeout=30000,
            )
            resume_snapshot = page.evaluate(browser_snapshot_script())

            page.evaluate("() => { window.__verifyForceDegrade = true; window.__verifyTriggerDisconnect(); }")
            page.wait_for_function(
                """() => {
                  const degraded = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="false"]');
                  const healthy = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="true"]');
                  const healthyBlock = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-owned="true"]');
                  const summary = document.querySelector("#session-summary-row");
                  const liveIndicator = document.querySelector("#session-live-indicator");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const statusOutput = document.querySelector("#status-output");
                  const executionStatusCard = statusOutput ? statusOutput.closest(".inspector-card") : null;
                  const follow = document.querySelector("#jump-to-latest");
                  const stripChips = sessionStripState ? sessionStripState.querySelectorAll(".session-chip") : [];
                  if (!degraded || healthy || healthyBlock || !summary || !follow || !activeSessionRow || !sessionStrip || !sessionStripState || !executionStatusCard || !statusOutput) {
                    return false;
                  }
                  const reason = degraded.dataset.liveReason || "";
                  const phase = degraded.dataset.liveRunPhase || "";
                  return (
                    ["retrying", "reconnecting", "polling-fallback", "session-rotation"].includes(reason) &&
                    ["RECONNECT", "POLLING"].includes(phase) &&
                    !summary.hidden &&
                    summary.dataset.summaryPath === "degraded" &&
                    summary.dataset.liveSessionOwned === "false" &&
                    liveIndicator &&
                    liveIndicator.hidden &&
                    ["RECONNECT", "POLLING"].includes(liveIndicator.textContent.trim()) &&
                    liveIndicator.dataset.liveSessionOwned === "false" &&
                    activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "none" &&
                    !sessionStrip.hidden &&
                    stripChips.length === 1 &&
                    sessionStripState.dataset.sessionStripRole === "degraded" &&
                    sessionStripState.dataset.sessionStripLabel === phase &&
                    sessionStripState.textContent.trim() === phase &&
                    ["reconnect", "polling"].includes(sessionStrip.dataset.composerTransport || "") &&
                    sessionStrip.dataset.composerTransportOwned === "false" &&
                    !executionStatusCard.hidden &&
                    executionStatusCard.dataset.executionSurface === "secondary-detail" &&
                    statusOutput.dataset.surface === "secondary-detail" &&
                    sessionStrip.dataset.composerTransport !== "sse-owner" &&
                    follow.dataset.followOwned !== "selected-thread"
                  );
                }""",
                timeout=120000,
            )
            degraded_snapshot = page.evaluate(browser_snapshot_script())

            page.evaluate("() => { window.__verifyFetchMark = window.__verifyFetchLog.length; }")
            page.click(f'[data-conversation-id="{switch_conversation_id}"]')
            page.wait_for_function(
                """([appId, targetConversationId]) => {
                  const transition = document.querySelector('[data-thread-transition="switching"]');
                  const summary = document.querySelector("#session-summary-row");
                  const liveIndicator = document.querySelector("#session-live-indicator");
                  const threadTitle = document.querySelector("#thread-title");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const sendRequest = document.querySelector("#send-request");
                  const composerOwnerRow = document.querySelector("#composer-owner-row");
                  const threadScroller = document.querySelector("#thread-scroller");
                  const healthyBlock = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-owned="true"]');
                  const healthy = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="true"]');
                  const degraded = document.querySelector('.session-inline-block[data-selected-thread-degraded-block="true"]');
                  const empty = document.querySelector(".timeline-empty");
                  const follow = document.querySelector("#jump-to-latest");
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  const goalsFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/apps/${appId}/goals`)
                  );
                  return Boolean(
                    transition &&
                    document.querySelectorAll('[data-thread-transition="switching"]').length === 1 &&
                    transition.dataset.threadTransitionPhase === "switching" &&
                    transition.dataset.threadTransitionSource === "selected-thread-session" &&
                    transition.dataset.threadTransitionOwnerCleared === "true" &&
                    transition.dataset.threadTransitionConversationId === targetConversationId &&
                    summary &&
                    summary.hidden &&
                    summary.dataset.liveSessionOwned === "false" &&
                    liveIndicator &&
                    liveIndicator.hidden &&
                    liveIndicator.dataset.liveSessionOwned === "false" &&
                    threadTitle &&
                    threadTitle.textContent.trim().length > 0 &&
                    threadTitle.textContent.trim() !== "새 대화를 시작하세요" &&
                    activeSessionRow &&
                    activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "none" &&
                    activeSessionRow.dataset.activeSessionState === "idle" &&
                    activeSessionRow.dataset.activeSessionPhase === "IDLE" &&
                    activeSessionRow.dataset.activeSessionConversationId === "" &&
                    activeSessionRow.dataset.activeSessionFollow === "idle" &&
                    sessionStrip &&
                    !sessionStrip.hidden &&
                    sessionStripState &&
                    sessionStripState.querySelectorAll(".session-chip").length === 1 &&
                    sessionStripState.dataset.sessionStripRole === "transition" &&
                    sessionStripState.dataset.sessionStripLabel === "SWITCHING" &&
                    sessionStripState.textContent.trim() === "SWITCHING" &&
                    sessionStrip.dataset.composerState === "switching" &&
                    sessionStrip.dataset.composerTransport === "attach" &&
                    sessionStrip.dataset.composerTargetConversationId === targetConversationId &&
                    sessionStrip.dataset.phaseValue === "UNKNOWN" &&
                    sessionStrip.dataset.phaseAuthoritative === "false" &&
                    sessionStrip.dataset.phaseProvenance === "thread-transition" &&
                    composerOwnerRow &&
                    composerOwnerRow.hidden &&
                    composerOwnerRow.dataset.composerOwnerMerged === "true" &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    sendRequest &&
                    sendRequest.dataset.composerOwnerState === "switching" &&
                    threadScroller &&
                    threadScroller.dataset.threadTransitionState === "switching" &&
                    threadScroller.dataset.threadTransitionConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspacePlaceholder === "switching" &&
                    document.querySelector("#conversation-timeline").dataset.workspaceConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.phaseValue === "UNKNOWN" &&
                    threadScroller.dataset.phaseAuthoritative === "false" &&
                    threadScroller.dataset.phaseProvenance === "thread-transition" &&
                    threadScroller.dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.sessionOwner !== "selected-thread" &&
                    follow &&
                    follow.dataset.followOwned !== "selected-thread" &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0 &&
                    !healthyBlock &&
                    !healthy &&
                    !degraded &&
                    !empty
                  );
                }""",
                [app_id, switch_conversation_id],
                timeout=30000,
            )
            switch_snapshot = page.evaluate(browser_snapshot_script())

            page.evaluate(
                """switchConversationId => {
                  window.__verifyDelayedConversationId = String(switchConversationId || "");
                  window.__verifyDelayedConversationConsumed = false;
                  window.__verifyConversationDelayMs = 800;
                  window.__verifyFetchMark = window.__verifyFetchLog.length;
                }""",
                switch_conversation_id,
            )
            page.click(f'[data-conversation-id="{switch_conversation_id}"]')
            page.wait_for_function(
                """targetConversationId => {
                  const transition = document.querySelector('[data-thread-transition="switching"]');
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const threadScroller = document.querySelector("#thread-scroller");
                  const empty = document.querySelector(".timeline-empty");
                  return Boolean(
                    transition &&
                    document.querySelectorAll('[data-thread-transition="switching"]').length === 1 &&
                    transition.dataset.threadTransitionOwnerCleared === "true" &&
                    transition.dataset.threadTransitionConversationId === targetConversationId &&
                    activeSessionRow &&
                    activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "none" &&
                    activeSessionRow.dataset.activeSessionState === "idle" &&
                    activeSessionRow.dataset.activeSessionPhase === "IDLE" &&
                    activeSessionRow.dataset.activeSessionConversationId === "" &&
                    activeSessionRow.dataset.activeSessionFollow === "idle" &&
                    sessionStrip &&
                    sessionStripState &&
                    sessionStripState.querySelectorAll(".session-chip").length === 1 &&
                    sessionStripState.dataset.sessionStripRole === "transition" &&
                    sessionStripState.dataset.sessionStripLabel === "SWITCHING" &&
                    sessionStripState.textContent.trim() === "SWITCHING" &&
                    sessionStrip.dataset.composerState === "switching" &&
                    sessionStrip.dataset.composerTargetConversationId === targetConversationId &&
                    threadScroller &&
                    threadScroller.dataset.threadTransitionState === "switching" &&
                    threadScroller.dataset.threadTransitionConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspacePlaceholder === "switching" &&
                    document.querySelector("#conversation-timeline").dataset.workspaceConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.workspaceOwnerCleared === "true" &&
                    !empty
                  );
                }""",
                switch_conversation_id,
                timeout=30000,
            )
            page.evaluate("() => { window.__verifyFetchMark = window.__verifyFetchLog.length; }")
            page.click(f'[data-conversation-id="{conversation_id}"]')
            page.wait_for_function(
                """([appId, targetConversationId]) => {
                  const transition = document.querySelector('[data-thread-transition="switching"]');
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const threadScroller = document.querySelector("#thread-scroller");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const summary = document.querySelector("#session-summary-row");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const follow = document.querySelector("#jump-to-latest");
                  const empty = document.querySelector(".timeline-empty");
                  const healthyBlock = document.querySelector('.session-inline-block[data-selected-thread-live-block="true"][data-live-owned="true"]');
                  const degraded = document.querySelector('.session-inline-block[data-selected-thread-degraded-block="true"]');
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  const goalsFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/apps/${appId}/goals`)
                  );
                  return Boolean(
                    transition &&
                    document.querySelectorAll('[data-thread-transition="switching"]').length === 1 &&
                    transition.dataset.threadTransitionOwnerCleared === "true" &&
                    transition.dataset.threadTransitionConversationId === targetConversationId &&
                    sessionStrip &&
                    !sessionStrip.hidden &&
                    sessionStripState &&
                    sessionStripState.querySelectorAll(".session-chip").length === 1 &&
                    sessionStripState.dataset.sessionStripRole === "transition" &&
                    sessionStripState.dataset.sessionStripLabel === "SWITCHING" &&
                    sessionStripState.textContent.trim() === "SWITCHING" &&
                    sessionStrip.dataset.composerState === "switching" &&
                    sessionStrip.dataset.composerTargetConversationId === targetConversationId &&
                    sessionStrip.dataset.phaseValue === "UNKNOWN" &&
                    sessionStrip.dataset.phaseAuthoritative === "false" &&
                    sessionStrip.dataset.phaseProvenance === "thread-transition" &&
                    threadScroller &&
                    threadScroller.dataset.threadTransitionState === "switching" &&
                    threadScroller.dataset.threadTransitionConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspacePlaceholder === "switching" &&
                    document.querySelector("#conversation-timeline").dataset.workspaceConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.sessionOwner !== "selected-thread" &&
                    summary &&
                    summary.dataset.liveSessionOwned === "false" &&
                    activeSessionRow &&
                    activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "none" &&
                    activeSessionRow.dataset.activeSessionState === "idle" &&
                    activeSessionRow.dataset.activeSessionPhase === "IDLE" &&
                    activeSessionRow.dataset.activeSessionConversationId === "" &&
                    activeSessionRow.dataset.activeSessionFollow === "idle" &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    follow &&
                    follow.dataset.followOwned !== "selected-thread" &&
                    !healthyBlock &&
                    !degraded &&
                    !empty &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0
                  );
                }""",
                [app_id, conversation_id],
                timeout=30000,
            )
            cancelled_switch_snapshot = page.evaluate(browser_snapshot_script())
            return {
                "job_id": job_id,
                "healthy": healthy_snapshot,
                "resume": resume_snapshot,
                "degraded": degraded_snapshot,
                "switch": switch_snapshot,
                "switch_cancelled": cancelled_switch_snapshot,
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
    app_js = http_text(parse.urljoin(ops_url, "app.js"), api_key=api_key)
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
    require(html, 'data-composer-utility-open="false"', label="composer utility default collapsed dataset")
    require(html, 'data-composer-utility-state="closed"', label="composer utility default closed dataset")
    require(html, 'aria-controls="composer-utility-cluster"', label="composer utility toggle controls")
    require(html, 'aria-hidden="true"', label="composer utility default aria-hidden")
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
    require(app_js, "setComposerUtilityOpen", label="composer utility state helper")
    require(app_js, 'const utilityOpen = isOpen ? "true" : "false";', label="composer utility finite open helper")
    require(app_js, 'const utilityState = isOpen ? "open" : "closed";', label="composer utility finite state helper")
    require(app_js, 'dom.composerUtilityMenu.dataset.composerUtilityState = utilityState;', label="composer utility menu state sync")
    require(app_js, 'dom.composerUtilityCluster.dataset.composerUtilityState = utilityState;', label="composer utility cluster state sync")
    require(app_js, 'dom.composerUtilityCluster.setAttribute("aria-hidden", isOpen ? "false" : "true");', label="composer utility cluster aria sync")
    require(app_js, 'dom.composerUtilityToggle.dataset.composerUtilityState = utilityState;', label="composer utility toggle state sync")
    require(app_js, 'dom.composerUtilityToggle.setAttribute("aria-expanded", utilityOpen);', label="composer utility toggle aria sync")
    require(app_js, 'persistSettings();\n  setComposerUtilityOpen(false);\n  dom.sendRequestButton.dataset.sendBusy = "true";', label="composer utility closes on send transition")
    require(app_js, 'dom.appSelect.addEventListener("change", async () => {\n    setComposerUtilityOpen(false);', label="composer utility closes on app change")
    require(app_js, 'dom.newConversationButton.addEventListener("click", async () => {\n    setComposerUtilityOpen(false);', label="composer utility closes on new conversation")
    require(app_js, 'setComposerUtilityOpen(false);\n    state.savedConversationId = button.dataset.conversationId || "";\n    await conversationController.handleConversationChange();', label="composer utility closes on selected-thread change")
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
    require(styles, ".autonomy-detail-card", label="secondary panel autonomy detail card CSS")
    require(styles, ".session-inline-block", label="inline session block CSS")
    require(styles, ".session-inline-autonomy", label="inline autonomy row CSS")
    require(styles, ".timeline-item.session-event", label="session timeline event CSS")
    require(styles, '.timeline-item.session-event[data-session-verdict="disqualifying"]', label="session timeline disqualifying CSS")
    require(styles, ".timeline-transition", label="thread transition CSS")
    require(styles, '.session-strip[data-stream-state="reconnecting"]', label="reconnecting session strip CSS")
    require(styles, '.session-strip[data-stream-state="offline"]', label="offline session strip CSS")
    require(styles, '.session-strip[data-stream-state="connecting"]', label="connecting session strip CSS")

    require(render_js, "renderSessionSummary", label="session summary helper")
    require(render_js, "selectedThreadLiveSessionIndicator", label="session live indicator helper")
    require(conversations_js, "bootstrapAutonomySummary", label="bootstrap autonomy authority helper")
    require(conversations_js, 'freshnessState: bootstrapAutonomy ? "fresh" : "stale-or-missing"', label="bootstrap autonomy freshness authority")
    require(conversations_js, "fallbackAllowed: !bootstrapAutonomy", label="bootstrap autonomy fallback gate")
    require(conversations_js, 'source: authoritativeBootstrapAutonomy ? "session-bootstrap" : "conversation-snapshot"', label="conversation fetch bootstrap authority precedence")
    require(conversations_js, "if (shouldAllowGoalsPollingFallback({ conversationId: conversation.conversation_id })) {", label="conversation fetch goals fallback guard")
    require(render_js, "latestSessionIndicatorEvent", label="session live indicator event helper")
    require(render_js, "composerOwnerState", label="composer owner state helper")
    require(render_js, "composerTransportState", label="composer transport state helper")
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
    require(render_js, "syncExecutionStatusSurface", label="execution status surface helper")
    require(render_js, 'statusCard.hidden = promoteToCenterLane;', label="execution card hidden helper")
    require(render_js, 'statusCard.dataset.executionSurface = promoteToCenterLane ? "center-lane" : "secondary-detail";', label="execution card surface dataset")
    require(render_js, 'dom.statusOutput.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";', label="status output surface dataset")
    require(render_js, 'dom.jobEvents.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";', label="job events surface dataset")
    require(render_js, 'dom.jobPhase.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";', label="job phase surface dataset")
    require(render_js, 'dom.jobMeta.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";', label="job meta surface dataset")
    require(render_js, "if (inlineState.visible) {", label="composer strip suppression guard")
    require(render_js, "renderInlineSessionBlock", label="inline session block helper")
    require(render_js, "INLINE_TERMINAL_RETENTION_MS = 12000", label="inline terminal retention window")
    require(render_js, "shouldRetainInlineTerminalPhase", label="inline terminal retention helper")
    require(render_js, "renderThreadTransition", label="thread transition helper")
    require(render_js, "function renderThreadTransition(currentState, sessionStatus = deriveSelectedThreadSessionStatus(currentState, null))", label="thread transition canonical status signature")
    require(render_js, "pendingHandoffState", label="pending handoff helper")
    require(render_js, 'data-thread-transition="switching"', label="thread transition DOM")
    require(render_js, 'data-thread-transition-source="selected-thread-session"', label="thread transition source dataset")
    require(render_js, 'data-thread-transition-phase="switching"', label="thread transition phase dataset")
    require(render_js, 'data-thread-transition-owner-cleared="true"', label="thread transition ownership-cleared dataset")
    require(render_js, 'data-thread-transition-owner-cleared="true"', label="thread transition ownership-cleared dataset")
    require(render_js, "selectedThreadWorkspacePlaceholder", label="thread transition workspace placeholder helper")
    require(render_js, "const workspacePlaceholder = selectedThreadWorkspacePlaceholder(currentState);", label="thread transition workspace placeholder state")
    require(render_js, 'workspaceSummary: "selected thread switching · target snapshot attach pending",', label="switch workspace summary copy")
    require(render_js, 'workspaceSummary: sessionStatus.restoreResume', label="restore workspace summary copy")
    require(render_js, 'workspaceSummary: "선택된 대화가 없으면 현재 세션 맥락이 여기에 정리됩니다.",', label="empty workspace summary copy")
    require(render_js, 'dom.conversationTimeline.dataset.workspacePlaceholder = workspacePlaceholder.mode;', label="workspace placeholder mode dataset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceConversationId = workspacePlaceholder.conversationId;', label="workspace placeholder conversation dataset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = isThreadTransition ? "true" : "false";', label="workspace placeholder ownership-cleared dataset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = isThreadTransition ? "true" : "false";', label="workspace placeholder ownership-cleared dataset")
    require(render_js, 'dom.conversationTimeline.innerHTML = workspacePlaceholder.timeline;', label="thread transition placeholder render path")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholder = workspacePlaceholder.mode;', label="thread scroller placeholder mode dataset")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholderConversationId = workspacePlaceholder.conversationId;', label="thread scroller placeholder conversation dataset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = isThreadTransition ? "true" : "false";', label="thread scroller ownership-cleared dataset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = isThreadTransition ? "true" : "false";', label="thread scroller ownership-cleared dataset")
    require(render_js, 'data-thread-transition-conversation-id="${escapeHtml(String(sessionStatus.switchConversationId || sessionStatus.targetConversationId || ""))}"', label="thread transition canonical conversation dataset")
    require(render_js, 'mode: "switching"', label="switch workspace placeholder mode")
    require(render_js, 'mode: "restore"', label="restore workspace placeholder mode")
    require(render_js, 'mode: "empty"', label="empty workspace placeholder mode")
    require(render_js, "timeline: renderThreadTransition(currentState, sessionStatus),", label="switch workspace timeline")
    require(render_js, 'timeline: \'<p class="timeline-empty">새 대화를 만들면 요청과 이벤트가 여기 쌓입니다.</p>\',', label="true empty workspace timeline")
    require(render_js, 'threadTitle: workspacePlaceholder.title,', label="thread transition or restore title copy")
    require(render_js, 'conversationState: workspacePlaceholder.conversationState,', label="thread transition or restore conversation state copy")
    require(render_js, 'liveRun: workspacePlaceholder.liveRun,', label="thread transition or restore neutral phase")
    require(render_js, "renderWorkspaceSummary(dom, workspacePlaceholder.workspaceSummary);", label="workspace placeholder summary render path")
    require(render_js, "dataset.threadTransitionState", label="thread transition state dataset")
    require(render_js, 'renderSessionStrip(dom, currentState, null);', label="thread transition composer shell render path")
    require(render_js, 'syncComposerOwnership(dom, currentState, null);', label="thread transition composer owner switching path")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholder = "conversation";', label="conversation scroller placeholder reset")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholderConversationId = String(conversation.conversation_id || "");', label="conversation scroller placeholder conversation reset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = "false";', label="conversation workspace ownership-cleared reset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = "false";', label="conversation scroller ownership-cleared reset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = "false";', label="conversation workspace ownership-cleared reset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = "false";', label="conversation scroller ownership-cleared reset")
    require(render_js, "const { handoffVisible, degradedVisible, sessionIndicator } = inlineState;", label="transcript live state wiring")
    require(render_js, 'return "";', label="inline session block removed as primary live surface")
    require(render_js, 'data-live-autonomy="true"', label="inline autonomy DOM")
    require(render_js, 'data-autonomy-path-verdict="', label="inline autonomy path verdict dataset")
    require(render_js, 'data-autonomy-verifier-acceptability="', label="inline autonomy verifier dataset")
    require(render_js, 'data-autonomy-blocker-reason="', label="inline autonomy blocker dataset")
    require(render_js, 'data-autonomy-iteration="', label="inline autonomy iteration dataset")
    require(render_js, 'data-autonomy-source="', label="inline autonomy source dataset")
    require(render_js, 'data-autonomy-freshness-state="', label="inline autonomy freshness dataset")
    require(render_js, 'data-autonomy-fallback-allowed="', label="inline autonomy fallback dataset")
    require(render_js, 'data-autonomy-generated-at="', label="inline autonomy generated-at dataset")
    require(render_js, 'data-live-reason="${escapeHtml(', label="transcript live reason dataset")
    require(render_js, 'const retainedTerminalVisible = shouldRetainInlineTerminalPhase(', label="inline terminal retention wiring")
    require(render_js, '(!liveRun.terminal || retainedTerminalVisible);', label="inline terminal visibility guard")
    require(render_js, 'Date.now() - createdAtMs <= INLINE_TERMINAL_RETENTION_MS;', label="inline terminal retention deadline")
    require(render_js, "(liveRun.phase !== \"READY\" && liveRun.phase !== \"APPLIED\")", label="inline terminal phase scope")
    require(render_js, "latestAppendId > terminalAppendId", label="inline terminal next-append clear guard")
    require(render_js, "dataset.liveRunPhase", label="phase dataset")
    require(render_js, "dataset.liveRunSource", label="live run source dataset")
    require(render_js, "dataset.streamState", label="stream state dataset")
    require(render_js, "dataset.attachMode", label="attach mode dataset")
    require(render_js, "dataset.bootstrapVersion", label="bootstrap version dataset")
    require(render_js, "dataset.resumeMode", label="resume mode dataset")
    require(render_js, "dataset.resumeCursor", label="resume cursor dataset")
    require(render_js, "dataset.phaseValue", label="phase value dataset")
    require(render_js, "dataset.phaseAuthoritative", label="phase authoritative dataset")
    require(render_js, "dataset.phaseProvenance", label="phase provenance dataset")
    require(render_js, 'ownerState.state === "switching" ? "UNKNOWN"', label="switching phase value reset")
    require(render_js, '"thread-transition"', label="switching phase provenance")
    require(render_js, "dataset.sessionOwner", label="session owner dataset")
    require(render_js, "dataset.liveOwned", label="live ownership dataset")
    require(render_js, "dataset.composerOwnerState", label="composer owner state dataset")
    require(render_js, 'dom.sessionStrip.dataset.composerState = ownerState.state;', label="composer strip state dataset")
    require(render_js, 'dom.sessionStrip.dataset.composerTransport = transportState.key;', label="composer strip transport dataset")
    require(render_js, 'dom.sessionStrip.dataset.composerTransportSource = transportState.source;', label="composer strip transport source dataset")
    require(render_js, 'dom.sessionStrip.dataset.composerTransportOwned = stripLiveOwned ? "true" : "false";', label="composer strip transport ownership dataset")
    require(render_js, 'dom.sessionStrip.dataset.composerTransportReason = transportState.reason;', label="composer strip transport reason dataset")
    require(render_js, 'dom.sessionStrip.dataset.composerTargetConversationId = ownerState.conversationId;', label="composer strip target dataset")
    require(render_js, 'dom.sessionStrip.dataset.restoreStage = sessionStatus.restoreStage || "none";', label="composer strip restore stage dataset")
    require(render_js, 'dom.sessionStrip.dataset.restorePath = sessionStatus.restorePath || "none";', label="composer strip restore path dataset")
    require(render_js, 'dom.sessionStrip.dataset.restoreProvenance = sessionStatus.restoreProvenance || "none";', label="composer strip restore provenance dataset")
    require(render_js, 'dom.threadScroller.dataset.restoreStage = sessionStatus.restoreStage || "none";', label="thread scroller restore stage dataset")
    require(render_js, 'dom.threadScroller.dataset.restorePath = sessionStatus.restorePath || "none";', label="thread scroller restore path dataset")
    require(render_js, 'dom.threadScroller.dataset.restoreProvenance = sessionStatus.restoreProvenance || "none";', label="thread scroller restore provenance dataset")
    require(render_js, 'dom.composerOwnerRow.dataset.composerRestoreStage = owner.state === "restore" ? (owner.label === "RESUME" ? "resume-pending" : "attach-pending") : "none";', label="composer owner restore stage dataset")
    require(render_js, 'dom.sessionSummaryRow.dataset.restoreStage = sessionStatus.restoreStage || "none";', label="session summary restore stage dataset")
    require(render_js, 'dom.sessionSummaryRow.dataset.restorePath = sessionStatus.restorePath || "none";', label="session summary restore path dataset")
    require(render_js, 'dom.sessionSummaryRow.dataset.restoreProvenance = sessionStatus.restoreProvenance || "none";', label="session summary restore provenance dataset")
    require(render_js, 'dom.sessionSummaryRow.dataset.footerDockOwned = footerDockOwnsLive ? "true" : "false";', label="header footer-dock ownership dataset")
    require(render_js, 'dom.sessionSummaryRow.hidden = !headerSummaryVisible || footerDockOwnsLive;', label="header summary row visibility")
    require(render_js, 'label: "ATTACH"', label="composer strip attach label")
    require(render_js, 'label: "SNAPSHOT"', label="composer strip snapshot label")
    require(store_js, 'transportLabel = "POLLING";', label="composer strip polling label")
    require(store_js, 'transportLabel = "RECONNECT";', label="composer strip reconnect label")
    require(render_js, "dataset.followState", label="follow-state dataset")
    require(render_js, "function isSessionAuthorityEvent(event)", label="selected-thread session authority event helper")
    require(render_js, "function selectedThreadSseAuthorityEvent(conversation, currentState)", label="selected-thread SSE authority event selector")
    require(render_js, "function sessionAuthorityJobId(conversation, currentState)", label="selected-thread authority job id helper")
    require(render_js, "function sessionAuthorityEvents(conversation, currentState)", label="selected-thread authority event filter helper")
    require(render_js, "export function renderJobActivity(dom, conversation, currentJobId, jobPayload = null, currentState = null)", label="job activity current-state signature")
    require(render_js, "const selectedThreadSseOwned =", label="job activity selected-thread SSE ownership guard")
    require(render_js, "const liveRun = currentState ? deriveLiveRunState(conversation, currentState)", label="job activity live-run ownership source")
    require(render_js, "const liveAuthorityEvent = selectedThreadSseAuthorityEvent(conversation, currentState);", label="selected-thread authority event lookup")
    require(render_js, "const jobId = sessionAuthorityJobId(conversation, currentState);", label="live run session authority job id")
    require(render_js, "const relevantEvents = sessionAuthorityEvents(conversation, currentState);", label="live run session authority event filter")
    require(render_js, "const phase = selectedThreadSseOwned", label="job activity phase ownership switch")
    require(render_js, 'String(liveRun.phase || "IDLE").toUpperCase()', label="job activity SSE phase label")
    require(render_js, 'phaseLabel(jobPayload?.status || latestEvent?.status || "", latestEvent?.type || "")', label="job activity polling fallback phase label")
    require(render_js, "currentState.latestProposalJobId =", label="apply readiness from selected-thread live state")
    require(render_js, "updateProposalButton(dom, currentState.latestProposalJobId);", label="apply button updated from selected-thread live state")
    require(render_js, "dataset.liveSessionState", label="live-session state dataset")
    require(render_js, "dataset.liveSessionSource", label="live-session source dataset")
    require(render_js, "dataset.liveSessionReason", label="live-session reason dataset")
    require(render_js, "dataset.liveSessionOwned", label="live-session owned dataset")
    require(render_js, "renderRestoreSessionTimeline", label="restore transcript timeline helper")
    require(render_js, 'data-live-restore="true"', label="restore transcript marker dataset")
    require(render_js, 'data-live-restore-stage="${escapeHtml(String(sessionStatus.restoreStage || "none"))}"', label="restore transcript stage dataset")
    require(render_js, 'data-live-restore-path="${escapeHtml(String(sessionStatus.restorePath || "none"))}"', label="restore transcript path dataset")
    require(render_js, 'data-live-restore-provenance="${escapeHtml(String(sessionStatus.restoreProvenance || "none"))}"', label="restore transcript provenance dataset")
    require(render_js, "syncAutonomyDetailSurface", label="secondary autonomy surface sync helper")
    require(render_js, "deriveSelectedThreadLiveAutonomy", label="selected-thread live autonomy render helper import")
    require(render_js, 'autonomyCard.hidden = hideForSelectedThreadLiveAutonomy;', label="selected-thread live autonomy card suppression")
    require(render_js, 'autonomyCard.dataset.autonomySurface = hideForSelectedThreadLiveAutonomy ? "center-lane" : "secondary-detail";', label="autonomy card surface dataset")
    require(render_js, 'dom.autonomyDetail.dataset.surface = hideForSelectedThreadLiveAutonomy ? "center-lane" : "secondary-detail";', label="autonomy detail surface dataset")
    require(render_js, 'dom.sessionLiveIndicator.dataset.liveSessionSource = sessionIndicator.source;', label="header indicator source dataset")
    require(render_js, 'dom.sessionLiveIndicator.dataset.liveSessionOwned = sessionIndicator.owned ? "true" : "false";', label="header indicator ownership dataset")
    require(render_js, 'dom.sessionLiveIndicator.dataset.liveSessionReason = sessionIndicator.reason;', label="header indicator reason dataset")
    require(render_js, 'label: sessionStatus.transportLabel || "SSE OWNER"', label="live-session healthy ownership label")
    require(store_js, 'transportLabel = "RECONNECT";', label="live-session reconnect label")
    require(store_js, 'transportLabel = "POLLING";', label="live-session polling label")
    require(render_js, "joinSessionChromeTokens", label="session chrome token join helper")
    require(render_js, "sessionFollowLabel", label="session follow token helper")
    require(render_js, "proposalStatusLabel", label="session proposal status token helper")
    require(render_js, "sessionChromeCopy", label="session summary chrome copy helper")
    require(render_js, "sessionStripDetailCopy", label="session strip detail copy helper")
    require(render_js, "sessionStripStateChipMarkup", label="session strip chip markup helper")
    require(render_js, "sessionStripStateRow", label="session strip single-row state helper")
    require(render_js, "selectedThreadFooterDockModel", label="footer session dock helper")
    require(render_js, 'copy: "ATTACH"', label="composer switching compact copy")
    require(render_js, 'pendingOutgoing.status === "sending-user"', label="composer sending compact copy guard")
    require(render_js, '? "SEND"', label="composer sending compact copy")
    require(render_js, ': "FIRST"', label="composer accepted compact copy")
    require(render_js, 'copy: "OWNER"', label="composer ready compact copy")
    require(render_js, 'copy: "SELECT"', label="composer idle compact copy")
    require(render_js, "phaseDetailCopy", label="phase detail copy helper")
    require(render_js, "compactPhaseDetailCopy", label="compact phase detail copy helper")
    require(render_js, 'dom.threadPhaseChip.dataset.threadPhaseDetail = liveRun?.visible ? phaseDetailCopy(liveRun) : "idle";', label="thread phase detail dataset")
    require(render_js, 'dom.threadPhaseChip.title = liveRun?.visible ? phaseDetailCopy(liveRun) : "현재 활성 세션이 없습니다.";', label="thread phase detail title")
    require(render_js, "return target;", label="summary or composer compact target copy")
    require(render_js, 'return joinSessionChromeTokens(target, stateLabel, "DEGRADED");', label="summary degraded token copy")
    require(render_js, 'type === "codex.exec.retrying"', label="live-session retry degradation mapping")
    require(render_js, "isAppendStreamAuthoritative(currentState, conversationId)", label="selected-thread authoritative SSE handoff guard")
    require(render_js, "const liveVisible =", label="inline live visibility guard")
    require(render_js, 'visible: liveVisible || degradedVisible,', label="inline block excludes handoff duplication")
    require(render_js, 'if (!conversationId && !(threadTransition.active && threadTransition.targetConversationId)) {', label="composer strip idle clear branch")
    require(render_js, 'const ownerState = composerOwnerState(currentState, conversation);', label="composer strip owner helper wiring")
    require(render_js, 'const transportState = composerTransportState(currentState, conversation, liveRun, handoffState);', label="composer strip transport helper wiring")
    require(render_js, "const proposalState = proposalChip(liveRun);", label="composer strip proposal chip helper wiring")
    require(render_js, "const liveOwned =", label="composer strip ownership decoupled from strip visibility")
    require(render_js, 'const footerDock = selectedThreadFooterDockModel(currentState, conversation, liveRun, footerFollow);', label="composer strip footer dock helper wiring")
    require(render_js, 'dom.sessionStrip.hidden = !sessionConversationId ? true : false;', label="composer strip selected-target visibility")
    require(render_js, 'dom.sessionStrip.dataset.sessionOwner = stripLiveOwned ? "selected-thread" : "none";', label="composer strip selected-thread owner dataset")
    require(render_js, 'dom.sessionStrip.dataset.followState = footerFollow.visible ? footerFollow.followState : stripLiveOwned ? sessionStatus.followState || "live" : transportState.owned ? "owned" : "idle";', label="composer strip follow-state dataset")
    require(render_js, 'dom.sessionStrip.dataset.followCount = String(footerFollow.visible ? footerFollow.unseenCount : 0);', label="composer strip follow-count dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockOwned = stripLiveOwned ? "true" : "false";', label="composer strip footer-dock ownership dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockPhase = footerDock.phaseLabel || "IDLE";', label="composer strip footer-dock phase dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockSource = footerDock.source || "none";', label="composer strip footer-dock source dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockMilestones = footerDock.visible ? "true" : "false";', label="composer strip footer-dock milestone dataset")
    require(render_js, 'dom.sessionStripState.dataset.sessionStripRole = stripState.role;', label="composer strip state role dataset")
    require(render_js, 'dom.sessionStripState.dataset.sessionStripLabel = stripState.label;', label="composer strip state label dataset")
    require(render_js, 'dom.sessionStripState.dataset.sessionStripTone = stripState.tone;', label="composer strip state tone dataset")
    require(render_js, 'dom.sessionStripMeta.textContent = ownerState.target;', label="composer strip target copy")
    require(render_js, 'label: "SWITCHING",', label="composer strip switching row")
    require(render_js, 'label: "TARGET",', label="composer strip context row")
    require(render_js, 'label: transportState.label,', label="composer strip degraded phase row")
    require(render_js, "chips: footerDock.chips,", label="composer strip footer-dock chip row")
    require(render_js, 'dom.sessionStripState.innerHTML = sessionStripStateChipMarkup(stripState.chips || stripState);', label="composer strip chip render")
    require(render_js, 'dom.sessionStripDetail.textContent = footerDock.visible', label="composer strip footer-dock detail copy")
    require(render_js, '!handoffVisible && !degradedVisible && (!phaseProgression.visible || !liveAutonomy.visible)', label="transcript live activity unified visibility guard")
    require(render_js, 'const phaseLabel = degradedVisible', label="transcript live activity unified phase label")
    require(render_js, 'const provenanceLabel = degradedVisible', label="transcript live activity unified provenance label")
    require(render_js, 'const mergedStripVisible = Boolean(dom.sessionStrip && !dom.sessionStrip.hidden);', label="composer owner row merged strip visibility")
    require(render_js, 'dom.composerOwnerRow.dataset.composerOwnerMerged = mergedStripVisible ? "true" : "false";', label="composer owner merged dataset")
    require(render_js, 'dom.composerOwnerRow.hidden = mergedStripVisible;', label="composer owner row hidden when strip active")
    require(render_js, 'return { label: "ACCEPTED", tone: "neutral" };', label="accepted handoff chip")
    require(render_js, '"RECONNECT"', label="reconnecting provenance label")
    require(render_js, '"OPEN"', label="connecting provenance label")
    require(render_js, '"OFFLINE"', label="offline provenance label")
    require(render_js, 'const stage = degradedVisible', label="inline degraded stage mapping")
    require(render_js, 'const phaseLabel = degradedVisible', label="inline degraded phase mapping")
    require(render_js, 'const sourceLabel = degradedVisible ? String(sessionIndicator.source || "polling") : handoffVisible ? "handoff" : "sse";', label="inline source mapping without handoff duplication")
    require_absent(render_js, 'const handoffVisible = handoffState.stage === "pending-assistant" && selectedThreadSseOwned;', label="legacy inline handoff visibility guard")
    require(render_js, "sessionTimelineEventModel", label="session timeline event model helper")
    require(render_js, "renderSessionTimelineEvent", label="session timeline event render helper")
    require(render_js, "shouldCollapseHealthySessionEvent", label="healthy transcript session-event collapse helper")
    require(render_js, "renderTranscriptMilestones", label="transcript live milestone helper")
    require(render_js, "const transcriptLiveActivity = renderTranscriptLiveActivity(conversation, currentState, liveRun);", label="transcript live activity wiring")
    require(render_js, "if (inlineState.visible) {", label="transcript live activity suppression guard")
    require(render_js, 'data-live-session-event="${liveOwned ? "true" : "false"}"', label="transcript session event lane dataset")
    require(render_js, 'data-live-session-lane="${escapeHtml(liveOwned ? "selected-thread" : degradedVisible ? "degraded" : handoffVisible ? "handoff" : "fallback")}"', label="transcript session lane ownership dataset")
    require(render_js, 'data-live-milestones-visible="${liveOwned && milestoneModel.visible ? "true" : "false"}"', label="transcript session event milestone visibility dataset")
    require(render_js, 'data-live-milestones-phase="${escapeHtml(liveOwned ? String(milestoneModel.currentLabel || phaseLabel) : "")}"', label="transcript session event milestone phase dataset")
    require(render_js, 'data-live-path-verdict="${escapeHtml(pathVerdict)}"', label="transcript session lane path verdict dataset")
    require(render_js, 'data-live-verifier-acceptability="${escapeHtml(verifierAcceptability)}"', label="transcript session lane verifier dataset")
    require(render_js, 'data-live-blocker-reason="${escapeHtml(blockerReason)}"', label="transcript session lane blocker dataset")
    require(render_js, 'data-live-milestones="true"', label="transcript live milestone dataset")
    require(render_js, 'timeline-live-row timeline-live-row-milestones', label="transcript milestone row class")
    require(render_js, 'data-milestone-key="${escapeHtml(item.key)}"', label="transcript milestone key dataset")
    require(render_js, 'data-milestone-state="${escapeHtml(item.state)}"', label="transcript milestone state dataset")
    require(render_js, 'data-session-event="true"', label="session timeline event DOM")
    require(render_js, 'data-session-phase="${escapeHtml(model.phase)}"', label="session timeline event phase dataset")
    require(render_js, 'data-session-milestone="${escapeHtml(model.milestone)}"', label="session timeline event milestone dataset")
    require(render_js, 'data-session-verdict="${escapeHtml(model.verdict.toLowerCase())}"', label="session timeline event verdict dataset")
    require(render_js, "if (shouldCollapseHealthySessionEvent(item, currentState, conversation, liveRun)) {", label="healthy transcript session-event suppression guard")
    require(render_js, 'const sessionEvent = renderSessionTimelineEvent(item);', label="session timeline event projection wiring")
    require(render_js, "if (sessionEvent) {", label="session timeline event branch")
    require(render_js, "const renderedItems = items", label="transcript render item join")
    require(render_js, 'if (!items.length && !inlineSessionBlock && !transcriptLiveActivity) {', label="transcript empty-state live activity guard")
    require(render_js, 'dom.conversationTimeline.innerHTML = renderedItems + transcriptLiveActivity + inlineSessionBlock;', label="transcript tail live activity render")
    require_absent(render_js, 'dom.conversationTimeline.innerHTML = inlineSessionBlock + items', label="legacy inline block prepended render")
    require_absent(render_js, "if (footerDock.visible) {", label="legacy healthy footer-dock transcript suppression guard")
    require_absent(render_js, "In Flight Assistant", label="duplicate accepted status block copy")
    require(store_js, "deriveSelectedThreadFollowControlModel", label="selected-thread follow control model helper")
    require(render_js, "selectedThreadFooterFollowState", label="footer follow state helper")
    require(render_js, "pendingAppendCount", label="follow control unseen append state")
    require(render_js, 'const footerFollow = selectedThreadFooterFollowState(dom, currentState, conversationId, renderSource);', label="follow control footer follow source")
    require(render_js, 'dom.jumpToLatestButton.hidden = true;', label="follow button hidden when footer bar owns control")
    require(render_js, 'dom.jumpToLatestButton.dataset.followOwned = "none";', label="follow button owner cleared")
    require(render_js, 'dom.jumpToLatestButton.dataset.followState = "hidden";', label="follow button state cleared")
    require(render_js, 'dom.jumpToLatestButton.dataset.followCount = "0";', label="follow button count cleared")
    require(render_js, 'dom.jumpToLatestButton.dataset.followConversationId = "";', label="follow button conversation cleared")
    require(render_js, 'dom.jumpToLatestButton.dataset.followRenderSource = footerFollow.renderSource || renderSource || "snapshot";', label="follow control render source dataset")
    require(store_js, 'followState === "new"', label="follow control new-state derivation")
    require(store_js, 'followState === "paused"', label="follow control paused-state derivation")
    require(store_js, "새 live append", label="follow control new copy")
    require(store_js, "live follow paused · unseen", label="follow control paused copy")
    require(render_js, 'dom.sessionStripToggle.hidden = !footerFollow.visible;', label="footer bar follow action visibility")
    require(render_js, 'dom.sessionStripToggle.dataset.sessionAction = footerFollow.visible ? "jump-latest" : "toggle-session-rail";', label="session strip toggle action dataset")
    require(render_js, 'phase: "PROPOSAL"', label="proposal phase mapping")
    require(render_js, 'phase: "REVIEW"', label="review phase mapping")
    require(render_js, 'phase: "VERIFY"', label="verify phase mapping")
    require(render_js, 'phase: "READY"', label="proposal ready phase mapping")
    require(render_js, 'phase: sessionPhase.value === "LIVE" ? "LIVE" : "UNKNOWN"', label="neutral live phase mapping")
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
    require_absent(conversations_js, 'follow.textContent = isSwitching ? "ATTACH" : isSelected && showLiveMirror ? liveFollowLabel : "";', label="recent-thread attach follow wiring")
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
    require(conversations_js, "const authoritativeSelectedAttach =", label="selected-thread attach authority gate")
    require(conversations_js, "if (authoritativeSelectedAttach) {", label="selected-thread attach authority short circuit")
    require(conversations_js, 'const summaryLiveOwned = String(dom.sessionSummaryRow?.dataset.liveSessionOwned || "false") === "true";', label="active session canonical ownership source")
    require(conversations_js, 'const summaryLiveSource = String(dom.sessionSummaryRow?.dataset.liveSessionSource || "none");', label="active session canonical source dataset")
    require(conversations_js, 'const summaryPhaseLabel = String(dom.sessionSummaryRow?.dataset.summaryPhase || "").trim().toUpperCase();', label="active session summary phase dataset")
    require(conversations_js, 'const sessionIndicatorLabel = String(dom.sessionLiveIndicator?.textContent || "").trim().toUpperCase();', label="active session canonical label source")
    require(conversations_js, 'const followControl = deriveSelectedThreadFollowControlModel(state);', label="active session follow-control helper read")
    require(conversations_js, 'const sessionStatus = deriveSelectedThreadSessionStatus(state, state.conversationCache);', label="active session canonical status helper read")
    require(conversations_js, 'const healthySelectedSessionMirror =', label="active session healthy mirror gate")
    require(conversations_js, 'summaryLiveSource === "sse"', label="active session healthy sse source gate")
    require(conversations_js, 'sessionIndicatorLabel === "SSE OWNER"', label="active session healthy label gate")
    require(conversations_js, 'const livePhaseLabel = summaryPhaseLabel || liveRunPhase || sessionStatus.phaseValue || "LIVE";', label="active session mirrored live phase label")
    require(conversations_js, 'rowState = followControl.visible ? followControl.followState : "live";', label="active session mirrored state mapping")
    require(conversations_js, 'ownerLabel = sessionStatus.transportLabel || "SSE OWNER";', label="active session mirrored owner label")
    require(conversations_js, 'stateLabel = livePhaseLabel;', label="active session mirrored finite state label")
    require(conversations_js, 'followLabel = followControl.visible ? followControl.stateLabel : "LIVE";', label="active session mirrored follow label")
    require(conversations_js, 'rowSource = summaryLiveSource;', label="active session mirrored source")
    require(conversations_js, 'rowPhase = livePhaseLabel;', label="active session mirrored phase")
    require(conversations_js, 'rowUnseenCount = followControl.visible ? Math.max(Number(followControl.unseenCount || unseenCount || 0), 0) : 0;', label="active session unseen count mirror")
    require(conversations_js, '`selected thread · ${livePhaseLabel.toLowerCase()} · ${rowUnseenCount} new`', label="active session unseen meta copy")
    require(conversations_js, '`selected thread · ${livePhaseLabel.toLowerCase()} · ${followControl.detailLabel}`', label="active session paused meta copy")
    require(conversations_js, '`selected thread · ${livePhaseLabel.toLowerCase()} · sse owner`', label="active session healthy meta copy")
    require(conversations_js, "syncSelectedSessionFromLiveAppend", label="selected-thread live append sync helper")
    require(conversations_js, "const liveJobId = String(livePayload.job_id || \"\").trim();", label="live append job id extraction")
    require(conversations_js, "state.currentJobId = liveJobId;", label="live append selected-thread job id authority")
    require(conversations_js, "conversation.latest_job_id = liveJobId;", label="live append conversation job id authority")
    require(conversations_js, "shouldProjectAutonomySummaryFromLiveAppend", label="autonomy summary append projection helper")
    require(conversations_js, "projectAutonomySummaryFromLiveAppend", label="autonomy summary live projection helper")
    require(conversations_js, "normalizeAutonomySummary", label="autonomy summary normalization helper")
    require(conversations_js, "hydrateAutonomySummary", label="autonomy summary hydration helper")
    require(conversations_js, "isSelectedThreadAutonomyAuthoritative", label="selected-thread autonomy authority helper")
    require(conversations_js, "shouldAllowGoalsPollingFallback", label="selected-thread goals fallback gate")
    require(conversations_js, "liveJobMetaLabel", label="live append job meta helper")
    require(conversations_js, "const projectedAutonomySummary = projectAutonomySummaryFromLiveAppend(kind, payload);", label="append-driven autonomy summary projection")
    require(conversations_js, "state.autonomySummary = projectedAutonomySummary;", label="append-driven autonomy summary state update")
    require(conversations_js, 'if (!shouldAllowGoalsPollingFallback({ conversationId })) {', label="healthy selected-thread goals fallback suppression")
    require(conversations_js, 'await refreshGoalSummary({ conversationId: conversation.conversation_id });', label="conversation-scoped autonomy fallback refresh")
    require_absent(conversations_js, "refreshGoalSummary().catch(() => {});", label="legacy append-driven autonomy summary refetch")
    require(conversations_js, "setJobMeta(dom, immediateMeta);", label="append-driven job meta refresh")
    require(conversations_js, "scheduleAppendStreamResume", label="reconnect resume scheduler")
    require(conversations_js, "transitionAppendStreamToFallback", label="explicit reconnect fallback helper")
    require(conversations_js, 'state.appendStream.transport = "sse"', label="selected-thread sse transport")
    require(store_js, "export function isAppendStreamAuthoritative", label="append stream authoritative helper")
    require(store_js, "export function deriveSelectedThreadSessionStatus", label="canonical selected-thread session status helper")
    require(store_js, "selectedThreadRestore", label="selected-thread restore state")
    require(store_js, "restoreResume", label="selected-thread restore resume state")
    require(store_js, "restoreStage", label="selected-thread restore stage")
    require(store_js, "switchActive", label="selected-thread switch activity state")
    require(store_js, "switchConversationId", label="selected-thread switch conversation state")
    require(store_js, "switchTargetTitle", label="selected-thread switch title state")
    require(store_js, 'transportReason = restoreResume ? "saved-restore-resume" : "saved-restore-attach";', label="selected-thread restore transport reason")
    require(store_js, 'presentation = "restore";', label="selected-thread restore presentation")
    require(store_js, "export function deriveSelectedThreadLiveAutonomy", label="canonical selected-thread live autonomy helper")
    require(store_js, "export function deriveSelectedThreadPhaseProgression", label="canonical selected-thread phase progression helper")
    require(store_js, "export function deriveSelectedThreadTimelineMilestones", label="canonical selected-thread timeline milestones helper")
    require(store_js, "export function isSelectedThreadSessionOwned", label="selected-thread session ownership helper")
    require(store_js, 'phaseValue === "LIVE"', label="selected-thread session live phase guard")
    require(store_js, 'phaseValue === "PROPOSAL"', label="selected-thread session proposal phase guard")
    require(store_js, 'phaseValue === "REVIEW"', label="selected-thread session review phase guard")
    require(store_js, 'phaseValue === "VERIFY"', label="selected-thread session verify phase guard")
    require(store_js, 'phaseValue === "READY"', label="selected-thread session ready phase guard")
    require(store_js, 'phaseValue === "APPLIED"', label="selected-thread session applied phase guard")
    require(store_js, 'appendStream.status === "connecting" || appendStream.status === "live"', label="append stream authoritative connecting-or-live guard")
    require(jobs_js, "isAppendStreamAuthoritative", label="job polling authoritative helper wiring")
    require(jobs_js, "isSelectedThreadSessionOwned", label="job polling selected-thread session ownership helper wiring")
    require(jobs_js, "state.currentConversationId && isSelectedThreadSessionOwned(state, state.currentConversationId)", label="polling suppression while selected-thread session is sse-owned")
    require(jobs_js, "stopPolling();\n      return;", label="polling early exit while selected-thread session is sse-owned")
    require(jobs_js, "!isAppendStreamAuthoritative(state, state.currentConversationId)", label="polling refetch skip while append stream is authoritative")
    require(styles, ".conversation-card-live-owner-row", label="selected card live owner row CSS")
    require(styles, ".active-session-row", label="active session row CSS")
    require(styles, ".active-session-chip", label="active session chip CSS")
    require(styles, '.active-session-row[data-active-session-state="paused"] .active-session-chip[data-active-chip="state"]', label="active session paused chip CSS")
    require(styles, '.active-session-row[data-active-session-follow="live"] .active-session-chip[data-active-chip="follow"]', label="active session live chip CSS")
    require(styles, '.active-session-row[data-active-session-follow="attach"] .active-session-chip[data-active-chip="follow"]', label="active session attach chip CSS")
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
