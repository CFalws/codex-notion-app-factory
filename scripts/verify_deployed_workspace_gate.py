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
  const threadPhase = document.querySelector("#thread-phase-chip");
  const threadSessionSummary = document.querySelector("#thread-session-summary");
  const inlineBlocks = Array.from(document.querySelectorAll('.session-inline-block[data-selected-thread-live-block="true"], .session-inline-block[data-selected-thread-degraded-block="true"]'));
  const liveActivity = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="true"]');
  const secondaryPanel = document.querySelector("#secondary-panel");
  const secondaryPanelToggle = document.querySelector("#secondary-panel-toggle");
  const secondarySessionFacts = document.querySelector("#secondary-session-facts");
  const activeSessionRow = document.querySelector("#active-session-row");
  const sessionStrip = document.querySelector("#session-strip");
  const composerUtilityMenu = document.querySelector("#composer-utility-menu");
  const composerUtilityToggle = document.querySelector("#composer-utility-toggle");
  const composerUtilityCluster = document.querySelector("#composer-utility-cluster");
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
    threadPhase: threadPhase ? {
      hidden: !!threadPhase.hidden,
      dataset: { ...threadPhase.dataset },
      text: (threadPhase.textContent || "").trim(),
    } : null,
    threadSessionSummary: threadSessionSummary ? {
      hidden: !!threadSessionSummary.hidden,
      dataset: { ...threadSessionSummary.dataset },
      text: (threadSessionSummary.textContent || "").trim(),
    } : null,
    inlineBlocks: inlineBlocks.map(block => ({
      dataset: { ...block.dataset },
      text: (block.textContent || "").trim(),
    })),
    liveActivity: liveActivity ? {
      dataset: { ...liveActivity.dataset },
      text: (liveActivity.textContent || "").trim(),
    } : null,
    secondaryPanel: secondaryPanel ? {
      dataset: { ...secondaryPanel.dataset },
      text: (secondaryPanel.textContent || "").trim(),
    } : null,
    secondaryPanelToggle: secondaryPanelToggle ? {
      expanded: secondaryPanelToggle.getAttribute("aria-expanded"),
      text: (secondaryPanelToggle.textContent || "").trim(),
    } : null,
    secondarySessionFacts: secondarySessionFacts ? {
      dataset: { ...secondarySessionFacts.dataset },
      text: (secondarySessionFacts.textContent || "").trim(),
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
    composerUtilityMenu: composerUtilityMenu ? {
      dataset: { ...composerUtilityMenu.dataset },
      text: (composerUtilityMenu.textContent || "").trim(),
    } : null,
    composerUtilityToggle: composerUtilityToggle ? {
      dataset: { ...composerUtilityToggle.dataset },
      expanded: composerUtilityToggle.getAttribute("aria-expanded"),
      text: (composerUtilityToggle.textContent || "").trim(),
    } : null,
    composerUtilityCluster: composerUtilityCluster ? {
      hidden: !!composerUtilityCluster.hidden,
      dataset: { ...composerUtilityCluster.dataset },
      ariaHidden: composerUtilityCluster.getAttribute("aria-hidden"),
      text: (composerUtilityCluster.textContent || "").trim(),
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
  window.__verifySwitchObserver = null;
  window.__verifySwitchMonitor = {
    active: false,
    targetConversationId: "",
    sawEmptyState: false,
    maxTransitionCount: 0,
    sawHiddenComposerDock: false,
    sawClearedWorkspacePlaceholder: false,
  };
  window.__verifySampleSwitchMonitor = () => {
    const monitor = window.__verifySwitchMonitor;
    if (!monitor || !monitor.active) {
      return;
    }
    const timeline = document.querySelector("#conversation-timeline");
    const composerDock = document.querySelector("#conversation-footer-dock");
    const emptyState = document.querySelector(".timeline-empty");
    const transitions = document.querySelectorAll('[data-thread-transition="switching"]');
    const targetConversationId = String(monitor.targetConversationId || "");
    const placeholderMode = String(timeline?.dataset.workspacePlaceholder || "");
    const placeholderConversationId = String(timeline?.dataset.workspaceConversationId || "");
    const targetAttached = placeholderMode === "conversation" && placeholderConversationId === targetConversationId;
    monitor.maxTransitionCount = Math.max(Number(monitor.maxTransitionCount || 0), transitions.length);
    if (!targetAttached && emptyState) {
      monitor.sawEmptyState = true;
    }
    if (composerDock) {
      const style = getComputedStyle(composerDock);
      if (composerDock.hidden || style.display === "none" || style.visibility === "hidden") {
        monitor.sawHiddenComposerDock = true;
      }
    }
    if (!targetAttached && placeholderMode !== "conversation") {
      monitor.sawClearedWorkspacePlaceholder = true;
    }
  };
  window.__verifyStartSwitchMonitor = (targetConversationId) => {
    if (window.__verifySwitchObserver) {
      window.__verifySwitchObserver.disconnect();
    }
    window.__verifySwitchMonitor = {
      active: true,
      targetConversationId: String(targetConversationId || ""),
      sawEmptyState: false,
      maxTransitionCount: 0,
      sawHiddenComposerDock: false,
      sawClearedWorkspacePlaceholder: false,
    };
    window.__verifySwitchObserver = new MutationObserver(() => {
      window.__verifySampleSwitchMonitor();
    });
    window.__verifySwitchObserver.observe(document.documentElement, {
      subtree: true,
      childList: true,
      attributes: true,
      attributeFilter: ["hidden", "data-workspace-placeholder", "data-workspace-conversation-id", "style"],
    });
    window.__verifySampleSwitchMonitor();
  };
  window.__verifyStopSwitchMonitor = () => {
    if (window.__verifySwitchObserver) {
      window.__verifySwitchObserver.disconnect();
      window.__verifySwitchObserver = null;
    }
    if (window.__verifySwitchMonitor) {
      window.__verifySwitchMonitor.active = false;
    }
  };
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
                  const threadPhase = document.querySelector("#thread-phase-chip");
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
                    threadPhase &&
                    threadPhase.hidden &&
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

            page.wait_for_function(
                """conversationId => {
                  const inlineBlocks = document.querySelectorAll('.session-inline-block[data-selected-thread-live-block="true"], .session-inline-block[data-selected-thread-degraded-block="true"]');
                  const inlineBlock = inlineBlocks.length ? inlineBlocks[0] : null;
                  const liveActivity = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="true"]');
                  const primaryLiveActivities = document.querySelectorAll('.timeline-item.live-activity[data-live-session-primary="true"]');
                  const threadPhase = document.querySelector("#thread-phase-chip");
                  const threadSessionSummary = document.querySelector("#thread-session-summary");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const selectedCard = document.querySelector('.conversation-card[data-selected="true"]');
                  const selectedCardLiveOwnerRow = selectedCard ? selectedCard.querySelector('[data-conversation-live-owner-row]') : null;
                  const selectedCardLiveDetail = selectedCard ? selectedCard.querySelector('[data-conversation-live-detail]') : null;
                  const selectedCardLiveFollow = selectedCard ? selectedCard.querySelector('[data-conversation-live-follow]') : null;
                  const visibleConversationOwnerRows = document.querySelectorAll('[data-conversation-live-owner-row]:not([hidden])');
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const sessionStripDetail = document.querySelector("#session-strip-detail");
                  const stripChips = sessionStripState ? sessionStripState.querySelectorAll(".session-chip") : [];
                  const threadScroller = document.querySelector("#thread-scroller");
                  const composerOwnerRow = document.querySelector("#composer-owner-row");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const sendRequest = document.querySelector("#send-request");
                  const secondaryPanelToggle = document.querySelector("#secondary-panel-toggle");
                  const secondarySessionFacts = document.querySelector("#secondary-session-facts");
                  const autonomyDetailCard = document.querySelector(".autonomy-detail-card");
                  const autonomyDetail = document.querySelector("#autonomy-detail");
                  const statusOutput = document.querySelector("#status-output");
                  const executionStatusCard = statusOutput ? statusOutput.closest(".inspector-card") : null;
                  const sessionEvents = document.querySelectorAll('.timeline-item.session-event[data-append-source="sse"]');
                  const milestoneLane = inlineBlock ? inlineBlock.querySelector('[data-live-milestones="true"]') : null;
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  const goalsFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/apps/${appId}/goals`)
                  );
                  return Boolean(
                    inlineBlocks.length === 1 &&
                    inlineBlock &&
                    !liveActivity &&
                    primaryLiveActivities.length === 0 &&
                    inlineBlock.dataset.selectedThreadLiveBlock === "true" &&
                    inlineBlock.dataset.selectedThreadDegradedBlock === "false" &&
                    inlineBlock.dataset.liveBlockOwned === "true" &&
                    inlineBlock.dataset.liveBlockConversationId === conversationId &&
                    inlineBlock.dataset.liveBlockTransport === "SSE OWNER" &&
                    ["EXPECTED", "ACCEPTABLE"].includes(inlineBlock.dataset.liveBlockPathVerdict || "") &&
                    (inlineBlock.dataset.liveBlockExpectedPath || "").length > 0 &&
                    ["ACCEPTABLE", "PENDING"].includes(inlineBlock.dataset.liveBlockVerifierAcceptability || "") &&
                    (inlineBlock.dataset.liveBlockBlockerReason || "").length > 0 &&
                    ["PROPOSAL", "REVIEW", "VERIFY", "AUTO APPLY", "READY", "APPLIED"].includes(inlineBlock.dataset.liveBlockPhase || "") &&
                    inlineBlock.textContent.includes("SELECTED") &&
                    inlineBlock.textContent.includes("SSE OWNER") &&
                    milestoneLane &&
                    milestoneLane.dataset.liveMilestones === "true" &&
                    milestoneLane.dataset.liveMilestonesExplicit === "true" &&
                    milestoneLane.dataset.liveMilestonesPhase === inlineBlock.dataset.liveBlockPhase &&
                    milestoneLane.querySelector('[data-milestone-key="auto-apply"]') &&
                    threadSessionSummary &&
                    threadSessionSummary.hidden &&
                    threadSessionSummary.dataset.threadSummaryVisible === "false" &&
                    threadSessionSummary.dataset.threadSummaryPresentation === "cleared" &&
                    threadSessionSummary.dataset.threadSummaryOwned === "false" &&
                    threadSessionSummary.dataset.threadSummaryScope === "" &&
                    threadSessionSummary.dataset.threadSummaryPath === "" &&
                    threadSessionSummary.dataset.threadSummaryOwner === "" &&
                    threadSessionSummary.dataset.threadSummaryPhase === "" &&
                    threadSessionSummary.dataset.threadSummaryReason === "idle" &&
                    threadSessionSummary.dataset.liveSessionVisible === "false" &&
                    threadSessionSummary.dataset.liveSessionPresentation === "cleared" &&
                    threadSessionSummary.dataset.liveSessionOwned === "false" &&
                    threadSessionSummary.dataset.liveSessionStateLabel === "" &&
                    threadSessionSummary.dataset.liveSessionPhase === "" &&
                    threadSessionSummary.dataset.centerTimelineAuthority === "true" &&
                    threadSessionSummary.dataset.centerTimelinePresentation === "healthy" &&
                    threadPhase &&
                    threadPhase.hidden &&
                    threadPhase.dataset.liveSessionVisible === "false" &&
                    threadPhase.dataset.liveSessionPresentation === "cleared" &&
                    threadPhase.dataset.liveSessionOwned === "false" &&
                    threadPhase.dataset.centerTimelineAuthority === "true" &&
                    threadPhase.dataset.centerTimelinePresentation === "healthy" &&
                    activeSessionRow &&
                    !activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "true" &&
                    activeSessionRow.dataset.activeSessionCanonical === "true" &&
                    activeSessionRow.dataset.activeSessionSource === "sse" &&
                    activeSessionRow.dataset.activeSessionConversationId === conversationId &&
                    activeSessionRow.dataset.activeSessionPhase === inlineBlock.dataset.liveBlockPhase &&
                    ["live", "new", "paused"].includes(activeSessionRow.dataset.activeSessionState || "") &&
                    visibleConversationOwnerRows.length === 0 &&
                    selectedCardLiveOwnerRow &&
                    selectedCardLiveOwnerRow.hidden &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerVisible === "false" &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerState === "idle" &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerConversationId === "" &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerSource === "none" &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerPhase === "IDLE" &&
                    selectedCardLiveDetail &&
                    selectedCardLiveDetail.textContent.trim() === "LIVE" &&
                    selectedCardLiveFollow &&
                    selectedCardLiveFollow.hidden &&
                    (selectedCardLiveFollow.textContent || "").trim() === "" &&
                    sessionStrip &&
                    !sessionStrip.hidden &&
                    sessionStrip.dataset.footerSurface === "dock" &&
                    sessionStrip.dataset.liveOwned === "true" &&
                    sessionStrip.dataset.sessionOwner === "selected-thread" &&
                    sessionStrip.dataset.sessionPresentation !== "suppressed" &&
                    sessionStrip.dataset.footerDockOwned === "true" &&
                    sessionStrip.dataset.footerDockMilestones === "true" &&
                    sessionStrip.dataset.footerDockPhase === inlineBlock.dataset.liveBlockPhase &&
                    sessionStrip.dataset.footerDockSource === "sse" &&
                    sessionStrip.dataset.composerTransportOwned === "true" &&
                    sessionStrip.dataset.phaseProvenance === "sse" &&
                    threadScroller &&
                    sessionStrip.dataset.phaseValue === inlineBlock.dataset.liveBlockPhase &&
                    threadScroller.dataset.phaseValue === inlineBlock.dataset.liveBlockPhase &&
                    threadScroller.dataset.phaseProvenance === "sse" &&
                    sessionStripState &&
                    !sessionStripState.hidden &&
                    stripChips.length >= 2 &&
                    sessionStripState.dataset.sessionStripRole === "live-dock" &&
                    sessionStripState.dataset.sessionStripLabel === inlineBlock.dataset.liveBlockPhase &&
                    sessionStripState.textContent.includes(inlineBlock.dataset.liveBlockPhase || "") &&
                    sessionStripMeta &&
                    !sessionStripMeta.hidden &&
                    sessionStripMeta.textContent.trim().length > 0 &&
                    sessionStripDetail &&
                    !sessionStripDetail.hidden &&
                    sessionStripDetail.textContent.includes(inlineBlock.dataset.liveBlockPhase || "") &&
                    composerUtilityMenu &&
                    composerUtilityMenu.dataset.composerUtilityOpen === "false" &&
                    composerUtilityMenu.dataset.composerUtilityState === "closed" &&
                    composerUtilityToggle &&
                    composerUtilityToggle.dataset.composerUtilityOpen === "false" &&
                    composerUtilityToggle.dataset.composerUtilityState === "closed" &&
                    composerUtilityToggle.getAttribute("aria-expanded") === "false" &&
                    composerUtilityCluster &&
                    composerUtilityCluster.hidden &&
                    composerUtilityCluster.dataset.composerUtilityOpen === "false" &&
                    composerUtilityCluster.dataset.composerUtilityState === "closed" &&
                    composerUtilityCluster.getAttribute("aria-hidden") === "true" &&
                    composerOwnerRow &&
                    composerOwnerRow.hidden &&
                    composerOwnerRow.dataset.composerOwnerMerged === "true" &&
                    composerOwnerRow.dataset.composerOwner === "ready" &&
                    composerOwnerRow.dataset.composerOwnerConversationId === conversationId &&
                    composerOwnerRow.textContent.includes("READY") &&
                    composerOwnerRow.textContent.includes("SSE OWNER") &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    sendRequest &&
                    sendRequest.dataset.composerOwnerState === "ready" &&
                    sendRequest.dataset.composerOwnerConversationId === conversationId &&
                    secondaryPanelToggle &&
                    secondaryPanelToggle.getAttribute("aria-expanded") === "false" &&
                    document.body.dataset.secondaryPanelOpen !== "true" &&
                    secondarySessionFacts &&
                    secondarySessionFacts.hidden &&
                    secondarySessionFacts.dataset.secondaryFactsPresentation === "suppressed" &&
                    secondarySessionFacts.dataset.secondaryFactsOwned === "false" &&
                    secondarySessionFacts.dataset.secondaryFactsTransport === "SUPPRESSED" &&
                    secondarySessionFacts.dataset.secondaryFactsPhase === inlineBlock.dataset.liveBlockPhase &&
                    secondarySessionFacts.dataset.secondaryFactsPath === inlineBlock.dataset.liveBlockPathVerdict &&
                    secondarySessionFacts.dataset.secondaryFactsVerifier === inlineBlock.dataset.liveBlockVerifierAcceptability &&
                    secondarySessionFacts.dataset.secondaryFactsBlocker === inlineBlock.dataset.liveBlockBlockerReason &&
                    autonomyDetailCard &&
                    autonomyDetailCard.hidden &&
                    autonomyDetailCard.dataset.autonomySurface === "suppressed" &&
                    autonomyDetailCard.dataset.centerTimelineAuthority === "true" &&
                    autonomyDetailCard.dataset.centerTimelinePresentation === "healthy" &&
                    autonomyDetail &&
                    autonomyDetail.dataset.surface === "suppressed" &&
                    autonomyDetail.dataset.centerTimelineAuthority === "true" &&
                    autonomyDetail.dataset.centerTimelinePresentation === "healthy" &&
                    executionStatusCard &&
                    executionStatusCard.hidden &&
                    executionStatusCard.dataset.executionSurface === "suppressed" &&
                    executionStatusCard.dataset.centerTimelineAuthority === "true" &&
                    executionStatusCard.dataset.centerTimelinePresentation === "healthy" &&
                    statusOutput &&
                    statusOutput.dataset.surface === "suppressed" &&
                    statusOutput.dataset.centerTimelineAuthority === "true" &&
                    statusOutput.dataset.centerTimelinePresentation === "healthy" &&
                    sessionEvents.length === 0 &&
                    !document.querySelector("#jump-to-latest") &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0
                  );
                }""",
                [app_id, conversation_id],
                timeout=120000,
            )
            healthy_snapshot = page.evaluate(browser_snapshot_script())

            page.click("#secondary-panel-toggle")
            page.wait_for_function(
                """() => {
                  const secondaryPanelToggle = document.querySelector("#secondary-panel-toggle");
                  const secondarySessionFacts = document.querySelector("#secondary-session-facts");
                  const autonomyDetailCard = document.querySelector(".autonomy-detail-card");
                  const executionStatusCard = document.querySelector("#status-output")?.closest(".inspector-card");
                  return Boolean(
                    secondaryPanelToggle &&
                    secondaryPanelToggle.getAttribute("aria-expanded") === "true" &&
                    document.body.dataset.secondaryPanelOpen === "true" &&
                    secondarySessionFacts &&
                    secondarySessionFacts.hidden &&
                    secondarySessionFacts.dataset.secondaryFactsPresentation === "suppressed" &&
                    secondarySessionFacts.dataset.secondaryFactsOwned === "false" &&
                    secondarySessionFacts.dataset.secondaryFactsTransport === "SUPPRESSED" &&
                    autonomyDetailCard &&
                    autonomyDetailCard.hidden &&
                    autonomyDetailCard.dataset.autonomySurface === "suppressed" &&
                    executionStatusCard &&
                    executionStatusCard.hidden &&
                    executionStatusCard.dataset.executionSurface === "suppressed"
                  );
                }""",
                timeout=30000,
            )
            page.click("#secondary-panel-close")
            page.wait_for_function(
                """() => {
                  const secondaryPanelToggle = document.querySelector("#secondary-panel-toggle");
                  return Boolean(
                    secondaryPanelToggle &&
                    secondaryPanelToggle.getAttribute("aria-expanded") === "false" &&
                    document.body.dataset.secondaryPanelOpen !== "true"
                  );
                }""",
                timeout=30000,
            )

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
                  const sessionStripToggle = document.querySelector("#session-strip-toggle");
                  return Boolean(
                    !document.querySelector("#jump-to-latest") &&
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
                  const sessionStripToggle = document.querySelector("#session-strip-toggle");
                  return Boolean(
                    !document.querySelector("#jump-to-latest") &&
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
                  const threadPhase = document.querySelector("#thread-phase-chip");
                  const composerOwnerRow = document.querySelector("#composer-owner-row");
                  const transition = document.querySelector('[data-thread-transition="attach"]');
                  const inlineBlocks = document.querySelectorAll('.session-inline-block[data-selected-thread-live-block="true"], .session-inline-block[data-selected-thread-degraded-block="true"]');
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
                    threadSessionSummary &&
                    !threadSessionSummary.hidden &&
                    threadSessionSummary.dataset.liveSessionPresentation === "restore" &&
                    threadSessionSummary.dataset.restorePath === "resume" &&
                    threadSessionSummary.dataset.restoreProvenance === "sse-bootstrap" &&
                    threadSessionSummary.dataset.restoreStage === "none" &&
                    threadPhase &&
                    threadPhase.hidden &&
                    composerOwnerRow &&
                    composerOwnerRow.hidden &&
                    composerOwnerRow.dataset.composerOwnerMerged === "true" &&
                    ["resume", "attach"].includes(composerOwnerRow.dataset.composerOwner || "") &&
                    composerOwnerRow.dataset.composerOwnerConversationId === conversationId &&
                    composerOwnerRow.dataset.composerRestoreStage === "none" &&
                    transition &&
                    transition.dataset.threadTransitionCompact === "true" &&
                    transition.dataset.threadTransitionStateLabel === "RESTORE" &&
                    transition.dataset.threadTransitionPhaseLabel === "RESUME" &&
                    transition.dataset.threadTransitionTransport === "SSE RESTORE" &&
                    transition.dataset.threadTransitionConversationId === conversationId &&
                    transition.dataset.threadTransitionRestorePath === "resume" &&
                    transition.dataset.threadTransitionRestoreProvenance === "sse-bootstrap" &&
                    executionStatusCard &&
                    executionStatusCard.hidden &&
                    executionStatusCard.dataset.executionSurface === "center-lane" &&
                    statusOutput &&
                    statusOutput.dataset.surface === "center-lane" &&
                    sessionStrip.dataset.phaseValue === transition.dataset.threadTransitionPhaseLabel &&
                    sessionStrip.dataset.phaseProvenance === "sse" &&
                    threadScroller.dataset.phaseValue === transition.dataset.threadTransitionPhaseLabel &&
                    threadScroller.dataset.phaseProvenance === "sse" &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    resumeEvents.length >= 1 &&
                    Number(lastResume.resume_from_append_id || 0) > 0 &&
                    resumeUrls.length >= 1 &&
                    conversationFetches.length === 0 &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0 &&
                    appendIds.length === deduped.size &&
                    inlineBlocks.length === 0 &&
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
                  const inlineBlocks = document.querySelectorAll('.session-inline-block[data-selected-thread-live-block="true"], .session-inline-block[data-selected-thread-degraded-block="true"]');
                  const threadSessionSummary = document.querySelector("#thread-session-summary");
                  const threadPhase = document.querySelector("#thread-phase-chip");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const selectedCard = document.querySelector('.conversation-card[data-selected="true"]');
                  const selectedCardLiveOwnerRow = selectedCard ? selectedCard.querySelector('[data-conversation-live-owner-row]') : null;
                  const visibleConversationOwnerRows = document.querySelectorAll('[data-conversation-live-owner-row]:not([hidden])');
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const secondarySessionFacts = document.querySelector("#secondary-session-facts");
                  const composerUtilityMenu = document.querySelector("#composer-utility-menu");
                  const composerUtilityToggle = document.querySelector("#composer-utility-toggle");
                  const composerUtilityCluster = document.querySelector("#composer-utility-cluster");
                  const statusOutput = document.querySelector("#status-output");
                  const executionStatusCard = statusOutput ? statusOutput.closest(".inspector-card") : null;
                  const stripChips = sessionStripState ? sessionStripState.querySelectorAll(".session-chip") : [];
                  if (!degraded || healthy || inlineBlocks.length !== 0 || !threadPhase || !activeSessionRow || !sessionStrip || !sessionStripState || !executionStatusCard || !statusOutput) {
                    return false;
                  }
                  const reason = degraded.dataset.liveReason || "";
                  const phase = degraded.dataset.liveRunPhase || "";
                  return (
                    ["retrying", "reconnecting", "polling-fallback", "session-rotation"].includes(reason) &&
                    ["RECONNECT", "POLLING"].includes(phase) &&
                    ["RECONNECT", "POLLING"].includes(degraded.dataset.liveTransport || "") &&
                    degraded.dataset.liveTransportOwned === "false" &&
                    secondarySessionFacts &&
                    secondarySessionFacts.dataset.secondaryFactsPresentation === "degraded" &&
                    secondarySessionFacts.dataset.secondaryFactsOwned === "false" &&
                    secondarySessionFacts.dataset.secondaryFactsTransport === degraded.dataset.liveTransport &&
                    secondarySessionFacts.dataset.secondaryFactsPhase === phase &&
                    threadSessionSummary &&
                    !threadSessionSummary.hidden &&
                    threadSessionSummary.dataset.threadSummaryVisible === "true" &&
                    threadSessionSummary.dataset.threadSummaryPresentation === "degraded" &&
                    threadSessionSummary.dataset.threadSummaryOwned === "false" &&
                    threadPhase.hidden &&
                    threadSessionSummary.dataset.liveSessionVisible === "true" &&
                    threadSessionSummary.dataset.liveSessionPresentation === "degraded" &&
                    threadSessionSummary.dataset.liveSessionOwned === "false" &&
                    threadSessionSummary.dataset.liveSessionStateLabel === degraded.dataset.liveTransport &&
                    threadSessionSummary.dataset.centerTimelineAuthority === "true" &&
                    threadSessionSummary.dataset.centerTimelinePresentation === "degraded" &&
                    visibleConversationOwnerRows.length === 0 &&
                    selectedCardLiveOwnerRow &&
                    selectedCardLiveOwnerRow.hidden &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerVisible === "false" &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerState === "idle" &&
                    activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "none" &&
                    composerOwnerRow &&
                    composerOwnerRow.hidden &&
                    composerOwnerRow.dataset.composerOwnerMerged === "true" &&
                    ["reconnect", "polling"].includes(composerOwnerRow.dataset.composerOwner || "") &&
                    composerOwnerRow.dataset.composerOwnerConversationId === conversationId &&
                    !composerOwnerRow.textContent.includes("READY") &&
                    !sessionStrip.hidden &&
                    stripChips.length === 1 &&
                    sessionStripState.dataset.sessionStripRole === "degraded" &&
                    sessionStripState.dataset.sessionStripLabel === phase &&
                    sessionStripState.textContent.trim() === phase &&
                    composerUtilityMenu &&
                    composerUtilityMenu.dataset.composerUtilityOpen === "false" &&
                    composerUtilityMenu.dataset.composerUtilityState === "closed" &&
                    composerUtilityToggle &&
                    composerUtilityToggle.dataset.composerUtilityOpen === "false" &&
                    composerUtilityToggle.dataset.composerUtilityState === "closed" &&
                    composerUtilityToggle.getAttribute("aria-expanded") === "false" &&
                    composerUtilityCluster &&
                    composerUtilityCluster.hidden &&
                    composerUtilityCluster.dataset.composerUtilityOpen === "false" &&
                    composerUtilityCluster.dataset.composerUtilityState === "closed" &&
                    composerUtilityCluster.getAttribute("aria-hidden") === "true" &&
                    ["reconnect", "polling"].includes(sessionStrip.dataset.composerTransport || "") &&
                    sessionStrip.dataset.composerTransportOwned === "false" &&
                    !executionStatusCard.hidden &&
                    executionStatusCard.dataset.executionSurface === "secondary-detail" &&
                    executionStatusCard.dataset.centerTimelineAuthority === "true" &&
                    executionStatusCard.dataset.centerTimelinePresentation === "degraded" &&
                    statusOutput.dataset.surface === "secondary-detail" &&
                    statusOutput.dataset.centerTimelineAuthority === "true" &&
                    statusOutput.dataset.centerTimelinePresentation === "degraded" &&
                    sessionStrip.dataset.composerTransport !== "sse-owner" &&
                    !document.querySelector("#jump-to-latest")
                  );
                }""",
                timeout=120000,
            )
            degraded_snapshot = page.evaluate(browser_snapshot_script())

            page.evaluate(
                """targetConversationId => {
                  window.__verifyStartSwitchMonitor(targetConversationId);
                  window.__verifyFetchMark = window.__verifyFetchLog.length;
                }""",
                switch_conversation_id,
            )
            page.click(f'[data-conversation-id="{switch_conversation_id}"]')
            page.wait_for_function(
                """([appId, targetConversationId]) => {
                  const transition = document.querySelector('[data-thread-transition="switching"]');
                  const threadPhase = document.querySelector("#thread-phase-chip");
                  const threadTitle = document.querySelector("#thread-title");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const selectedCard = document.querySelector('.conversation-card[data-selected="true"]');
                  const selectedCardLiveOwnerRow = selectedCard ? selectedCard.querySelector('[data-conversation-live-owner-row]') : null;
                  const visibleConversationOwnerRows = document.querySelectorAll('[data-conversation-live-owner-row]:not([hidden])');
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const secondarySessionFacts = document.querySelector("#secondary-session-facts");
                  const composerUtilityMenu = document.querySelector("#composer-utility-menu");
                  const composerUtilityToggle = document.querySelector("#composer-utility-toggle");
                  const composerUtilityCluster = document.querySelector("#composer-utility-cluster");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const sendRequest = document.querySelector("#send-request");
                  const composerOwnerRow = document.querySelector("#composer-owner-row");
                  const threadScroller = document.querySelector("#thread-scroller");
                  const inlineBlocks = document.querySelectorAll('.session-inline-block[data-selected-thread-live-block="true"], .session-inline-block[data-selected-thread-degraded-block="true"]');
                  const healthy = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="true"]');
                  const degraded = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="false"]');
                  const empty = document.querySelector(".timeline-empty");
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  const goalsFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/apps/${appId}/goals`)
                  );
                  const switchMonitor = window.__verifySwitchMonitor || {};
                  return Boolean(
                    transition &&
                    document.querySelectorAll('[data-thread-transition="switching"]').length === 1 &&
                    transition.dataset.threadTransitionPhase === "switching" &&
                    transition.dataset.threadTransitionSource === "selected-thread-session" &&
                    transition.dataset.threadTransitionOwnerCleared === "true" &&
                    transition.dataset.threadTransitionCompact === "true" &&
                    transition.dataset.threadTransitionConversationId === targetConversationId &&
                    threadPhase &&
                    threadPhase.hidden &&
                    threadPhase.dataset.liveSessionOwned === "false" &&
                    threadSessionSummary &&
                    threadSessionSummary.hidden &&
                    threadTitle &&
                    threadTitle.textContent.trim().length > 0 &&
                    threadTitle.textContent.trim() !== "새 대화를 시작하세요" &&
                    activeSessionRow &&
                    !activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "thread-transition" &&
                    activeSessionRow.dataset.activeSessionState === "switching" &&
                    activeSessionRow.dataset.activeSessionPhase === "SWITCHING" &&
                    activeSessionRow.dataset.activeSessionConversationId === targetConversationId &&
                    activeSessionRow.dataset.activeSessionFollow === "attach" &&
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
                    composerUtilityMenu &&
                    composerUtilityMenu.dataset.composerUtilityOpen === "false" &&
                    composerUtilityMenu.dataset.composerUtilityState === "closed" &&
                    composerUtilityToggle &&
                    composerUtilityToggle.dataset.composerUtilityOpen === "false" &&
                    composerUtilityToggle.dataset.composerUtilityState === "closed" &&
                    composerUtilityToggle.getAttribute("aria-expanded") === "false" &&
                    composerUtilityCluster &&
                    composerUtilityCluster.hidden &&
                    composerUtilityCluster.dataset.composerUtilityOpen === "false" &&
                    composerUtilityCluster.dataset.composerUtilityState === "closed" &&
                    composerUtilityCluster.getAttribute("aria-hidden") === "true" &&
                    secondarySessionFacts &&
                    secondarySessionFacts.dataset.secondaryFactsPresentation === "switching" &&
                    secondarySessionFacts.dataset.secondaryFactsOwned === "false" &&
                    secondarySessionFacts.dataset.secondaryFactsTransport === "ATTACH" &&
                    secondarySessionFacts.dataset.secondaryFactsPhase === "SWITCHING" &&
                    sessionStrip.dataset.phaseValue === "UNKNOWN" &&
                    sessionStrip.dataset.phaseAuthoritative === "false" &&
                    sessionStrip.dataset.phaseProvenance === "thread-transition" &&
                    composerOwnerRow &&
                    composerOwnerRow.hidden &&
                    composerOwnerRow.dataset.composerOwnerMerged === "true" &&
                    composerOwnerRow.dataset.composerOwner === "switching" &&
                    composerOwnerRow.dataset.composerOwnerConversationId === targetConversationId &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    sendRequest &&
                    sendRequest.dataset.composerOwnerState === "switching" &&
                    sendRequest.dataset.composerOwnerConversationId === targetConversationId &&
                    threadScroller &&
                    threadScroller.dataset.threadTransitionState === "switching" &&
                    threadScroller.dataset.threadTransitionConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspacePlaceholder === "conversation" &&
                    document.querySelector("#conversation-timeline").dataset.workspacePlaceholder !== "empty" &&
                    document.querySelector("#conversation-timeline").dataset.workspaceConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.phaseValue === "UNKNOWN" &&
                    threadScroller.dataset.phaseAuthoritative === "false" &&
                    threadScroller.dataset.phaseProvenance === "thread-transition" &&
                    threadScroller.dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.sessionOwner !== "selected-thread" &&
                    !document.querySelector("#jump-to-latest") &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0 &&
                    switchMonitor.active === true &&
                    switchMonitor.targetConversationId === targetConversationId &&
                    switchMonitor.sawEmptyState === false &&
                    switchMonitor.maxTransitionCount === 1 &&
                    switchMonitor.sawHiddenComposerDock === false &&
                    switchMonitor.sawClearedWorkspacePlaceholder === false &&
                    inlineBlocks.length === 0 &&
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
                  window.__verifyStartSwitchMonitor(switchConversationId);
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
                  const switchMonitor = window.__verifySwitchMonitor || {};
                  return Boolean(
                    transition &&
                    document.querySelectorAll('[data-thread-transition="switching"]').length === 1 &&
                    transition.dataset.threadTransitionOwnerCleared === "true" &&
                    transition.dataset.threadTransitionCompact === "true" &&
                    transition.dataset.threadTransitionConversationId === targetConversationId &&
                    activeSessionRow &&
                    !activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "thread-transition" &&
                    activeSessionRow.dataset.activeSessionState === "switching" &&
                    activeSessionRow.dataset.activeSessionPhase === "SWITCHING" &&
                    activeSessionRow.dataset.activeSessionConversationId === targetConversationId &&
                    activeSessionRow.dataset.activeSessionFollow === "attach" &&
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
                    document.querySelector("#conversation-timeline").dataset.workspacePlaceholder === "conversation" &&
                    document.querySelector("#conversation-timeline").dataset.workspaceConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.workspaceOwnerCleared === "true" &&
                    switchMonitor.active === true &&
                    switchMonitor.targetConversationId === targetConversationId &&
                    switchMonitor.sawEmptyState === false &&
                    switchMonitor.maxTransitionCount === 1 &&
                    switchMonitor.sawHiddenComposerDock === false &&
                    switchMonitor.sawClearedWorkspacePlaceholder === false &&
                    !empty
                  );
                }""",
                switch_conversation_id,
                timeout=30000,
            )
            page.evaluate(
                """targetConversationId => {
                  window.__verifyStartSwitchMonitor(targetConversationId);
                  window.__verifyFetchMark = window.__verifyFetchLog.length;
                }""",
                conversation_id,
            )
            page.click(f'[data-conversation-id="{conversation_id}"]')
            page.wait_for_function(
                """([appId, targetConversationId]) => {
                  const transition = document.querySelector('[data-thread-transition="switching"]');
                  const sessionStrip = document.querySelector("#session-strip");
                  const sessionStripState = document.querySelector("#session-strip-state");
                  const threadScroller = document.querySelector("#thread-scroller");
                  const composerDock = document.querySelector("#conversation-footer-dock");
                  const threadPhase = document.querySelector("#thread-phase-chip");
                  const activeSessionRow = document.querySelector("#active-session-row");
                  const secondarySessionFacts = document.querySelector("#secondary-session-facts");
                  const empty = document.querySelector(".timeline-empty");
                  const inlineBlocks = document.querySelectorAll('.session-inline-block[data-selected-thread-live-block="true"], .session-inline-block[data-selected-thread-degraded-block="true"]');
                  const degraded = document.querySelector('.timeline-item.live-activity[data-live-activity-turn="true"][data-live-owned="false"]');
                  const fetchMark = Number(window.__verifyFetchMark || 0);
                  const jobFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes("/api/jobs/")
                  );
                  const goalsFetches = (window.__verifyFetchLog || []).slice(fetchMark).filter(
                    entry => String(entry.url || "").includes(`/api/apps/${appId}/goals`)
                  );
                  const switchMonitor = window.__verifySwitchMonitor || {};
                  return Boolean(
                    transition &&
                    document.querySelectorAll('[data-thread-transition="switching"]').length === 1 &&
                    transition.dataset.threadTransitionOwnerCleared === "true" &&
                    transition.dataset.threadTransitionCompact === "true" &&
                    transition.dataset.threadTransitionConversationId === targetConversationId &&
                    sessionStrip &&
                    !sessionStrip.hidden &&
                    !document.querySelector("#jump-to-latest") &&
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
                    document.querySelector("#conversation-timeline").dataset.workspacePlaceholder === "conversation" &&
                    document.querySelector("#conversation-timeline").dataset.workspaceConversationId === targetConversationId &&
                    document.querySelector("#conversation-timeline").dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.workspaceOwnerCleared === "true" &&
                    threadScroller.dataset.sessionOwner !== "selected-thread" &&
                    threadPhase &&
                    threadPhase.hidden &&
                    threadPhase.dataset.liveSessionOwned === "false" &&
                    threadSessionSummary &&
                    threadSessionSummary.hidden &&
                    visibleConversationOwnerRows.length === 0 &&
                    selectedCardLiveOwnerRow &&
                    selectedCardLiveOwnerRow.hidden &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerVisible === "false" &&
                    selectedCardLiveOwnerRow.dataset.liveOwnerState === "idle" &&
                    activeSessionRow &&
                    !activeSessionRow.hidden &&
                    activeSessionRow.dataset.activeSessionOwned === "false" &&
                    activeSessionRow.dataset.activeSessionSource === "thread-transition" &&
                    activeSessionRow.dataset.activeSessionState === "switching" &&
                    activeSessionRow.dataset.activeSessionPhase === "SWITCHING" &&
                    activeSessionRow.dataset.activeSessionConversationId === targetConversationId &&
                    activeSessionRow.dataset.activeSessionFollow === "attach" &&
                    secondarySessionFacts &&
                    secondarySessionFacts.dataset.secondaryFactsPresentation === "switching" &&
                    secondarySessionFacts.dataset.secondaryFactsOwned === "false" &&
                    composerDock &&
                    ["sticky", "fixed"].includes(getComputedStyle(composerDock).position) &&
                    follow &&
                    follow.dataset.followOwned !== "selected-thread" &&
                    inlineBlocks.length === 0 &&
                    !degraded &&
                    !empty &&
                    switchMonitor.active === true &&
                    switchMonitor.targetConversationId === targetConversationId &&
                    switchMonitor.sawEmptyState === false &&
                    switchMonitor.maxTransitionCount === 1 &&
                    switchMonitor.sawHiddenComposerDock === false &&
                    switchMonitor.sawClearedWorkspacePlaceholder === false &&
                    jobFetches.length === 0 &&
                    goalsFetches.length === 0
                  );
                }""",
                [app_id, conversation_id],
                timeout=30000,
            )
            cancelled_switch_snapshot = page.evaluate(browser_snapshot_script())
            return {
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


def wait_for_conversation_ready(
    base_url: str,
    conversation_id: str,
    api_key: str,
    *,
    timeout_seconds: float = 420.0,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        payload = http_json("GET", f"{base_url}/api/conversations/{conversation_id}", api_key=api_key)
        event_types = [str(event.get("type", "")) for event in payload.get("events", [])]
        for forbidden in ("codex.exec.retrying", "runtime.exception"):
            if forbidden in event_types:
                raise RuntimeError(f"unexpected degraded event: {forbidden}")
        if "job.failed" in event_types:
            raise RuntimeError("selected-thread conversation failed before proposal.ready")
        if "proposal.ready" in event_types:
            return payload
        time.sleep(2)
    raise RuntimeError(f"timed out waiting for selected-thread proposal.ready on conversation {conversation_id}")


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
    require_absent(html, 'id="session-summary-row"', label="removed session summary row")
    require_absent(html, 'id="recent-thread-rail"', label="removed recent-thread rail")
    require_absent(html, 'id="recent-thread-rail-list"', label="removed recent-thread rail list")
    require_absent(html, 'id="session-live-indicator"', label="removed session live indicator")
    require_absent(html, 'id="session-summary-path"', label="removed session summary path")
    require_absent(html, 'id="session-summary-state"', label="removed session summary state")
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
    require(html, 'id="secondary-session-facts"', label="secondary panel session facts")
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
    require(render_js, 'dom.composerUtilityMenu.dataset.composerUtilityOpen = "false";', label="composer utility closes on non-healthy render")
    require(render_js, 'dom.composerUtilityCluster.hidden = true;', label="composer utility cluster hides on non-healthy render")
    require(render_js, 'dom.composerUtilityToggle.setAttribute("aria-expanded", "false");', label="composer utility toggle aria closes on non-healthy render")
    require_absent(styles, ".session-summary-row", label="removed session summary row CSS")
    require_absent(styles, ".recent-thread-rail", label="removed recent-thread rail CSS")
    require_absent(styles, ".recent-thread-rail-list", label="removed recent-thread rail list CSS")
    require_absent(styles, ".recent-thread-chip", label="removed recent-thread chip CSS")
    require_absent(styles, ".session-live-indicator", label="removed session live indicator CSS")
    require(styles, ".composer-owner-row", label="composer owner row CSS")
    require(styles, ".composer-owner-chip", label="composer owner chip CSS")
    require(styles, ".autonomy-detail-card", label="secondary panel autonomy detail card CSS")
    require(styles, ".secondary-session-facts", label="secondary panel session facts CSS")
    require(styles, ".secondary-session-chip-row", label="secondary panel session chip row CSS")
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
    require(render_js, "renderSecondaryPanelSessionFacts", label="secondary panel session facts helper")
    require(render_js, "secondaryPanelSessionFactsModel", label="secondary panel session facts model")
    require(render_js, 'dom.secondarySessionFacts.hidden = facts.presentation === "suppressed";', label="secondary panel facts healthy suppression")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsPresentation = facts.presentation;', label="secondary panel facts presentation dataset")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsOwned = facts.owned ? "true" : "false";', label="secondary panel facts ownership dataset")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsTransport = facts.transport;', label="secondary panel facts transport dataset")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsPhase = facts.phase;', label="secondary panel facts phase dataset")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsPath = facts.path;', label="secondary panel facts path dataset")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsVerifier = facts.verifier;', label="secondary panel facts verifier dataset")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsBlocker = facts.blocker;', label="secondary panel facts blocker dataset")
    require(render_js, 'dom.secondarySessionFacts.dataset.secondaryFactsFollow = facts.follow;', label="secondary panel facts follow dataset")
    require(render_js, "syncExecutionStatusSurface", label="execution status surface helper")
    require(render_js, 'statusCard.hidden = suppressed;', label="execution card hidden helper")
    require(render_js, 'statusCard.dataset.executionSurface = suppressed ? "suppressed" : "secondary-detail";', label="execution card surface dataset")
    require(render_js, 'statusCard.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="execution card center-timeline authority dataset")
    require(render_js, 'statusCard.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="execution card center-timeline presentation dataset")
    require(render_js, 'dom.statusOutput.dataset.surface = suppressed ? "suppressed" : "secondary-detail";', label="status output surface dataset")
    require(render_js, 'dom.statusOutput.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="status output center-timeline authority dataset")
    require(render_js, 'dom.statusOutput.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="status output center-timeline presentation dataset")
    require(render_js, 'dom.jobEvents.dataset.surface = suppressed ? "suppressed" : "secondary-detail";', label="job events surface dataset")
    require(render_js, 'dom.jobEvents.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="job events center-timeline authority dataset")
    require(render_js, 'dom.jobEvents.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="job events center-timeline presentation dataset")
    require(render_js, 'dom.jobPhase.dataset.surface = suppressed ? "suppressed" : "secondary-detail";', label="job phase surface dataset")
    require(render_js, 'dom.jobPhase.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="job phase center-timeline authority dataset")
    require(render_js, 'dom.jobPhase.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="job phase center-timeline presentation dataset")
    require(render_js, 'dom.jobMeta.dataset.surface = suppressed ? "suppressed" : "secondary-detail";', label="job meta surface dataset")
    require(render_js, 'dom.jobMeta.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="job meta center-timeline authority dataset")
    require(render_js, 'dom.jobMeta.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="job meta center-timeline presentation dataset")
    require(render_js, "if (inlineState.visible) {", label="composer strip suppression guard")
    require(render_js, "renderInlineSessionBlock", label="inline session block helper")
    require(render_js, "const provisionalVisible = sessionStatus.presentation === \"provisional\";", label="inline provisional visibility helper")
    require(render_js, 'data-selected-thread-live-block="true"', label="inline session block live dataset")
    require(render_js, 'data-live-block-provisional="${provisionalVisible ? "true" : "false"}"', label="inline session block provisional dataset")
    require(render_js, 'data-live-block-phase="${escapeHtml(phaseLabel)}"', label="inline session block phase dataset")
    require(render_js, 'data-live-block-transport="${escapeHtml(transportLabel)}"', label="inline session block transport dataset")
    require(render_js, 'if (handoffVisible || inlineState.liveVisible) {', label="transcript live activity suppression behind inline block")
    require(render_js, "INLINE_TERMINAL_RETENTION_MS = 12000", label="inline terminal retention window")
    require(render_js, "shouldRetainInlineTerminalPhase", label="inline terminal retention helper")
    require(render_js, "selectedThreadTimelineAuthorityModel", label="timeline authority model helper")
    require(render_js, 'authority.state === "provisional"', label="provisional authority presentation branch")
    require(render_js, "renderThreadTransition", label="thread transition helper")
    require(render_js, "function renderThreadTransition(currentState, sessionStatus = deriveSelectedThreadSessionStatus(currentState, null))", label="thread transition canonical status signature")
    require(render_js, "pendingHandoffState", label="pending handoff helper")
    require(render_js, "function sessionCompactTarget(", label="compact selected-thread target helper")
    require(render_js, 'data-thread-transition="switching"', label="thread transition DOM")
    require(render_js, 'data-thread-transition-source="selected-thread-session"', label="thread transition source dataset")
    require(render_js, 'data-thread-transition-phase="switching"', label="thread transition phase dataset")
    require(render_js, 'data-thread-transition-owner-cleared="true"', label="thread transition ownership-cleared dataset")
    require(render_js, 'data-thread-transition-live-strip-cleared="true"', label="thread transition live-strip-cleared dataset")
    require(render_js, 'data-thread-transition-compact="true"', label="thread transition compact dataset")
    require(render_js, 'class="timeline-transition-target"', label="thread transition compact target label")
    require(render_js, 'data-thread-transition-owner-cleared="true"', label="thread transition ownership-cleared dataset")
    require(render_js, "selectedThreadWorkspacePlaceholder", label="thread transition workspace placeholder helper")
    require(render_js, "const workspacePlaceholder = selectedThreadWorkspacePlaceholder(currentState);", label="thread transition workspace placeholder state")
    require(render_js, "if (isSwitching) {", label="switch placeholder branch")
    require(render_js, "if (isRestore) {", label="restore placeholder branch")
    require(render_js, 'workspaceSummary: "selected thread switching · target snapshot attach pending",', label="switch workspace summary copy")
    require(render_js, 'workspaceSummary: sessionStatus.restoreResume', label="restore workspace summary copy")
    require(render_js, 'workspaceSummary: "선택된 대화가 없으면 현재 세션 맥락이 여기에 정리됩니다.",', label="empty workspace summary copy")
    require(render_js, 'dom.conversationTimeline.dataset.workspacePlaceholder = "conversation";', label="workspace placeholder mode dataset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceConversationId = workspacePlaceholder.conversationId;', label="workspace placeholder conversation dataset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = isThreadTransition || isSavedRestore ? "true" : "false";', label="workspace placeholder ownership-cleared dataset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = isThreadTransition || isSavedRestore ? "true" : "false";', label="workspace placeholder ownership-cleared dataset")
    require(render_js, 'dom.conversationTimeline.innerHTML = workspacePlaceholder.timeline;', label="thread transition placeholder render path")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholder = "conversation";', label="thread scroller placeholder mode dataset")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholderConversationId = workspacePlaceholder.conversationId;', label="thread scroller placeholder conversation dataset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = isThreadTransition || isSavedRestore ? "true" : "false";', label="thread scroller ownership-cleared dataset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = isThreadTransition || isSavedRestore ? "true" : "false";', label="thread scroller ownership-cleared dataset")
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
    require(render_js, 'dom.conversationTimeline.dataset.liveSessionStripVisible = "false";', label="workspace placeholder clears center strip visibility")
    require(render_js, 'dom.threadScroller.dataset.liveSessionStripClearReason = sessionStripModel.clearReason || (isThreadTransition ? "thread-switch" : "deselected");', label="workspace placeholder center strip clear reason dataset")
    require(render_js, 'dom.conversationTimeline.dataset.liveSessionStripVisible = sessionStripModel.visible ? "true" : "false";', label="conversation center strip visibility dataset")
    require(render_js, 'dom.threadScroller.dataset.liveSessionStripOwned = sessionStripModel.owned ? "true" : "false";', label="thread scroller center strip ownership dataset")
    require(styles, ".timeline-transition-target", label="thread transition compact target CSS")
    require(render_js, 'renderSessionStrip(dom, currentState, null);', label="thread transition composer shell render path")
    require(render_js, 'syncComposerOwnership(dom, currentState, null);', label="thread transition composer owner switching path")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholder = "conversation";', label="conversation scroller placeholder reset")
    require(render_js, 'dom.threadScroller.dataset.workspacePlaceholderConversationId = String(conversation.conversation_id || "");', label="conversation scroller placeholder conversation reset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = "false";', label="conversation workspace ownership-cleared reset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = "false";', label="conversation scroller ownership-cleared reset")
    require(render_js, 'dom.conversationTimeline.dataset.workspaceOwnerCleared = "false";', label="conversation workspace ownership-cleared reset")
    require(render_js, 'dom.threadScroller.dataset.workspaceOwnerCleared = "false";', label="conversation scroller ownership-cleared reset")
    require(render_js, "const { handoffVisible, degradedVisible, sessionIndicator } = inlineState;", label="transcript live state wiring")
    require(conversations_js, "function normalizeSessionStatus(payload = {}, overrides = {}) {", label="session-status normalizer helper")
    require(conversations_js, 'state.appendStream.sessionStatus = normalizeSessionStatus(appendEnvelope.session_status || {}, {', label="append envelope session-status hydration")
    require(conversations_js, 'state.appendStream.sessionStatus = normalizeSessionStatus(payload.session_status || {}, {', label="bootstrap session-status hydration")
    require(conversations_js, 'goalTitle: String(payload?.goal_title || payload?.goalTitle || "Autonomy Goal"),', label="session-status goal title normalization")
    require(conversations_js, 'goalStatus: String(payload?.goal_status || payload?.goalStatus || "unknown"),', label="session-status goal status normalization")
    require(conversations_js, 'iteration: String(payload?.iteration || ""),', label="session-status iteration normalization")
    require(conversations_js, 'heading: String(payload?.heading || "").trim(),', label="session-status heading normalization")
    require(conversations_js, 'freshnessState: String(payload?.freshness_state || payload?.freshnessState || "stale-or-missing").toLowerCase(),', label="session-status freshness normalization")
    require(conversations_js, 'fallbackAllowed: Boolean(payload?.fallback_allowed ?? payload?.fallbackAllowed ?? true),', label="session-status fallback normalization")
    require(store_js, "export function deriveSelectedThreadSessionStripModel(currentState, conversation = null, liveRun = null) {", label="selected-thread session strip model helper")
    require_absent(render_js, 'data-live-session-strip="true"', label="selected-thread session strip DOM")
    require_absent(render_js, 'data-session-event-source="session-status"', label="canonical inline session-event source dataset")
    require_absent(render_js, 'if (sessionStrip.visible) {', label="transcript live activity suppression behind strip")
    require(render_js, 'if (item.pending_assistant && inlineState.handoffVisible) {', label="pending assistant placeholder suppression behind inline block")
    require_absent(render_js, 'data-live-autonomy="true"', label="inline autonomy DOM")
    require(render_js, 'data-live-reason="${escapeHtml(', label="transcript live reason dataset")
    require(render_js, 'data-live-transport="${escapeHtml(transportLabel)}"', label="transcript live transport dataset")
    require(render_js, 'data-live-transport-owned="${liveOwned ? "true" : "false"}"', label="transcript live transport ownership dataset")
    require(render_js, 'data-live-expected-path="${escapeHtml(expectedPath)}"', label="transcript live expected-path dataset")
    require(render_js, 'data-thread-transition-transport="${escapeHtml(transportLabel)}"', label="restore transition transport dataset")
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
    require(render_js, 'dom.composerOwnerRow.dataset.composerRestoreStage = "none";', label="composer owner restore stage dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.restoreStage = sessionStatus.restoreStage || "none";', label="header summary restore stage dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.restorePath = sessionStatus.restorePath || "none";', label="header summary restore path dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.restoreProvenance = sessionStatus.restoreProvenance || "none";', label="header summary restore provenance dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="header summary center-timeline authority dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="header summary center-timeline presentation dataset")
    require(render_js, 'dom.threadPhaseChip.hidden = true;', label="header badge forced hidden")
    require(api_runtime_context_py, '"goal_title": str(autonomy_summary.get("goal_title") or autonomy_summary.get("goalTitle") or "Autonomy Goal"),', label="runtime session-status goal title emission")
    require(api_runtime_context_py, '"goal_status": str(autonomy_summary.get("goal_status") or autonomy_summary.get("goalStatus") or "unknown"),', label="runtime session-status goal status emission")
    require(api_runtime_context_py, '"iteration": str(autonomy_summary.get("iteration") or ""),', label="runtime session-status iteration emission")
    require(api_runtime_context_py, '"heading": str(', label="runtime session-status heading emission")
    require(api_runtime_context_py, '"freshness_state": str(', label="runtime session-status freshness emission")
    require(api_runtime_context_py, '"fallback_allowed": bool(', label="runtime session-status fallback emission")
    require(content, "__verifyStartSwitchMonitor", label="switch monitor start helper")
    require(content, "__verifySwitchMonitor", label="switch monitor state")
    require(content, "switchMonitor.sawEmptyState === false", label="switch monitor no empty-state flash assertion")
    require(content, "switchMonitor.maxTransitionCount === 1", label="switch monitor single placeholder assertion")
    require(content, "switchMonitor.sawHiddenComposerDock === false", label="switch monitor composer continuity assertion")
    require(content, "switchMonitor.sawClearedWorkspacePlaceholder === false", label="switch monitor placeholder persistence assertion")
    require(render_js, 'label: "ATTACH"', label="composer strip attach label")
    require(render_js, 'label: "SNAPSHOT"', label="composer strip snapshot label")
    require(store_js, 'transportLabel = "POLLING";', label="composer strip polling label")
    require(store_js, 'transportLabel = "RECONNECT";', label="composer strip reconnect label")
    require(render_js, "dataset.followState", label="follow-state dataset")
    require(render_js, "function isSessionAuthorityEvent(event)", label="selected-thread session authority event helper")
    require(render_js, "function selectedThreadSseAuthorityEvent(conversation, currentState)", label="selected-thread SSE authority event selector")
    require(render_js, "function selectedThreadSseAuthorityStatus(conversation, currentState)", label="selected-thread SSE authority status helper")
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
    require(render_js, "const sessionStrip = deriveSelectedThreadSessionStripModel(currentState, conversation, liveRun);", label="selected-thread session strip apply authority")
    require(render_js, 'sessionStrip?.owned && (sessionStrip.proposalReady || sessionStrip.proposalStatus === "ready_to_apply")', label="session-strip proposal readiness apply guard")
    require(render_js, "updateProposalButton(dom, currentState.latestProposalJobId);", label="apply button updated from selected-thread live state")
    require(render_js, "dataset.liveSessionState", label="live-session state dataset")
    require(render_js, "dataset.liveSessionSource", label="live-session source dataset")
    require(render_js, "dataset.liveSessionReason", label="live-session reason dataset")
    require(render_js, "dataset.liveSessionOwned", label="live-session owned dataset")
    require(render_js, "renderRestoreSessionTimeline", label="restore transcript timeline helper")
    require(render_js, 'data-thread-transition-restore-stage="${escapeHtml(String(sessionStatus.restoreStage || "none"))}"', label="restore transition stage dataset")
    require(render_js, 'data-thread-transition-restore-path="${escapeHtml(String(sessionStatus.restorePath || "none"))}"', label="restore transition path dataset")
    require(render_js, 'data-thread-transition-restore-provenance="${escapeHtml(String(sessionStatus.restoreProvenance || "none"))}"', label="restore transition provenance dataset")
    require(render_js, "syncAutonomyDetailSurface", label="secondary autonomy surface sync helper")
    require(render_js, "deriveSelectedThreadLiveAutonomy", label="selected-thread live autonomy render helper import")
    require(render_js, 'autonomyCard.hidden = false;', label="selected-thread live autonomy card suppression")
    require(render_js, 'autonomyCard.dataset.autonomySurface = suppressed ? "suppressed" : "secondary-detail";', label="autonomy card surface dataset")
    require(render_js, 'autonomyCard.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="autonomy card center-timeline authority dataset")
    require(render_js, 'autonomyCard.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="autonomy card center-timeline presentation dataset")
    require(render_js, 'dom.autonomyDetail.dataset.surface = suppressed ? "suppressed" : "secondary-detail";', label="autonomy detail surface dataset")
    require(render_js, 'dom.autonomyDetail.dataset.centerTimelineAuthority = timelineAuthority.visible ? "true" : "false";', label="autonomy detail center-timeline authority dataset")
    require(render_js, 'dom.autonomyDetail.dataset.centerTimelinePresentation = timelineAuthority.presentation;', label="autonomy detail center-timeline presentation dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionSource = summaryVisible ? badgeSource : "none";', label="header summary live source dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionOwned = summaryVisible && authority.owned ? "true" : "false";', label="header summary ownership dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionReason = summaryVisible ? badgeReason : "idle";', label="header summary reason dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionPresentation = summaryVisible ? badgePresentation : "cleared";', label="header summary presentation dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionVisible = summaryVisible ? "true" : "false";', label="header summary visible dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionStateLabel = summaryVisible ? badgeStateLabel : "";', label="header summary state label dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionProvenance = summaryVisible ? badgeSource : "none";', label="header summary provenance dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionPhase = summaryVisible ? healthyPhaseLabel : "";', label="header summary phase dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.liveSessionDetail = summaryVisible ? badgeDetail : "현재 활성 세션이 없습니다.";', label="header summary detail dataset")
    require(render_js, "const healthyTranscriptAuthority =", label="healthy transcript authority header suppression guard")
    require(render_js, "const provisionalTranscriptAuthority =", label="header session summary provisional suppression helper")
    require(render_js, "const summaryVisible = authority.summaryVisible && !healthyTranscriptAuthority && !provisionalTranscriptAuthority;", label="header session summary healthy suppression")
    require(render_js, "dom.threadSessionSummary.hidden = !summaryVisible;", label="header session summary visibility")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryVisible = summaryVisible ? "true" : "false";', label="header session summary visible dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryPresentation = summaryVisible ? badgePresentation : "cleared";', label="header session summary presentation dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryScope = summaryVisible ? "selected-thread" : "";', label="header session summary scope dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryPath = summaryVisible ? summaryPath : "";', label="header session summary path dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryOwner = summaryVisible ? summaryOwner : "";', label="header session summary owner dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryPhase = summaryVisible ? healthyPhaseLabel : "";', label="header session summary phase dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummarySource = summaryVisible ? badgeSource : "none";', label="header session summary source dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryOwned = summaryVisible && authority.owned ? "true" : "false";', label="header session summary ownership dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryConversationId = summaryVisible ? conversationId : "";', label="header session summary conversation dataset")
    require(render_js, 'dom.threadSessionSummary.dataset.threadSummaryReason = summaryVisible ? badgeReason : "idle";', label="header session summary reason dataset")
    require(render_js, 'dom.threadSessionSummaryOwner.textContent = summaryOwner;', label="header session summary owner chip copy")
    require(render_js, 'const badgeStateLabel =', label="header badge path-state helper")
    require(render_js, 'const badgeDetail =', label="header badge detail helper")
    require(render_js, 'const healthyPhaseLabel = String(', label="header healthy phase label helper")
    require(store_js, 'transportLabel = "RECONNECT";', label="live-session reconnect label")
    require(store_js, 'transportLabel = "POLLING";', label="live-session polling label")
    require(render_js, "joinSessionChromeTokens", label="session chrome token join helper")
    require(render_js, "sessionFollowLabel", label="session follow token helper")
    require(render_js, 'const followPhaseLabel = footerDock?.phaseLabel || ownerState.label || "READY";', label="footer follow phase label helper")
    require(render_js, "proposalStatusLabel", label="session proposal status token helper")
    require(render_js, "sessionChromeCopy", label="session summary chrome copy helper")
    require(render_js, "sessionStripDetailCopy", label="session strip detail copy helper")
    require(render_js, "sessionStripStateChipMarkup", label="session strip chip markup helper")
    require(render_js, "sessionStripStateRow", label="session strip single-row state helper")
    require(render_js, "selectedThreadFooterDockModel", label="footer session dock helper")
    require(store_js, "export function deriveSelectedThreadSessionSurfaceModel", label="selected-thread session surface helper")
    require(render_js, "const sessionSurface = deriveSelectedThreadSessionSurfaceModel(currentState, conversation);", label="shared selected-thread session surface wiring")
    require(render_js, 'const liveOwned = Boolean(sessionSurface.liveOwned && sessionSurface.source === "sse");', label="footer dock shared live ownership wiring")
    require(render_js, 'const phaseLabel = String(sessionSurface.phaseLabel || deriveSelectedThreadShellPhaseLabel(currentState, conversation) || liveRun?.phase || "LIVE").toUpperCase();', label="footer dock shared phase label wiring")
    require(render_js, 'source: String(sessionSurface.milestoneModel.source || sessionSurface.source || "sse").toLowerCase(),', label="footer dock shared source wiring")
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
    require(render_js, 'dom.sessionStrip.hidden = !sessionConversationId;', label="composer strip selected-target visibility")
    require(render_js, 'dom.sessionStrip.dataset.sessionOwner = selectedFooterLaneVisible ? "selected-thread" : "none";', label="composer strip selected-thread owner dataset")
    require(render_js, 'dom.sessionStrip.dataset.sessionPresentation = presentation;', label="composer strip presentation dataset")
    require(render_js, 'dom.sessionStrip.dataset.followState = footerFollow.visible ? footerFollow.followState : stripLiveOwned ? sessionStatus.followState || "live" : transportState.owned ? "owned" : "idle";', label="composer strip follow-state dataset")
    require(render_js, 'dom.sessionStrip.dataset.followCount = String(footerFollow.visible ? footerFollow.unseenCount : 0);', label="composer strip follow-count dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockOwned = stripProgressOwned ? "true" : "false";', label="composer strip footer-dock ownership dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockPhase = footerDock.phaseLabel || "IDLE";', label="composer strip footer-dock phase dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockSource = footerDock.source || "none";', label="composer strip footer-dock source dataset")
    require(render_js, 'dom.sessionStrip.dataset.footerDockMilestones = footerDock.visible && footerDock.chips.length > 1 ? "true" : "false";', label="composer strip footer-dock milestone dataset")
    require(render_js, 'dom.sessionStrip.dataset.composerTransportOwned = stripLiveOwned ? "true" : "false";', label="composer strip transport ownership dataset")
    require(render_js, 'dom.sessionStripState.hidden = false;', label="composer strip state visible on healthy path")
    require(render_js, 'dom.sessionStripState.dataset.sessionStripRole = stripState.role;', label="composer strip state role dataset")
    require(render_js, 'dom.sessionStripState.dataset.sessionStripLabel = stripState.label;', label="composer strip state label dataset")
    require(render_js, 'dom.sessionStripState.dataset.sessionStripTone = stripState.tone;', label="composer strip state tone dataset")
    require(render_js, 'dom.sessionStripMeta.hidden = false;', label="footer strip target visibility")
    require(render_js, 'dom.sessionStripMeta.textContent = ownerState.target;', label="composer strip target copy")
    require(render_js, 'label: "SWITCHING",', label="composer strip switching row")
    require(render_js, 'label: "TARGET",', label="composer strip context row")
    require(render_js, 'label: transportState.label,', label="composer strip degraded phase row")
    require(render_js, "chips: footerDock.chips,", label="composer strip footer-dock chip row")
    require(render_js, 'dom.sessionStripState.innerHTML = sessionStripStateChipMarkup(stripState.chips || stripState);', label="composer strip chip render")
    require(render_js, 'dom.sessionStripDetail.hidden = false;', label="footer strip detail visibility")
    require(render_js, 'dom.sessionStripDetail.textContent = footerDock.visible', label="composer strip footer-dock detail copy")
    require(render_js, '!handoffVisible && !degradedVisible && (!phaseProgression.visible || !liveAutonomy.visible)', label="transcript live activity unified visibility guard")
    require(render_js, "const { liveAutonomy, phaseProgression, milestoneModel } = sessionSurface;", label="transcript live activity shared session surface destructuring")
    require(render_js, 'const phaseLabel = degradedVisible', label="transcript live activity unified phase label")
    require(render_js, 'String(sessionSurface.phaseLabel || phaseProgression.label || liveRun.phase || "LIVE").toUpperCase();', label="transcript live activity shared phase label wiring")
    require(render_js, 'const provenanceLabel = degradedVisible', label="transcript live activity unified provenance label")
    require(render_js, 'const pathVerdict = liveOwned ? sessionSurface.pathVerdict : "";', label="transcript live activity shared path verdict wiring")
    require(render_js, 'const verifierAcceptability = liveOwned ? sessionSurface.verifierAcceptability : "";', label="transcript live activity shared verifier wiring")
    require(render_js, 'const blockerReason = liveOwned ? sessionSurface.blockerReason : "";', label="transcript live activity shared blocker wiring")
    require(render_js, 'const mergedIntoStrip = Boolean(dom.sessionStrip && !dom.sessionStrip.hidden && owner.conversationId);', label="composer owner merged strip guard")
    require(render_js, 'dom.composerOwnerRow.dataset.composerOwnerMerged = mergedIntoStrip ? "true" : "false";', label="composer owner merged dataset")
    require(render_js, 'dom.composerOwnerRow.hidden = mergedIntoStrip || owner.state === "idle";', label="composer owner row hidden when merged")
    require(render_js, 'dom.sessionStrip.dataset.footerSurface = !sessionConversationId', label="footer strip merged surface dataset")
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
    require(render_js, "selectedThreadPrimaryTimelineSessionModel", label="primary selected-thread timeline session helper")
    require(render_js, 'data-live-session-primary="true"', label="transcript primary session surface dataset")
    require(render_js, "shouldCollapseSelectedThreadSessionEvent", label="selected-thread transcript session-event collapse helper")
    require(render_js, "renderTranscriptMilestones", label="transcript live milestone helper")
    require(render_js, "const transcriptLiveActivity = renderTranscriptLiveActivity(conversation, currentState, liveRun);", label="transcript live activity wiring")
    require(render_js, "if (inlineState.visible) {", label="transcript live activity suppression guard")
    require(render_js, 'data-live-session-event="${liveOwned ? "true" : "false"}"', label="transcript session event lane dataset")
    require(render_js, 'data-live-session-duplicates="${collapseSessionEvents ? "collapsed" : "allowed"}"', label="transcript session-event collapse dataset")
    require(render_js, 'data-live-session-lane="${escapeHtml(liveOwned ? "selected-thread" : degradedVisible ? "degraded" : handoffVisible ? "handoff" : "fallback")}"', label="transcript session lane ownership dataset")
    require(render_js, 'data-live-milestones-visible="${liveOwned && milestoneModel.visible ? "true" : "false"}"', label="transcript session event milestone visibility dataset")
    require(render_js, 'data-live-milestones-phase="${escapeHtml(liveOwned ? String(milestoneModel.currentLabel || phaseLabel) : "")}"', label="transcript session event milestone phase dataset")
    require(render_js, 'data-live-path-verdict="${escapeHtml(pathVerdict)}"', label="transcript session lane path verdict dataset")
    require(render_js, 'data-live-verifier-acceptability="${escapeHtml(verifierAcceptability)}"', label="transcript session lane verifier dataset")
    require(render_js, 'data-live-blocker-reason="${escapeHtml(blockerReason)}"', label="transcript session lane blocker dataset")
    require(render_js, 'data-live-milestones="true"', label="transcript live milestone dataset")
    require(render_js, 'timeline-live-row timeline-live-row-milestones', label="transcript milestone row class")
    require(render_js, '<span class="timeline-live-chip" data-tone="neutral">SELECTED</span>', label="transcript selected scope chip")
    require(render_js, '${escapeHtml(transportLabel)}', label="transcript transport owner chip")
    require(render_js, 'data-milestone-key="${escapeHtml(item.key)}"', label="transcript milestone key dataset")
    require(render_js, 'data-milestone-state="${escapeHtml(item.state)}"', label="transcript milestone state dataset")
    require(render_js, 'data-session-event="true"', label="session timeline event DOM")
    require(render_js, 'data-session-phase="${escapeHtml(model.phase)}"', label="session timeline event phase dataset")
    require(render_js, 'data-session-milestone="${escapeHtml(model.milestone)}"', label="session timeline event milestone dataset")
    require(render_js, 'data-session-verdict="${escapeHtml(model.verdict.toLowerCase())}"', label="session timeline event verdict dataset")
    require(render_js, "const timelineSession = selectedThreadPrimaryTimelineSessionModel(conversation, currentState, liveRun);", label="selected-thread transcript collapse shared model wiring")
    require(render_js, "const { collapseSessionEvents } = timelineSession;", label="selected-thread transcript collapse state destructuring")
    require(render_js, "if (shouldCollapseSelectedThreadSessionEvent(item, currentState, conversation, liveRun)) {", label="selected-thread transcript session-event suppression guard")
    require(render_js, "collapseSessionEvents: liveOwned,", label="healthy selected-thread session-event collapse ownership")
    require(render_js, 'const sessionEvent = renderSessionTimelineEvent(item);', label="session timeline event projection wiring")
    require(render_js, "if (sessionEvent) {", label="session timeline event branch")
    require(render_js, "const renderedItems = items", label="transcript render item join")
    require(render_js, 'if (!items.length && !inlineSessionBlock && !transcriptLiveActivity) {', label="transcript empty-state live activity guard")
    require(render_js, 'dom.conversationTimeline.innerHTML = inlineSessionBlock + renderedItems + transcriptLiveActivity;', label="canonical inline session lane timeline ordering")
    require_absent(render_js, "if (footerDock.visible) {", label="legacy healthy footer-dock transcript suppression guard")
    require_absent(render_js, "In Flight Assistant", label="duplicate accepted status block copy")
    require(store_js, "deriveSelectedThreadFollowControlModel", label="selected-thread follow control model helper")
    require(render_js, "selectedThreadFooterFollowState", label="footer follow state helper")
    require(render_js, "pendingAppendCount", label="follow control unseen append state")
    require(render_js, 'const footerFollow = selectedThreadFooterFollowState(dom, currentState, conversationId, renderSource);', label="follow control footer follow source")
    require(render_js, "footerFollowActionLabel", label="footer follow action label helper")
    require(render_js, 'dom.sessionStripToggle.textContent = footerFollowActionLabel(footerFollow);', label="footer follow action label render")
    require(render_js, 'dom.sessionStripToggle.dataset.followRenderSource = footerFollow.renderSource || renderSource || "snapshot";', label="follow control render source dataset")
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
    require_absent(conversations_js, "renderRecentThreadRail", label="removed recent-thread rail render helper")
    require_absent(conversations_js, "RECENT_THREAD_LIMIT = 4", label="removed recent-thread rail limit")
    require_absent(conversations_js, "data-recent-thread-chip", label="removed recent-thread chip DOM")
    require_absent(conversations_js, "data-recent-thread-state", label="removed recent-thread state DOM")
    require(conversations_js, "syncActiveSessionRow", label="active session row helper")
    require(conversations_js, "data-conversation-live-state", label="selected card live dataset")
    require(conversations_js, "data-conversation-live-owner-row", label="selected card live owner row DOM")
    require(conversations_js, "data-conversation-live-detail", label="selected card live owner detail DOM")
    require(conversations_js, "data-conversation-live-follow", label="selected card live owner follow DOM")
    require(conversations_js, 'marker.textContent = "NOW";', label="selected card marker label")
    require(conversations_js, 'card.dataset.liveOwnerState = "idle";', label="selected card owner state")
    require(conversations_js, 'sessionMarker.textContent = isSelected ? (showLiveMirror ? liveLabel || snapshotLabel : snapshotLabel) : "";', label="selected card compact session chip label")
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
    require(conversations_js, 'card.dataset.liveOwner = "false";', label="selected live owner dataset")
    require(conversations_js, 'const activeRowModel = deriveSelectedThreadActiveSessionRowModel(state, state.conversationCache);', label="active row model wiring")
    require(conversations_js, 'const selectedRowModel = deriveSelectedThreadConversationRowLiveModel(state, state.conversationCache);', label="selected row live model wiring")
    require(conversations_js, 'liveOwnerRow.hidden = !showSelectedRowLiveMarker;', label="selected row live owner row visibility")
    require(conversations_js, '!Boolean(activeRowModel.visible && activeRowModel.canonical);', label="selected row helper suppression behind active row authority")
    require(conversations_js, 'liveOwnerDetail.textContent = showSelectedRowLiveMarker ? selectedRowModel.markerLabel : "LIVE";', label="selected row live owner detail label")
    require(conversations_js, 'liveOwnerFollow.dataset.liveOwnerCue = showSelectedRowLiveMarker ? selectedRowModel.cueKind : "idle";', label="selected row live owner cue dataset")
    require(conversations_js, 'card.dataset.liveOwnerState = "idle";', label="selected live owner state dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionState = visible ? rowState : "idle";', label="active session row state dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionConversationId = visible ? conversationId : "";', label="active session row conversation dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionFollow = visible ? followLabel.toLowerCase() : "idle";', label="active session row follow dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionOwned = visible ? String(rowOwned) : "false";', label="active session row ownership dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionCanonical = visible ? String(Boolean(canonical)) : "false";', label="active session row canonical dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionSource = visible ? rowSource : "none";', label="active session row source dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionPhase = visible ? rowPhase : "IDLE";', label="active session row phase dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionUnseenCount = String(visible ? rowUnseenCount : 0);', label="active session row unseen dataset")
    require(conversations_js, 'dom.activeSessionRow.dataset.activeSessionClearReason = visible ? clearReason : "idle";', label="active session row clear reason dataset")
    require(conversations_js, "const authoritativeSelectedAttach =", label="selected-thread attach authority gate")
    require(conversations_js, "if (authoritativeSelectedAttach) {", label="selected-thread attach authority short circuit")
    require(store_js, "export function deriveSelectedThreadActiveSessionRowModel", label="active session row store helper")
    require(store_js, "export function deriveSelectedThreadConversationRowLiveModel", label="selected row live model store helper")
    require(store_js, "canonical: true,", label="active session canonical owned state")
    require(store_js, "canonical: false,", label="active session non-canonical state")
    require(conversations_js, 'const rowModel = deriveSelectedThreadActiveSessionRowModel(state, state.conversationCache);', label="active session row store model wiring")
    require(store_js, 'markerLabel =', label="selected row marker label mapping")
    require(store_js, 'cueLabel =', label="selected row cue label mapping")
    require(store_js, 'cueKind =', label="selected row cue kind mapping")
    require(store_js, 'presentation: "switching",', label="active session switching presentation")
    require(store_js, 'rowState: "switching",', label="active session switching state")
    require(store_js, 'rowSource: "thread-transition",', label="active session switching source")
    require(store_js, 'rowPhase: "SWITCHING",', label="active session switching phase")
    require(store_js, 'followLabel: "ATTACH",', label="active session switching follow label")
    require(store_js, 'meta: "selected thread · switching · attach pending",', label="active session switching meta copy")
    require(store_js, 'presentation: "handoff",', label="active session handoff presentation")
    require(store_js, 'rowState: "handoff",', label="active session handoff state")
    require(store_js, 'stateLabel: "HANDOFF",', label="active session handoff label")
    require(store_js, 'const rowState = followControl.visible ? followControl.followState : "live";', label="active session owned state mapping")
    require(store_js, 'const followLabel = followControl.visible ? followControl.stateLabel : "LIVE";', label="active session owned follow mapping")
    require(store_js, 'const rowPhase = phaseLabel || "LIVE";', label="active session owned phase mapping")
    require(store_js, '`selected thread · ${rowPhase.toLowerCase()} · ${rowUnseenCount} new`', label="active session unseen meta copy")
    require(store_js, '`selected thread · ${rowPhase.toLowerCase()} · ${followControl.detailLabel}`', label="active session paused meta copy")
    require(store_js, '`selected thread · ${rowPhase.toLowerCase()} · sse owner`', label="active session healthy meta copy")
    require(conversations_js, "syncSelectedSessionFromLiveAppend", label="selected-thread live append sync helper")
    require(conversations_js, "const liveJobId = String(livePayload.job_id || \"\").trim();", label="live append job id extraction")
    require(conversations_js, "state.currentJobId = liveJobId;", label="live append selected-thread job id authority")
    require(conversations_js, "conversation.latest_job_id = liveJobId;", label="live append conversation job id authority")
    require(conversations_js, "shouldProjectAutonomySummaryFromLiveAppend", label="autonomy summary append projection helper")
    require(conversations_js, "projectAutonomySummaryFromLiveAppend", label="autonomy summary live projection helper")
    require(conversations_js, "autonomySummaryFromSessionStatus", label="session-status autonomy summary helper")
    require(conversations_js, "normalizeAutonomySummary", label="autonomy summary normalization helper")
    require(conversations_js, "hydrateAutonomySummary", label="autonomy summary hydration helper")
    require(conversations_js, "isSelectedThreadAutonomyAuthoritative", label="selected-thread autonomy authority helper")
    require(conversations_js, "isSelectedThreadSessionStatusAutonomyAuthoritative", label="session-status autonomy authority helper")
    require(conversations_js, "shouldAllowGoalsPollingFallback", label="selected-thread goals fallback gate")
    require(conversations_js, "liveJobMetaLabel", label="live append job meta helper")
    require(conversations_js, "const sessionStatusAutonomySummary = autonomySummaryFromSessionStatus(", label="append session-status autonomy summary hydration")
    require(conversations_js, "const projectedAutonomySummary = projectAutonomySummaryFromLiveAppend(kind, payload);", label="append-driven autonomy summary projection")
    require(conversations_js, "state.autonomySummary = projectedAutonomySummary;", label="append-driven autonomy summary state update")
    require(conversations_js, 'String(conversationId) === String(state.currentConversationId || "") ||', label="selected-thread goals fallback current conversation suppression")
    require(conversations_js, 'String(conversationId) === String(state.savedConversationId || "")', label="selected-thread goals fallback saved conversation suppression")
    require(conversations_js, 'source: authoritative ? "session-status" : `session-status-${transportState || "degraded"}`', label="session-status autonomy source selection")
    require(conversations_js, "const selectedThreadAutonomy =", label="bootstrap session-status autonomy selection")
    require(conversations_js, "state.autonomySummary = selectedThreadAutonomy;", label="bootstrap session-status autonomy state update")
    require(conversations_js, 'state.appendStream?.attachMode === "sse-bootstrap" ||', label="bootstrap attach healthy-path polling suppression")
    require(conversations_js, "state.appendStream?.sessionStatus?.proposalJobId ||", label="bootstrap session-status proposal job id authority")
    require_absent(conversations_js, 'await refreshGoalSummary({ conversationId: conversation.conversation_id });', label="removed selected-thread goals polling refresh")
    require_absent(conversations_js, "refreshGoalSummary().catch(() => {});", label="legacy append-driven autonomy summary refetch")
    require(conversations_js, "setJobMeta(dom, immediateMeta);", label="append-driven job meta refresh")
    require(conversations_js, "scheduleAppendStreamResume", label="reconnect resume scheduler")
    require(conversations_js, "transitionAppendStreamToFallback", label="explicit reconnect fallback helper")
    require(conversations_js, 'state.appendStream.transport = "sse"', label="selected-thread sse transport")
    require(store_js, "export function isAppendStreamAuthoritative", label="append stream authoritative helper")
    require(store_js, "export function deriveSelectedThreadSessionStatus", label="canonical selected-thread session status helper")
    require(store_js, "selectedThreadProvisional", label="selected-thread provisional state")
    require(store_js, "selectedThreadRestore", label="selected-thread restore state")
    require(store_js, "provisionalResume", label="selected-thread provisional resume state")
    require(store_js, "restoreResume", label="selected-thread restore resume state")
    require(store_js, "restoreStage", label="selected-thread restore stage")
    require(store_js, "switchActive", label="selected-thread switch activity state")
    require(store_js, "switchConversationId", label="selected-thread switch conversation state")
    require(store_js, "switchTargetTitle", label="selected-thread switch title state")
    require(store_js, 'transportReason = provisionalResume ? "selected-thread-resume" : "selected-thread-attach";', label="selected-thread provisional transport reason")
    require(store_js, 'transportReason = restoreResume ? "saved-restore-resume" : "saved-restore-attach";', label="selected-thread restore transport reason")
    require(store_js, 'presentation = "provisional";', label="selected-thread provisional presentation")
    require(store_js, 'presentation = "restore";', label="selected-thread restore presentation")
    require(store_js, "export function deriveSelectedThreadLiveAutonomy", label="canonical selected-thread live autonomy helper")
    require(store_js, "const sessionStatusPayload = currentState.appendStream?.sessionStatus || null;", label="store session-status autonomy payload read")
    require(store_js, 'source: "session-status",', label="store session-status autonomy source")
    require(store_js, "const canonicalAutonomySummary = sessionStatusSummary || autonomySummary;", label="store session-status autonomy precedence")
    require(store_js, "export function deriveSelectedThreadPhaseProgression", label="canonical selected-thread phase progression helper")
    require(store_js, "export function deriveSelectedThreadShellPhaseLabel", label="canonical selected-thread shell phase helper")
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
    require(jobs_js, "selectedThreadPollingFallbackAllowed", label="job polling selected-thread fallback gate")
    require(jobs_js, "!selectedThreadPollingFallbackAllowed()", label="polling suppression while selected-thread session is sse-owned")
    require(jobs_js, "stopPolling();\n      return;", label="polling early exit while selected-thread session is sse-owned")
    require(jobs_js, 'if (!selectedThreadPollingFallbackAllowed()) {\n      return payload;\n    }', label="late poll visible-state suppression")
    require(jobs_js, "selectedThreadPollingFallbackAllowed(state.currentConversationId)", label="poll-driven conversation refresh fallback gate")
    require_absent(jobs_js, 'await refreshGoalSummary();', label="removed poll-driven goals refresh fallback")
    require(jobs_js, "!isAppendStreamAuthoritative(state, state.currentConversationId)", label="polling refetch skip while append stream is authoritative")
    require(styles, ".conversation-card-live-owner-row", label="selected card live owner row CSS")
    require(styles, ".active-session-row", label="active session row CSS")
    require(styles, "position: sticky;", label="active session sticky position CSS")
    require(styles, ".active-session-chip", label="active session chip CSS")
    require(styles, '.active-session-row[data-active-session-state="paused"] .active-session-chip[data-active-chip="state"]', label="active session paused chip CSS")
    require(styles, '.active-session-row[data-active-session-follow="live"] .active-session-chip[data-active-chip="follow"]', label="active session live chip CSS")
    require(styles, '.active-session-row[data-active-session-follow="attach"] .active-session-chip[data-active-chip="follow"]', label="active session attach chip CSS")
    require(styles, '.conversation-card[data-live-owner-state="handoff"] .conversation-card-marker', label="selected handoff owner marker CSS")
    require(styles, '.conversation-card[data-live-owner-state="new"] .conversation-card-marker', label="selected new owner marker CSS")
    require(styles, '.conversation-card[data-live-owner-state="paused"] .conversation-card-marker', label="selected paused owner marker CSS")
    require_absent(index_html, 'id="jump-to-latest"', label="removed floating jump-to-latest DOM")
    require(index_html, 'id="active-session-row"', label="active session row DOM")
    require(index_html, 'id="active-session-owner"', label="active session owner DOM")
    require(index_html, 'id="active-session-state"', label="active session state DOM")
    require(index_html, 'id="active-session-follow"', label="active session follow DOM")
    require(index_html, 'data-active-session-owned="false"', label="active session owned default")
    require(index_html, 'data-active-session-source="none"', label="active session source default")
    require(index_html, 'data-active-session-phase="IDLE"', label="active session phase default")
    require(index_html, 'data-active-session-unseen-count="0"', label="active session unseen default")
    require_absent(styles, ".jump-to-latest", label="removed floating jump-to-latest CSS")


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

    time.sleep(2)
    recorder.stop()

    conversation_after = wait_for_conversation_ready(base_url, conversation_id, api_key)
    terminal_event = "proposal.ready"
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
                "latest_job_id": str(conversation_after.get("latest_job_id", "") or ""),
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
