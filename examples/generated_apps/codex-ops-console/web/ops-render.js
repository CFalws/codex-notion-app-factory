import { DECISION_FIELDS } from "./ops-constants.js";
import {
  deriveSelectedThreadLiveAutonomy,
  deriveSelectedThreadPhaseProgression,
  deriveSelectedThreadSessionStatus,
  deriveSelectedThreadTimelineMilestones,
  maxConversationAppendId,
} from "./ops-store.js";

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function simplifyText(value) {
  return String(value || "")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\*\*/g, "")
    .replace(/^#{1,3}\s+/gm, "")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function eventLabel(eventType = "") {
  const labels = {
    "conversation.created": "대화 시작",
    "message.accepted": "메시지 접수",
    "intent.interpreted": "의도 해석",
    "job.queued": "작업 대기",
    "job.running": "작업 시작",
    "job.completed": "작업 완료",
    "goal.proposal.phase.started": "제안 단계 시작",
    "goal.proposal.phase.completed": "제안 단계 완료",
    "goal.review.phase.started": "리뷰 단계 시작",
    "goal.review.phase.completed": "리뷰 단계 완료",
    "goal.verify.phase.started": "검증 단계 시작",
    "goal.verify.phase.completed": "검증 단계 완료",
    "goal.proposal.auto_apply.started": "자동 적용 시작",
    "proposal.saved": "제안 저장",
    "proposal.ready": "제안 준비",
    "runtime.context.loaded": "기존 맥락 로드",
    "runtime.workspace.selected": "작업 경로 선택",
    "runtime.summary.recorded": "요약 저장",
    "codex.exec.started": "Codex 실행",
    "codex.exec.finished": "Codex 종료",
    "runtime.exception": "런타임 예외",
  };
  return labels[eventType] || eventType;
}

export function setStatus(dom, message) {
  dom.statusOutput.textContent = message;
}

export function setJobMeta(dom, message) {
  dom.jobMeta.textContent = message;
}

function headerPhaseTone(liveRun) {
  if (!liveRun || !liveRun.visible) {
    return "muted";
  }
  if (liveRun.tone === "done") {
    return "healthy";
  }
  if (liveRun.tone === "waiting") {
    return "warning";
  }
  if (liveRun.tone === "running") {
    return "danger";
  }
  if (liveRun.tone === "thinking") {
    return "neutral";
  }
  return "muted";
}

function headerPhaseSource(liveRun) {
  if (!liveRun || !liveRun.visible) {
    return "none";
  }
  return String(liveRun.source || "none").toLowerCase();
}

function phaseDetailCopy(liveRun) {
  const detail = simplifyText(liveRun?.detail || "");
  if (detail) {
    return detail;
  }
  return phaseDetailHint(liveRun);
}

function compactPhaseDetailCopy(liveRun, fallback = "SESSION ACTIVE") {
  const hint = phaseDetailHint(liveRun);
  if (hint && hint !== "SESSION ACTIVE") {
    return hint;
  }
  return compactTargetLabel(phaseDetailCopy(liveRun), fallback);
}

export function updateHeroState(
  dom,
  {
    threadTitle = "",
    threadKicker = "",
    conversationState = "",
    liveRun = null,
  } = {},
) {
  if (threadTitle && dom.threadTitle) {
    dom.threadTitle.textContent = threadTitle;
  }
  if (threadKicker && dom.threadKicker) {
    dom.threadKicker.textContent = threadKicker;
  }
  if (conversationState && dom.conversationMeta) {
    dom.conversationMeta.textContent = conversationState;
  }
  if (dom.threadPhaseChip) {
    const phaseLabel = liveRun?.visible ? String(liveRun.phase || "IDLE").toUpperCase() : "IDLE";
    const phaseTone = headerPhaseTone(liveRun);
    const phaseSource = headerPhaseSource(liveRun);
    dom.threadPhaseChip.textContent = phaseLabel;
    dom.threadPhaseChip.dataset.tone = phaseTone;
    dom.threadPhaseChip.dataset.threadPhase = phaseLabel;
    dom.threadPhaseChip.dataset.threadPhaseSource = phaseSource;
    dom.threadPhaseChip.dataset.threadPhaseDetail = liveRun?.visible ? phaseDetailCopy(liveRun) : "idle";
    dom.threadPhaseChip.title = liveRun?.visible ? phaseDetailCopy(liveRun) : "현재 활성 세션이 없습니다.";
  }
}

export function renderWorkspaceSummary(dom, summary) {
  dom.workspaceSummaryText.textContent = summary;
}

export function renderDraftStatus(dom, message) {
  dom.draftStatus.textContent = message;
}

function compactTargetLabel(value, fallback = "SELECTED") {
  const simplified = simplifyText(value || "")
    .replace(/\s+/g, " ")
    .trim();
  if (!simplified) {
    return fallback;
  }
  return simplified.length > 28 ? `${simplified.slice(0, 27).trimEnd()}…` : simplified;
}

function summaryHint(pathLabel, stateLabel) {
  return `${pathLabel} · ${stateLabel}`;
}

function joinSessionChromeTokens(...tokens) {
  return tokens
    .map((token) => String(token || "").trim())
    .filter(Boolean)
    .join(" · ");
}

function sessionFollowLabel(sessionIndicator, transportState) {
  if (sessionIndicator.state === "paused") {
    return "PAUSED";
  }
  if (sessionIndicator.state === "new") {
    return "NEW";
  }
  if (sessionIndicator.state === "handoff") {
    return "HANDOFF";
  }
  if (sessionIndicator.state === "live" && transportState.owned) {
    return "FOLLOW";
  }
  return "";
}

function proposalStatusLabel(proposalState) {
  if (proposalState.label === "READY") {
    return "APPLY READY";
  }
  if (proposalState.label === "APPLIED") {
    return "APPLIED";
  }
  if (proposalState.label === "BLOCKED") {
    return "BLOCKED";
  }
  return "";
}

function sessionChromeCopy(ownerState, transportState, sessionIndicator, liveRun, proposalState, pathLabel, stateLabel) {
  const target = ownerState.target;
  if (ownerState.state === "switching") {
    return target;
  }
  if (ownerState.state === "handoff") {
    return target;
  }
  if (transportState.owned && sessionIndicator.source === "sse") {
    return target;
  }
  if (pathLabel === "DEGRADED") {
    return joinSessionChromeTokens(target, stateLabel, "DEGRADED");
  }
  return target;
}

function sessionStripDetailCopy(ownerState, transportState, sessionIndicator, liveRun, proposalState, liveOwned, footerFollow = null) {
  const target = ownerState.target;
  if (ownerState.state === "switching") {
    return target;
  }
  if (ownerState.state === "handoff") {
    return target;
  }
  if (footerFollow?.visible) {
    return `${footerFollow.stateLabel} · ${footerFollow.detailLabel}`;
  }
  if (liveOwned) {
    return target;
  }
  if (transportState.key === "reconnect" || transportState.key === "polling") {
    return joinSessionChromeTokens(target, transportState.label, "DEGRADED");
  }
  return target;
}

function sessionStripStateChipMarkup(chips) {
  const items = Array.isArray(chips) ? chips : [chips];
  return items
    .map(
      ({ label, tone, role }) =>
        `<span class="session-chip" data-tone="${escapeHtml(tone)}" data-session-strip-role="${escapeHtml(role)}">${escapeHtml(label)}</span>`,
    )
    .join("");
}

function selectedThreadFooterDockModel(currentState, conversation, liveRun, footerFollow = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, conversation);
  const milestoneModel = deriveSelectedThreadTimelineMilestones(currentState, conversation);
  const summary = liveAutonomy.summary || null;
  const liveOwned = Boolean(
    sessionStatus.liveOwned &&
      phaseProgression.visible &&
      String(phaseProgression.source || "none").toLowerCase() === "sse",
  );
  const phaseLabel = String(phaseProgression.label || liveRun?.phase || "LIVE").toUpperCase();
  const milestoneChips = milestoneModel.visible
    ? milestoneModel.items.map((item) => ({
        label: item.label,
        tone: item.state === "complete" ? "healthy" : item.state === "active" ? "neutral" : item.state === "blocked" ? "warning" : "muted",
        role: item.state === "active" ? "live-phase" : item.state === "complete" ? "live-complete" : item.state === "blocked" ? "live-blocked" : "live-pending",
      }))
    : [{ label: phaseLabel, tone: "neutral", role: "live-phase" }];
  const chips = [];
  if (footerFollow?.visible) {
    chips.push({
      label: footerFollow.stateLabel,
      tone: footerFollow.followState === "new" ? "warning" : "neutral",
      role: "live-follow",
    });
  }
  chips.push(...milestoneChips);
  const detailTokens = [];
  if (footerFollow?.visible) {
    detailTokens.push(footerFollow.detailLabel);
  }
  if (summary) {
    detailTokens.push(String(summary.pathVerdict || "UNKNOWN").toUpperCase());
    detailTokens.push(String(summary.verifierAcceptability || "PENDING").toUpperCase());
    detailTokens.push(`BLOCKER ${String(summary.blockerReason || "none").toUpperCase()}`);
  } else {
    detailTokens.push(phaseLabel);
  }
  return {
    visible: liveOwned,
    phaseLabel,
    chips,
    detail: detailTokens.filter(Boolean).join(" · "),
    source: String(milestoneModel.source || phaseProgression.source || "sse").toLowerCase(),
    summary,
    liveOwned,
  };
}

function sessionStripStateRow(ownerState, transportState, liveRun, presentation, liveOwned, footerFollow = null, footerDock = null) {
  if (transportState.key === "reconnect" || transportState.key === "polling") {
    return {
      label: transportState.label,
      tone: transportState.tone,
      role: "degraded",
      chips: [{ label: transportState.label, tone: transportState.tone, role: "degraded" }],
    };
  }
  if (ownerState.state === "switching") {
    return {
      label: "SWITCHING",
      tone: "warning",
      role: "transition",
      chips: [{ label: "SWITCHING", tone: "warning", role: "transition" }],
    };
  }
  if (footerDock?.visible) {
    const primaryChip = footerDock.chips[0] || { label: footerDock.phaseLabel || "LIVE", tone: "neutral", role: "live-phase" };
    return {
      label: primaryChip.label,
      tone: primaryChip.tone,
      role: "live-dock",
      chips: footerDock.chips,
    };
  }
  if (footerFollow?.visible) {
    return {
      label: footerFollow.followState === "new" ? "LIVE" : ownerState.label || "READY",
      tone: "healthy",
      role: "live-follow",
      chips: [{ label: footerFollow.followState === "new" ? "LIVE" : ownerState.label || "READY", tone: "healthy", role: "live-follow" }],
    };
  }
  return {
    label: "TARGET",
    tone: "muted",
    role: "context",
    chips: [{ label: "TARGET", tone: "muted", role: "context" }],
  };
}

function composerOwnerState(currentState, conversation) {
  const pendingOutgoing = currentState.pendingOutgoing || {};
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);

  if (sessionStatus.presentation === "attach" && sessionStatus.targetConversationId) {
    return {
      state: "switching",
      label: "SWITCHING",
      tone: "warning",
      conversationId: String(sessionStatus.targetConversationId || ""),
      target: compactTargetLabel(sessionStatus.targetTitle || "선택한 대화", "ATTACH TARGET"),
      copy: "ATTACH",
      blocked: true,
      blockedReason: "selected-thread attach가 끝날 때까지 잠시 기다려 주세요.",
    };
  }

  if (sessionStatus.pendingHandoff && sessionStatus.selectedThreadSse) {
    return {
      state: "handoff",
      label: "HANDOFF",
      tone: "neutral",
      conversationId: sessionStatus.conversationId,
      target: compactTargetLabel(sessionStatus.conversationTitle, "CURRENT THREAD"),
      copy:
        pendingOutgoing.status === "sending-user"
          ? "SEND"
          : "FIRST",
      blocked: false,
      blockedReason: "",
    };
  }

  if (sessionStatus.presentation === "restore" && sessionStatus.conversationId) {
    return {
      state: "restore",
      label: sessionStatus.restoreResume ? "RESUME" : "ATTACH",
      tone: sessionStatus.restoreResume ? "warning" : "neutral",
      conversationId: sessionStatus.conversationId,
      target: compactTargetLabel(sessionStatus.conversationTitle, "CURRENT THREAD"),
      copy: "RESTORE",
      blocked: false,
      blockedReason: "",
    };
  }

  if (sessionStatus.conversationId) {
    return {
      state: "ready",
      label: "READY",
      tone: "healthy",
      conversationId: sessionStatus.conversationId,
      target: compactTargetLabel(sessionStatus.conversationTitle, "CURRENT THREAD"),
      copy: "OWNER",
      blocked: false,
      blockedReason: "",
    };
  }

  return {
    state: "idle",
    label: "IDLE",
    tone: "muted",
    conversationId: "",
    target: "NO TARGET",
    copy: "SELECT",
    blocked: false,
    blockedReason: "",
  };
}

function syncComposerOwnership(dom, currentState, conversation) {
  if (!dom.composerOwnerRow || !dom.composerOwnerState || !dom.composerOwnerTarget || !dom.composerOwnerCopy) {
    return;
  }
  const owner = composerOwnerState(currentState, conversation);
  const mergedStripVisible = Boolean(dom.sessionStrip && !dom.sessionStrip.hidden);
  dom.composerOwnerRow.dataset.composerOwner = owner.state;
  dom.composerOwnerRow.dataset.composerOwnerConversationId = owner.conversationId;
  dom.composerOwnerRow.dataset.composerRestoreStage = owner.state === "restore" ? (owner.label === "RESUME" ? "resume-pending" : "attach-pending") : "none";
  dom.composerOwnerRow.dataset.composerOwnerMerged = mergedStripVisible ? "true" : "false";
  dom.composerOwnerRow.hidden = mergedStripVisible;
  dom.composerOwnerState.textContent = owner.label;
  dom.composerOwnerState.dataset.ownerTone = owner.tone;
  dom.composerOwnerTarget.textContent = owner.target;
  dom.composerOwnerCopy.textContent = owner.copy;
  if (dom.sendRequestButton) {
    const sendBusy = dom.sendRequestButton.dataset.sendBusy === "true";
    dom.sendRequestButton.dataset.composerBlocked = owner.blocked ? "true" : "false";
    dom.sendRequestButton.dataset.composerOwnerState = owner.state;
    dom.sendRequestButton.dataset.composerOwnerConversationId = owner.conversationId;
    dom.sendRequestButton.dataset.composerBlockedReason = owner.blockedReason;
    dom.sendRequestButton.disabled = owner.blocked || sendBusy;
  }
}

function composerTransportState(currentState, conversation, liveRun, handoffState = { stage: "idle" }) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const sessionIndicator = selectedThreadLiveSessionIndicator(currentState, conversation, liveRun, handoffState);

  if (sessionStatus.presentation === "restore" && sessionStatus.conversationId) {
    return {
      label: sessionStatus.restoreResume ? "RESUME" : "ATTACH",
      key: sessionStatus.restoreResume ? "resume" : "attach",
      tone: sessionStatus.transportTone,
      source: sessionStatus.restoreProvenance || sessionStatus.transport || "sse",
      owned: false,
      reason: sessionStatus.transportReason,
    };
  }

  if (!sessionStatus.conversationId && sessionStatus.presentation === "attach" && sessionStatus.targetConversationId) {
    return {
      label: "ATTACH",
      key: "attach",
      tone: "warning",
      source: "thread-transition",
      owned: false,
      reason: "thread-switch",
    };
  }

  if (sessionIndicator.visible) {
    return {
      label: sessionIndicator.label,
      key: String(sessionIndicator.label || "session").toLowerCase().replace(/\s+/g, "-"),
      tone: sessionIndicator.tone,
      source: sessionIndicator.source,
      owned: sessionIndicator.owned,
      reason: sessionIndicator.reason,
    };
  }

  if (sessionStatus.transportState === "reconnect" || sessionStatus.transportState === "polling") {
    return {
      label: sessionStatus.transportLabel || "POLLING",
      key: sessionStatus.transportState,
      tone: sessionStatus.transportTone,
      source: sessionStatus.transport === "sse" ? sessionStatus.renderSource || "snapshot" : sessionStatus.transport || "polling",
      owned: false,
      reason: sessionStatus.transportReason,
    };
  }

  return {
    label: "SNAPSHOT",
    key: "snapshot",
    tone: "muted",
    source: "snapshot",
    owned: false,
    reason: "snapshot",
  };
}

function renderSessionSummary(dom, currentState, conversation, liveRun, handoffState = { stage: "idle" }) {
  if (
    !dom.sessionSummaryRow ||
    !dom.sessionSummaryScope ||
    !dom.sessionSummaryPath ||
    !dom.sessionSummaryState ||
    !dom.sessionLiveIndicator ||
    !dom.sessionSummaryCopy
  ) {
    return;
  }

  const threadTransition = currentState.threadTransition || {};
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  const conversationId = String(conversation?.conversation_id || sessionStatus.conversationId || "");
  const headerSummaryVisible = Boolean(conversationId || threadTransition.targetConversationId || sessionStatus.conversationId);
  const footerDockOwnsLive = Boolean(sessionStatus.liveOwned && phaseProgression.visible && liveAutonomy.owned);
  const sessionIndicator = selectedThreadLiveSessionIndicator(currentState, conversation, liveRun, handoffState);
  const proposalState = proposalChip(liveRun);

  let pathLabel = "SNAPSHOT";
  let stateLabel = conversationId ? "READY" : "IDLE";
  let copy = sessionChromeCopy(
    composerOwnerState(currentState, conversation),
    composerTransportState(currentState, conversation, liveRun, handoffState),
    sessionIndicator,
    liveRun,
    proposalState,
    "SNAPSHOT",
    conversationId ? "READY" : "IDLE",
  );

  if (threadTransition.active && threadTransition.targetConversationId) {
    pathLabel = "SWITCHING";
    stateLabel = "ATTACH";
  } else if (sessionStatus.presentation === "restore" && sessionStatus.conversationId) {
    pathLabel = "RESTORE";
    stateLabel = sessionStatus.restoreResume ? "RESUME" : "ATTACH";
  } else if (handoffState.stage === "pending-user") {
    pathLabel = "SESSION";
    stateLabel = "ATTACHED";
  } else if (handoffState.stage === "pending-assistant") {
    pathLabel = "SESSION";
    stateLabel = "ATTACHED";
  } else if (sessionStatus.transportState === "reconnect") {
    pathLabel = "DEGRADED";
    stateLabel = "RESUME";
  } else if (liveAutonomy.visible && liveAutonomy.owned) {
    pathLabel = "SESSION";
    stateLabel = "ATTACHED";
  } else if (sessionStatus.transportState === "polling") {
    pathLabel = "DEGRADED";
    stateLabel = "POLLING";
  }
  copy = sessionChromeCopy(
    composerOwnerState(currentState, conversation),
    composerTransportState(currentState, conversation, liveRun, handoffState),
    sessionIndicator,
    liveRun,
    proposalState,
    pathLabel,
    stateLabel,
  );

  dom.sessionSummaryRow.dataset.summaryPath = pathLabel.toLowerCase();
  dom.sessionSummaryRow.dataset.summaryState = stateLabel.toLowerCase();
  dom.sessionSummaryRow.dataset.summaryPhase = String(phaseProgression.label || liveRun?.phase || "IDLE").toUpperCase();
  dom.sessionSummaryRow.dataset.restoreStage = sessionStatus.restoreStage || "none";
  dom.sessionSummaryRow.dataset.restorePath = sessionStatus.restorePath || "none";
  dom.sessionSummaryRow.dataset.restoreProvenance = sessionStatus.restoreProvenance || "none";
  dom.sessionSummaryRow.dataset.followState = sessionIndicator.state;
  dom.sessionSummaryRow.dataset.liveSessionState = sessionIndicator.state;
  dom.sessionSummaryRow.dataset.liveSessionSource = sessionIndicator.source;
  dom.sessionSummaryRow.dataset.liveSessionReason = sessionIndicator.reason;
  dom.sessionSummaryRow.dataset.liveSessionOwned = sessionIndicator.owned ? "true" : "false";
  dom.sessionSummaryRow.dataset.footerDockOwned = footerDockOwnsLive ? "true" : "false";
  dom.sessionSummaryRow.hidden = !headerSummaryVisible || footerDockOwnsLive;
  dom.sessionSummaryScope.textContent = compactTargetLabel(
    conversation?.title || sessionStatus.conversationTitle || threadTransition.targetTitle || "",
    "SELECTED",
  );
  dom.sessionSummaryPath.textContent = pathLabel;
  dom.sessionSummaryState.textContent = stateLabel;
  dom.sessionLiveIndicator.hidden = true;
  dom.sessionLiveIndicator.textContent = sessionIndicator.label;
  dom.sessionLiveIndicator.dataset.liveSessionTone = sessionIndicator.tone;
  dom.sessionLiveIndicator.dataset.liveSessionSource = sessionIndicator.source;
  dom.sessionLiveIndicator.dataset.liveSessionOwned = sessionIndicator.owned ? "true" : "false";
  dom.sessionLiveIndicator.dataset.liveSessionReason = sessionIndicator.reason;
  dom.sessionSummaryCopy.textContent = copy;
  if (dom.threadPhaseChip) {
    dom.threadPhaseChip.hidden = headerSummaryVisible;
  }
}

function isThreadNearBottom(threadScroller) {
  if (!threadScroller) {
    return true;
  }
  return threadScroller.scrollTop + threadScroller.clientHeight >= threadScroller.scrollHeight - 72;
}

function phaseDetail(prefix, latestEvent, fallback) {
  const body = simplifyText(latestEvent?.body || "");
  return body ? `${prefix} ${body}` : fallback;
}

function selectedThreadSessionPhase(conversation, currentState) {
  const appendStream = currentState?.appendStream || {};
  const conversationId = String(conversation?.conversation_id || "");
  const currentConversationId = String(currentState?.currentConversationId || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const transport = String(appendStream.transport || "polling").toLowerCase();
  const renderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const status = String(appendStream.status || "offline").toLowerCase();
  const selectedThreadStream =
    Boolean(conversationId) &&
    currentConversationId === conversationId &&
    streamConversationId === conversationId &&
    transport === "sse" &&
    renderSource === "sse" &&
    (status === "live" || status === "connecting");
  if (!selectedThreadStream) {
    return {
      value: "UNKNOWN",
      authoritative: false,
      reason: "non-authoritative-stream",
      appendId: 0,
      source: "none",
      eventType: "",
      status: "",
      jobId: "",
    };
  }
  const model = appendStream.sessionPhase || {};
  return {
    value: String(model.value || "UNKNOWN").toUpperCase(),
    authoritative: Boolean(model.authoritative),
    reason: String(model.reason || "missing-phase"),
    appendId: Math.max(Number(model.appendId || model.append_id || 0), 0),
    source: String(model.source || "sse").toLowerCase(),
    eventType: String(model.eventType || model.event_type || ""),
    status: String(model.status || "").toLowerCase(),
    jobId: String(model.jobId || model.job_id || ""),
  };
}

function isSessionAuthorityEvent(event) {
  const type = String(event?.type || "");
  const status = String(event?.status || "").toLowerCase();
  return (
    type === "codex.exec.retrying" ||
    type === "runtime.exception" ||
    type === "job.completed" ||
    type === "proposal.ready" ||
    type === "codex.exec.applied" ||
    type.startsWith("goal.proposal.phase.") ||
    type.startsWith("goal.review.phase.") ||
    type.startsWith("goal.verify.phase.") ||
    type === "goal.proposal.auto_apply.started" ||
    type === "job.running" ||
    type === "job.queued" ||
    type === "message.accepted" ||
    type === "codex.exec.started" ||
    type === "codex.exec.finished" ||
    status === "failed" ||
    status === "completed" ||
    status === "applied"
  );
}

function selectedThreadSseAuthorityEvent(conversation, currentState) {
  const appendStream = currentState?.appendStream || {};
  const conversationId = String(conversation?.conversation_id || "");
  const currentConversationId = String(currentState?.currentConversationId || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const status = String(appendStream.status || "offline").toLowerCase();
  const transport = String(appendStream.transport || "polling").toLowerCase();
  const renderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const selectedThreadSseOwned =
    Boolean(conversationId) &&
    currentConversationId === conversationId &&
    streamConversationId === conversationId &&
    transport === "sse" &&
    renderSource === "sse" &&
    status === "live";
  if (!selectedThreadSseOwned) {
    return null;
  }
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  for (let index = events.length - 1; index >= 0; index -= 1) {
    const event = events[index];
    if (String(event?.delivery_source || "").toLowerCase() !== "sse") {
      continue;
    }
    if (isSessionAuthorityEvent(event)) {
      return event;
    }
  }
  return null;
}

function sessionAuthorityJobId(conversation, currentState) {
  const liveAuthorityEvent = selectedThreadSseAuthorityEvent(conversation, currentState);
  const liveAuthorityJobId = String(liveAuthorityEvent?.job_id || "").trim();
  if (liveAuthorityJobId) {
    return liveAuthorityJobId;
  }
  return String(currentState.currentJobId || conversation?.latest_job_id || "");
}

function sessionAuthorityEvents(conversation, currentState) {
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  const liveAuthorityEvent = selectedThreadSseAuthorityEvent(conversation, currentState);
  const authoritativeJobId = String(liveAuthorityEvent?.job_id || "").trim();
  const jobId = authoritativeJobId || String(currentState.currentJobId || conversation?.latest_job_id || "");
  return jobId ? events.filter((event) => !event.job_id || event.job_id === jobId) : events;
}

function latestSessionIndicatorEvent(conversation, currentState) {
  const liveAuthorityEvent = selectedThreadSseAuthorityEvent(conversation, currentState);
  if (liveAuthorityEvent) {
    return liveAuthorityEvent;
  }
  const relevantEvents = sessionAuthorityEvents(conversation, currentState);
  for (let index = relevantEvents.length - 1; index >= 0; index -= 1) {
    const event = relevantEvents[index];
    if (isSessionAuthorityEvent(event)) {
      return event;
    }
  }
  return relevantEvents.length ? relevantEvents[relevantEvents.length - 1] : null;
}

function selectedThreadLiveSessionIndicator(currentState, conversation, liveRun, handoffState = { stage: "idle" }) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const latestEvent = latestSessionIndicatorEvent(conversation, currentState);
  const latestType = String(latestEvent?.type || "");
  const hasActiveRun =
    Boolean(sessionStatus.conversationId) &&
    liveRun?.visible &&
    !liveRun?.terminal &&
    liveRun?.phase &&
    liveRun.phase !== "IDLE";
  if (
    !hasActiveRun ||
    sessionStatus.presentation === "attach" ||
    handoffState.stage === "pending-user" ||
    handoffState.stage === "pending-assistant"
  ) {
    return {
      visible: false,
      label: "SESSION",
      state: "idle",
      source: "none",
      reason: "idle",
      tone: "muted",
      owned: false,
    };
  }
  if (sessionStatus.liveOwned) {
    return {
      visible: true,
      label: sessionStatus.transportLabel || "SSE OWNER",
      state: sessionStatus.followPaused ? "paused" : "following",
      source: "sse",
      reason: sessionStatus.transportReason,
      tone: "healthy",
      owned: true,
    };
  }
  if (sessionStatus.transportState === "reconnect") {
    return {
      visible: true,
      label: sessionStatus.transportLabel || "RECONNECT",
      state: "reconnecting",
      source: "sse",
      reason: sessionStatus.transportReason,
      tone: "warning",
      owned: false,
    };
  }
  if (
    sessionStatus.transportState === "polling"
  ) {
    return {
      visible: true,
      label: sessionStatus.transportLabel || "POLLING",
      state: "polling",
      source: sessionStatus.transport === "sse" ? sessionStatus.renderSource || "snapshot" : sessionStatus.transport || "polling",
      reason: sessionStatus.transportReason,
      tone: sessionStatus.transportTone,
      owned: false,
    };
  }
  return {
    visible: false,
    label: "SESSION",
    state: "idle",
    source: "none",
    reason: "idle",
    tone: "muted",
    owned: false,
  };
}

function runStateSnapshot({
  visible = true,
  state = "idle",
  phase = "IDLE",
  detail = "",
  source = "none",
  tone = "idle",
  jobId = "",
  terminal = false,
  appendId = 0,
  createdAt = "",
}) {
  return { visible, state, phase, detail, source, tone, jobId, terminal, appendId, createdAt };
}

const INLINE_TERMINAL_RETENTION_MS = 12000;

function shouldRetainInlineTerminalPhase(appendStream, liveRun, selectedThreadSseOwned, renderSource, status) {
  if (
    !selectedThreadSseOwned ||
    renderSource !== "sse" ||
    status !== "live" ||
    !liveRun?.visible ||
    !liveRun?.terminal ||
    (liveRun.phase !== "READY" && liveRun.phase !== "APPLIED")
  ) {
    return false;
  }
  const latestAppendId = Number(appendStream.lastLiveAppendId || appendStream.lastAppendId || 0);
  const terminalAppendId = Number(liveRun.appendId || 0);
  if (terminalAppendId && latestAppendId > terminalAppendId) {
    return false;
  }
  const createdAtMs = Date.parse(String(liveRun.createdAt || ""));
  if (!Number.isFinite(createdAtMs)) {
    return false;
  }
  return Date.now() - createdAtMs <= INLINE_TERMINAL_RETENTION_MS;
}

function transcriptLiveTone(liveRun) {
  if (liveRun?.tone === "done") {
    return "healthy";
  }
  if (liveRun?.tone === "waiting") {
    return "warning";
  }
  if (liveRun?.tone === "running") {
    return "danger";
  }
  return "neutral";
}

function selectedThreadInlineSessionState(conversation, currentState, liveRun, handoffState = { stage: "idle" }) {
  const appendStream = currentState.appendStream || {};
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const handoffVisible = handoffState.stage === "pending-assistant" && sessionStatus.selectedThreadSse;
  const retainedTerminalVisible = shouldRetainInlineTerminalPhase(
    appendStream,
    liveRun,
    sessionStatus.selectedThreadSse,
    sessionStatus.renderSource,
    sessionStatus.streamStatus,
  );
  const sessionIndicator = selectedThreadLiveSessionIndicator(currentState, conversation, liveRun, handoffState);
  const liveVisible =
    sessionStatus.liveOwned &&
    liveRun?.visible &&
    liveRun.phase &&
    liveRun.phase !== "IDLE" &&
    liveRun.state !== "sending" &&
    liveRun.state !== "generating" &&
    (!liveRun.terminal || retainedTerminalVisible);
  const degradedVisible =
    !handoffVisible &&
    !liveVisible &&
    sessionIndicator.visible &&
    !sessionIndicator.owned &&
    (sessionIndicator.state === "reconnecting" || sessionIndicator.state === "polling");
  return {
    conversationId: sessionStatus.conversationId,
    selectedThreadSseOwned: sessionStatus.selectedThreadSse,
    renderSource: sessionStatus.renderSource,
    status: sessionStatus.streamStatus,
    transport: sessionStatus.transport,
    sessionIndicator,
    handoffVisible,
    retainedTerminalVisible,
    liveVisible,
    degradedVisible,
    visible: handoffVisible || liveVisible || degradedVisible,
  };
}

function shouldShowComposerLiveStrip(conversation, currentState, liveRun, handoffState = { stage: "idle" }) {
  const inlineState = selectedThreadInlineSessionState(conversation, currentState, liveRun, handoffState);
  if (inlineState.visible) {
    return false;
  }
  if (
    !inlineState.selectedThreadSseOwned ||
    !liveRun?.visible ||
    liveRun.terminal ||
    !liveRun.phase ||
    liveRun.phase === "IDLE"
  ) {
    return false;
  }

  if (inlineState.status !== "live") {
    return false;
  }

  return inlineState.renderSource === "sse";
}

function renderInlineSessionBlock(conversation, currentState, liveRun, handoffState) {
  return "";
}

function autonomyChipTone(value) {
  if (value === "EXPECTED" || value === "ACCEPTABLE" || value === "none") {
    return "healthy";
  }
  if (value === "DEGRADED" || value === "DISQUALIFYING") {
    return "blocked";
  }
  return "neutral";
}

export function buildAutonomySummary(goal) {
  const iteration = latestIteration(goal);
  if (!goal || !iteration) {
    return null;
  }

  const intendedPath = iteration.intended_path || {};
  const pathVerdict = String(intendedPath.verdict || "").toLowerCase() === "expected" ? "EXPECTED" : "DEGRADED";
  const verifierAcceptability = summarizeVerifierAcceptability(iteration);
  const blockerReason = String(iteration.continuation_blocker_reason || goal.stop_reason || "none");
  const degradedSignals = Array.isArray(intendedPath.degraded_signals) ? intendedPath.degraded_signals : [];
  const expectedPath = String(intendedPath.expected_path || "").trim() || "unknown";
  return {
    goalTitle: goal.title || "Autonomy Goal",
    goalStatus: goal.status || "unknown",
    iteration: String(iteration.iteration ?? ""),
    pathVerdict,
    verifierAcceptability,
    blockerReason,
    expectedPath,
    degradedSignals,
    heading: `${goal.title || "Autonomy Goal"} · ${goal.status || "unknown"} · iteration ${iteration.iteration}`,
  };
}

function summarizeInlineAutonomy(currentState, conversation) {
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  const autonomySummary = liveAutonomy.summary;
  if (!liveAutonomy.visible || !autonomySummary) {
    return "";
  }
  const blockerReason = String(autonomySummary.blockerReason || "none");
  const degradedSignals = Array.isArray(autonomySummary.degradedSignals) ? autonomySummary.degradedSignals : [];
  return `
    <div class="session-inline-autonomy" data-live-autonomy="true" data-live-autonomy-owned="${liveAutonomy.owned ? "true" : "false"}" data-live-autonomy-presentation="${escapeHtml(liveAutonomy.presentation)}" data-live-autonomy-label="${escapeHtml(String(liveAutonomy.label || ""))}" data-live-autonomy-reason="${escapeHtml(String(liveAutonomy.reason || "idle"))}" data-live-phase-label="${escapeHtml(String(phaseProgression.label || ""))}" data-live-phase-owned="${phaseProgression.owned ? "true" : "false"}" data-live-phase-authoritative="${phaseProgression.authoritative ? "true" : "false"}" data-live-phase-source="${escapeHtml(String(phaseProgression.source || "none"))}" data-autonomy-path-verdict="${escapeHtml(String(autonomySummary.pathVerdict || "unknown").toLowerCase())}" data-autonomy-verifier-acceptability="${escapeHtml(String(autonomySummary.verifierAcceptability || "pending").toLowerCase())}" data-autonomy-blocker-reason="${escapeHtml(blockerReason)}" data-autonomy-iteration="${escapeHtml(String(autonomySummary.iteration || ""))}" data-autonomy-source="${escapeHtml(String(liveAutonomy.source || autonomySummary.source || "none"))}" data-autonomy-freshness-state="${escapeHtml(String(liveAutonomy.freshnessState || autonomySummary.freshnessState || "stale-or-missing"))}" data-autonomy-fallback-allowed="${liveAutonomy.fallbackAllowed ? "true" : "false"}" data-autonomy-generated-at="${escapeHtml(String(autonomySummary.generatedAt || ""))}">
      <div class="autonomy-chip-row autonomy-chip-row-compact">
        <span class="autonomy-chip ${liveAutonomy.owned ? "healthy" : liveAutonomy.presentation === "degraded" ? "warning" : "neutral"}">${escapeHtml(String(liveAutonomy.label || "SESSION"))}</span>
        <span class="autonomy-chip ${phaseProgression.owned ? "healthy" : liveAutonomy.presentation === "degraded" ? "warning" : "neutral"}">${escapeHtml(String(phaseProgression.label || "UNKNOWN"))}</span>
        <span class="autonomy-chip ${autonomyChipTone(autonomySummary.pathVerdict)}">${escapeHtml(String(autonomySummary.pathVerdict || "UNKNOWN"))}</span>
        <span class="autonomy-chip ${autonomyChipTone(autonomySummary.verifierAcceptability)}">${escapeHtml(String(autonomySummary.verifierAcceptability || "PENDING"))}</span>
        <span class="autonomy-chip ${blockerTone(blockerReason)}">BLOCKER ${escapeHtml(blockerReason.toUpperCase())}</span>
      </div>
      <div class="session-inline-autonomy-meta">
        <p class="session-inline-autonomy-item"><span>Iteration</span>${escapeHtml(String(autonomySummary.iteration || ""))}</p>
        <p class="session-inline-autonomy-item"><span>Path</span>${escapeHtml(String(autonomySummary.expectedPath || "unknown"))}</p>
        <p class="session-inline-autonomy-item"><span>Signals</span>${escapeHtml(degradedSignals.length ? degradedSignals.join(", ") : "none")}</p>
        <p class="session-inline-autonomy-item"><span>Phase</span>${escapeHtml(String(phaseProgression.reason || "healthy"))}</p>
      </div>
    </div>
  `;
}

function renderTranscriptMilestones(currentState, conversation) {
  const milestoneModel = deriveSelectedThreadTimelineMilestones(currentState, conversation);
  if (!milestoneModel.visible) {
    return "";
  }
  return `
    <div class="timeline-live-row timeline-live-row-milestones" data-live-milestones="true" data-live-milestones-source="${escapeHtml(String(milestoneModel.source || "none"))}" data-live-milestones-phase="${escapeHtml(String(milestoneModel.currentLabel || "UNKNOWN"))}">
      ${milestoneModel.items
        .map(
          (item) => `<span class="autonomy-chip ${
            item.state === "complete" ? "healthy" : item.state === "active" ? "neutral" : item.state === "blocked" ? "blocked" : ""
          }" data-milestone-key="${escapeHtml(item.key)}" data-milestone-state="${escapeHtml(item.state)}">${escapeHtml(item.label)}</span>`,
        )
        .join("")}
    </div>
  `;
}

function renderTranscriptLiveActivity(conversation, currentState, liveRun) {
  const handoffState = pendingHandoffState(conversation, currentState);
  const inlineState = selectedThreadInlineSessionState(conversation, currentState, liveRun, handoffState);
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  const milestoneModel = deriveSelectedThreadTimelineMilestones(currentState, conversation);
  const { handoffVisible, degradedVisible, sessionIndicator } = inlineState;
  if (!handoffVisible && !degradedVisible && (!phaseProgression.visible || !liveAutonomy.visible)) {
    return "";
  }
  const liveOwned = !handoffVisible && !degradedVisible && liveAutonomy.owned;
  const phaseLabel = degradedVisible
    ? String(sessionIndicator.label || "POLLING").toUpperCase()
    : handoffVisible
      ? "HANDOFF"
      : String(phaseProgression.label || liveRun.phase || "LIVE").toUpperCase();
  const tone = degradedVisible ? "warning" : handoffVisible ? "neutral" : liveOwned ? transcriptLiveTone(liveRun) : "warning";
  const detail = degradedVisible
    ? sessionIndicator.reason === "session-rotation"
      ? "세션 회전이 감지되어 선택된 대화의 live SSE 소유권이 끊겼습니다. fallback 경로로 상태를 복구하는 중입니다."
      : sessionIndicator.reason === "retrying"
        ? "선택된 대화의 live SSE 연결이 재시도 중입니다. fallback 경로로 현재 상태를 이어받는 중입니다."
        : sessionIndicator.state === "reconnecting"
          ? "선택된 대화의 append stream을 다시 붙이는 중입니다. 복구가 끝나면 live SSE 소유권으로 되돌아갑니다."
          : "선택된 대화의 live SSE 소유권이 약화되어 polling fallback으로 상태를 유지하는 중입니다."
    : handoffVisible
      ? "서버 handoff가 확인되어 첫 live assistant append를 기다리는 중입니다."
      : simplifyText(phaseDetailHint(liveRun) || liveRun.detail || "");
  const appendStream = currentState.appendStream || {};
  const appendId = Number(appendStream.lastLiveAppendId || appendStream.lastAppendId || 0);
  const autonomySummary = liveAutonomy.summary;
  const milestoneLane = degradedVisible ? "" : liveOwned ? renderTranscriptMilestones(currentState, conversation) : "";
  const provenanceLabel = degradedVisible
    ? String(sessionIndicator.label || "POLLING")
    : handoffVisible
      ? "HANDOFF"
      : liveOwned
        ? "SSE LIVE"
        : String(liveAutonomy.label || "FALLBACK");
  const metaPhase = degradedVisible ? phaseLabel : handoffVisible ? "HANDOFF" : String(phaseProgression.label || "LIVE");
  const metaReason = degradedVisible ? String(sessionIndicator.reason || "polling-fallback").toUpperCase() : "";
  const pathVerdict = liveOwned ? String(autonomySummary?.pathVerdict || "UNKNOWN").toUpperCase() : "";
  const verifierAcceptability = liveOwned ? String(autonomySummary?.verifierAcceptability || "PENDING").toUpperCase() : "";
  const blockerReason = liveOwned ? String(autonomySummary?.blockerReason || "none").toUpperCase() : "";
  return `
    <article class="timeline-item live-activity" data-live-activity-turn="true" data-live-session-event="${liveOwned ? "true" : "false"}" data-live-session-lane="${escapeHtml(liveOwned ? "selected-thread" : degradedVisible ? "degraded" : handoffVisible ? "handoff" : "fallback")}" data-live-milestones-visible="${liveOwned && milestoneModel.visible ? "true" : "false"}" data-live-milestones-phase="${escapeHtml(liveOwned ? String(milestoneModel.currentLabel || phaseLabel) : "")}" data-live-path-verdict="${escapeHtml(pathVerdict)}" data-live-verifier-acceptability="${escapeHtml(verifierAcceptability)}" data-live-blocker-reason="${escapeHtml(blockerReason)}" data-live-run-state="${escapeHtml(handoffVisible ? "handoff" : degradedVisible ? String(sessionIndicator.state || "polling") : phaseProgression.state || liveRun.state)}" data-live-run-phase="${escapeHtml(phaseLabel)}" data-live-run-source="${escapeHtml(degradedVisible ? String(sessionIndicator.source || "polling") : handoffVisible ? "handoff" : phaseProgression.source || liveRun.source)}" data-live-owned="${liveOwned ? "true" : "false"}" data-live-autonomy-presentation="${escapeHtml(degradedVisible ? "degraded" : handoffVisible ? "handoff" : liveAutonomy.presentation)}" data-live-reason="${escapeHtml(degradedVisible ? String(sessionIndicator.reason || "polling-fallback") : handoffVisible ? "handoff" : String(liveAutonomy.reason || "healthy"))}" data-append-id="${appendId}" data-append-source="sse-live-activity">
      <p class="timeline-kind">${liveOwned ? "세션 진행" : "실시간 진행"}</p>
      <div class="timeline-live-row">
        <span class="timeline-live-chip" data-tone="${degradedVisible ? "warning" : handoffVisible ? "neutral" : liveOwned ? "neutral" : "warning"}">${escapeHtml(degradedVisible ? "DEGRADED" : handoffVisible ? "HANDOFF" : String(liveAutonomy.label || "LIVE"))}</span>
        <span class="timeline-live-chip" data-tone="${escapeHtml(tone)}">${escapeHtml(phaseLabel)}</span>
        ${liveOwned ? `<span class="timeline-live-chip" data-tone="${escapeHtml(autonomyChipTone(pathVerdict))}">${escapeHtml(pathVerdict)}</span>` : ""}
        ${liveOwned ? `<span class="timeline-live-chip" data-tone="${escapeHtml(autonomyChipTone(verifierAcceptability))}">${escapeHtml(verifierAcceptability)}</span>` : ""}
        ${liveOwned ? `<span class="timeline-live-chip" data-tone="${escapeHtml(blockerTone(String(autonomySummary?.blockerReason || "none")))}">BLOCKER ${escapeHtml(blockerReason)}</span>` : ""}
      </div>
      ${milestoneLane}
      <p class="timeline-body">${escapeHtml(detail || "선택된 대화의 최신 live 진행 상태를 반영하는 중입니다.")}</p>
      <p class="timeline-meta">selected thread · ${escapeHtml(metaPhase)}${phaseProgression.jobId || liveRun.jobId ? ` · ${escapeHtml(String(phaseProgression.jobId || liveRun.jobId || ""))}` : ""}${metaReason ? ` · ${escapeHtml(metaReason)}` : ""} · <span class="timeline-provenance">${escapeHtml(provenanceLabel)}</span></p>
    </article>
  `;
}

function renderRestoreSessionTimeline(currentState) {
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, null);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, null);
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, null);
  if (!liveAutonomy.visible || liveAutonomy.presentation !== "restore" || !phaseProgression.visible) {
    return "";
  }
  const phaseLabel = String(phaseProgression.label || liveAutonomy.label || "ATTACH").toUpperCase();
  const detail =
    phaseLabel === "RESUME"
      ? "저장된 선택 대화에 다시 연결하는 중입니다. append SSE 복구가 완료되면 같은 세션이 이어집니다."
      : "저장된 선택 대화에 attach 중입니다. 첫 bootstrap이 완료되면 같은 세션이 live 상태로 이어집니다.";
  return `
    <article class="timeline-item live-activity" data-live-activity-turn="true" data-live-run-state="${escapeHtml(String(phaseProgression.state || "attach"))}" data-live-run-phase="${escapeHtml(phaseLabel)}" data-live-run-source="sse" data-live-owned="false" data-live-autonomy-presentation="restore" data-live-reason="${escapeHtml(String(liveAutonomy.reason || "saved-restore-attach"))}" data-live-restore="true" data-live-restore-stage="${escapeHtml(String(sessionStatus.restoreStage || "none"))}" data-live-restore-path="${escapeHtml(String(sessionStatus.restorePath || "none"))}" data-live-restore-provenance="${escapeHtml(String(sessionStatus.restoreProvenance || "none"))}" data-append-id="0" data-append-source="sse-live-activity">
      <p class="timeline-kind">실시간 진행</p>
      <div class="timeline-live-row">
        <span class="timeline-live-chip" data-tone="neutral">RESTORE</span>
        <span class="timeline-live-chip" data-tone="${phaseLabel === "RESUME" ? "warning" : "neutral"}">${escapeHtml(phaseLabel)}</span>
      </div>
      <p class="timeline-body">${escapeHtml(detail)}</p>
      <p class="timeline-meta">selected thread · ${escapeHtml(phaseLabel)} · <span class="timeline-provenance">SSE RESTORE</span></p>
    </article>
  `;
}

function sessionTimelineEventModel(item) {
  const type = String(item?.type || "");
  const status = String(item?.status || "").toLowerCase();
  const jobId = String(item?.job_id || "").trim();
  const suffix = jobId ? ` · ${jobId}` : "";
  if (type === "job.running") {
    return { milestone: "ACTIVE", phase: "RUNNING", tone: "neutral", verdict: "EXPECTED", verdictTone: "healthy" };
  }
  if (type === "goal.proposal.phase.started") {
    return { milestone: "PHASE", phase: "PROPOSAL", tone: "neutral", verdict: "EXPECTED", verdictTone: "healthy" };
  }
  if (type === "goal.review.phase.started") {
    return { milestone: "PHASE", phase: "REVIEW", tone: "neutral", verdict: "EXPECTED", verdictTone: "healthy" };
  }
  if (type === "goal.verify.phase.started") {
    return { milestone: "PHASE", phase: "VERIFY", tone: "neutral", verdict: "EXPECTED", verdictTone: "healthy" };
  }
  if (type === "goal.proposal.auto_apply.started") {
    return { milestone: "PHASE", phase: "AUTO APPLY", tone: "warning", verdict: "EXPECTED", verdictTone: "healthy" };
  }
  if (type === "proposal.ready") {
    return { milestone: "READY", phase: "READY", tone: "healthy", verdict: "ACCEPTABLE", verdictTone: "healthy" };
  }
  if (type === "codex.exec.applied" || status === "applied") {
    return { milestone: "APPLY", phase: "APPLIED", tone: "healthy", verdict: "ACCEPTABLE", verdictTone: "healthy" };
  }
  if (type === "runtime.exception" || status === "failed") {
    return { milestone: "FAILED", phase: "FAILED", tone: "danger", verdict: "DISQUALIFYING", verdictTone: "danger" };
  }
  if (status === "completed") {
    return { milestone: "DONE", phase: "COMPLETED", tone: "healthy", verdict: "ACCEPTABLE", verdictTone: "healthy" };
  }
  if (!suffix) {
    return null;
  }
  return null;
}

function renderSessionTimelineEvent(item) {
  const model = sessionTimelineEventModel(item);
  if (!model) {
    return "";
  }
  const body = simplifyText(item?.body || "");
  const jobId = String(item?.job_id || "").trim();
  const meta = `selected thread · session event${jobId ? ` · ${escapeHtml(jobId)}` : ""}${item.delivery_source === "sse" ? ' · <span class="timeline-provenance">SSE LIVE</span>' : ""}`;
  return `
    <article class="timeline-item session-event" data-session-event="true" data-session-phase="${escapeHtml(model.phase)}" data-session-milestone="${escapeHtml(model.milestone)}" data-session-verdict="${escapeHtml(model.verdict.toLowerCase())}" data-append-id="${Number(item.append_id || 0)}" data-append-source="${escapeHtml(String(item.delivery_source || "snapshot"))}">
      <p class="timeline-kind">세션 진행</p>
      <div class="timeline-live-row">
        <span class="timeline-live-chip" data-tone="neutral">${escapeHtml(model.milestone)}</span>
        <span class="timeline-live-chip" data-tone="${escapeHtml(model.tone)}">${escapeHtml(model.phase)}</span>
        <span class="timeline-live-chip" data-tone="${escapeHtml(model.verdictTone)}">${escapeHtml(model.verdict)}</span>
      </div>
      <p class="timeline-body">${escapeHtml(body || `${eventLabel(item.type)} 이벤트가 선택된 세션 타임라인에 반영되었습니다.`)}</p>
      <p class="timeline-meta">${meta}</p>
    </article>
  `;
}

function shouldCollapseHealthySessionEvent(item, currentState, conversation, liveRun) {
  if (!item || item.kind !== "event") {
    return false;
  }
  const footerDock = selectedThreadFooterDockModel(currentState, conversation, liveRun);
  if (!footerDock.visible) {
    return false;
  }
  if (String(item.delivery_source || "").toLowerCase() !== "sse") {
    return false;
  }
  return Boolean(sessionTimelineEventModel(item));
}

function pendingHandoffState(conversation, currentState) {
  const conversationId = String(conversation?.conversation_id || "");
  const pendingOutgoing = currentState.pendingOutgoing || {};
  const appendStream = currentState.appendStream || {};
  const selectedThreadSseOwned =
    conversationId &&
    String(appendStream.conversationId || "") === conversationId &&
    String(appendStream.transport || "polling").toLowerCase() === "sse";
  if (!conversationId || pendingOutgoing.conversationId !== conversationId) {
    return {
      stage: "idle",
      pendingUserCount: 0,
      pendingAssistantCount: 0,
      items: [],
    };
  }
  if (pendingOutgoing.status === "sending-user") {
    return {
      stage: "pending-user",
      pendingUserCount: 1,
      pendingAssistantCount: 0,
      items: [
        {
          kind: "message",
          role: "user",
          body: pendingOutgoing.body,
          created_at: pendingOutgoing.createdAt || new Date().toISOString(),
          sortAt: pendingOutgoing.createdAt || new Date().toISOString(),
          append_id: 0,
          delivery_source: "local-pending",
          pending_local: true,
        },
      ],
    };
  }
  if (pendingOutgoing.status === "awaiting-assistant") {
    if (!selectedThreadSseOwned) {
      return {
        stage: "idle",
        pendingUserCount: 0,
        pendingAssistantCount: 0,
        items: [],
      };
    }
    return {
      stage: "pending-assistant",
      pendingUserCount: 0,
      pendingAssistantCount: 1,
      items: [
        {
          kind: "message",
          role: "assistant",
          body: "응답을 생성하는 중입니다.",
          created_at: pendingOutgoing.assistantCreatedAt || new Date().toISOString(),
          sortAt: pendingOutgoing.assistantCreatedAt || new Date().toISOString(),
          append_id: 0,
          delivery_source: "local-assistant-placeholder",
          pending_assistant: true,
        },
      ],
    };
  }
  return {
    stage: "idle",
    pendingUserCount: 0,
    pendingAssistantCount: 0,
    items: [],
  };
}

function syncJumpToLatest(dom, currentState, conversationId, renderSource) {
  if (!dom.jumpToLatestButton) {
    return;
  }
  const footerFollow = selectedThreadFooterFollowState(dom, currentState, conversationId, renderSource);
  const isVisible = footerFollow.visible ? false : footerFollow.detached;
  const stateLabel = footerFollow.stateLabel;
  const detailLabel = footerFollow.detailLabel;
  dom.jumpToLatestButton.hidden = !isVisible;
  dom.jumpToLatestButton.dataset.followConversationId = conversationId || "";
  dom.jumpToLatestButton.dataset.followOwned = footerFollow.visible ? "none" : footerFollow.liveOwned ? "selected-thread" : "none";
  dom.jumpToLatestButton.dataset.followMode = footerFollow.isFollowing ? "following" : "paused";
  dom.jumpToLatestButton.dataset.followState = isVisible ? footerFollow.followState : "hidden";
  dom.jumpToLatestButton.dataset.followCount = String(isVisible ? footerFollow.unseenCount : 0);
  dom.jumpToLatestButton.dataset.followRenderSource = renderSource || "snapshot";
  dom.jumpToLatestButton.setAttribute(
    "aria-label",
    isVisible ? `${stateLabel}. ${detailLabel}. 최신 응답으로 이동` : "최신 응답으로 이동",
  );
  dom.jumpToLatestButton.innerHTML = isVisible
    ? `<span class="jump-to-latest-chip">${stateLabel}</span><span class="jump-to-latest-copy">${detailLabel}</span>`
    : '<span class="jump-to-latest-chip">NEW</span><span class="jump-to-latest-copy">최신 응답으로 이동</span>';
}

function selectedThreadFooterFollowState(dom, currentState, conversationId, renderSource) {
  const liveFollow = currentState.liveFollow || {};
  const unseenCount = Math.max(
    Number(liveFollow.pendingAppendCount || 0),
    Number(liveFollow.lastAppendId || 0) - Number(liveFollow.lastSeenAppendId || 0),
  );
  const streamState = String(dom.threadScroller?.dataset.streamState || "offline").toLowerCase();
  const terminalIdle = String(dom.threadScroller?.dataset.sessionTerminal || "false") === "true";
  const liveOwned =
    Boolean(conversationId) &&
    String(dom.threadScroller?.dataset.sessionOwner || "none") === "selected-thread" &&
    renderSource === "sse" &&
    streamState === "live" &&
    !terminalIdle;
  const detached = !Boolean(liveFollow.isFollowing);
  const hasBacklog = unseenCount > 0;
  const followState = hasBacklog ? "new" : "paused";
  const stateLabel = followState === "new" ? "NEW" : "PAUSED";
  const detailLabel =
    followState === "new"
      ? unseenCount > 1
        ? `새 live append ${unseenCount}개`
        : "새 live append"
      : "live follow paused";
  return {
    liveOwned,
    isFollowing: Boolean(liveFollow.isFollowing),
    detached: Boolean(liveOwned && detached),
    visible: Boolean(liveOwned && detached),
    followState,
    unseenCount,
    stateLabel,
    detailLabel,
  };
}

export function updateLiveFollowFromScroll(dom, currentState) {
  const liveFollow = currentState.liveFollow || {};
  const isNearBottom = isThreadNearBottom(dom.threadScroller);
  const latestAppendId = Number(dom.threadScroller?.dataset.lastAppendId || 0);
  currentState.liveFollow = {
    ...liveFollow,
    isFollowing: isNearBottom,
    jumpVisible: isNearBottom ? false : Boolean(liveFollow.jumpVisible),
    lastSeenAppendId: isNearBottom ? latestAppendId : Number(liveFollow.lastSeenAppendId || 0),
    pendingAppendCount: isNearBottom ? 0 : Number(liveFollow.pendingAppendCount || 0),
  };
  syncJumpToLatest(dom, currentState, liveFollow.conversationId || "", dom.threadScroller?.dataset.renderSource || "snapshot");
}

export function jumpToLatest(dom, currentState) {
  if (!dom.threadScroller) {
    return;
  }
  dom.threadScroller.scrollTop = dom.threadScroller.scrollHeight;
  const liveFollow = currentState.liveFollow || {};
  currentState.liveFollow = {
    ...liveFollow,
    isFollowing: true,
    jumpVisible: false,
    lastSeenAppendId: Number(dom.threadScroller.dataset.lastAppendId || 0),
    pendingAppendCount: 0,
  };
  syncJumpToLatest(dom, currentState, liveFollow.conversationId || "", dom.threadScroller.dataset.renderSource || "snapshot");
}

function deriveLiveRunState(conversation, currentState) {
  const jobId = sessionAuthorityJobId(conversation, currentState);
  const sessionPhase = selectedThreadSessionPhase(conversation, currentState);
  const pendingOutgoing = currentState.pendingOutgoing || {};
  const sessionPhaseEventType = String(sessionPhase.eventType || "");

  if (!conversation?.conversation_id) {
    return runStateSnapshot({
      visible: false,
      state: "done",
      phase: "IDLE",
      detail: "",
      source: "none",
      tone: "idle",
      jobId: "",
      terminal: false,
    });
  }

  if (pendingOutgoing.status === "sending-user" && pendingOutgoing.conversationId === conversation.conversation_id) {
    return runStateSnapshot({
      visible: true,
      state: "sending",
      phase: "SENDING",
      detail: "메시지를 live conversation에 등록하는 중입니다.",
      source: "local-submit",
      tone: "thinking",
      jobId,
      terminal: false,
    });
  }

  if (
    pendingOutgoing.status === "awaiting-assistant" &&
    pendingOutgoing.conversationId === conversation.conversation_id &&
    String(currentState.appendStream?.conversationId || "") === conversation.conversation_id &&
    String(currentState.appendStream?.transport || "polling").toLowerCase() === "sse"
  ) {
    return runStateSnapshot({
      visible: true,
      state: "generating",
      phase: "ACCEPTED",
      detail: "에이전트가 첫 응답을 준비 중입니다.",
      source: "accepted-event",
      tone: "thinking",
      jobId,
      terminal: false,
    });
  }

  if (sessionPhase.authoritative && sessionPhase.value === "FAILED") {
    return runStateSnapshot({
      visible: true,
      state: "failed",
      phase: "FAILED",
      detail: "선택된 대화의 authoritative SSE phase가 실패를 보고했습니다.",
      source: sessionPhase.source,
      tone: "done",
      jobId: sessionPhase.jobId || jobId,
      terminal: true,
      appendId: sessionPhase.appendId,
    });
  }
  if (sessionPhase.authoritative && sessionPhase.value === "VERIFY") {
    return runStateSnapshot({
      visible: true,
      state: "verify-phase",
      phase: "VERIFY",
      detail: "선택된 대화의 authoritative SSE phase가 검증 단계를 보고했습니다.",
      source: sessionPhase.source,
      tone: "running",
      jobId: sessionPhase.jobId || jobId,
      terminal: false,
      appendId: sessionPhase.appendId,
    });
  }
  if (sessionPhase.authoritative && sessionPhase.value === "REVIEW") {
    return runStateSnapshot({
      visible: true,
      state: "review-phase",
      phase: "REVIEW",
      detail: "선택된 대화의 authoritative SSE phase가 리뷰 단계를 보고했습니다.",
      source: sessionPhase.source,
      tone: "thinking",
      jobId: sessionPhase.jobId || jobId,
      terminal: false,
      appendId: sessionPhase.appendId,
    });
  }
  if (sessionPhase.authoritative && sessionPhaseEventType === "goal.proposal.auto_apply.started") {
    return runStateSnapshot({
      visible: true,
      state: "auto-apply",
      phase: "AUTO APPLY",
      detail: "선택된 대화의 authoritative SSE phase가 자동 적용 단계를 보고했습니다.",
      source: sessionPhase.source,
      tone: "waiting",
      jobId: sessionPhase.jobId || jobId,
      terminal: false,
      appendId: sessionPhase.appendId,
    });
  }
  if (sessionPhase.authoritative && sessionPhase.value === "PROPOSAL") {
    return runStateSnapshot({
      visible: true,
      state: "proposal-phase",
      phase: "PROPOSAL",
      detail: "선택된 대화의 authoritative SSE phase가 제안 단계를 보고했습니다.",
      source: sessionPhase.source,
      tone: "thinking",
      jobId: sessionPhase.jobId || jobId,
      terminal: false,
      appendId: sessionPhase.appendId,
    });
  }
  if (sessionPhase.authoritative && sessionPhase.value === "READY") {
    return runStateSnapshot({
      visible: true,
      state: "proposal-ready",
      phase: "READY",
      detail: "선택된 대화의 authoritative SSE phase가 ready 상태를 보고했습니다.",
      source: sessionPhase.source,
      tone: "waiting",
      jobId: sessionPhase.jobId || jobId,
      terminal: true,
      appendId: sessionPhase.appendId,
    });
  }
  if (sessionPhase.authoritative && sessionPhase.value === "APPLIED") {
    return runStateSnapshot({
      visible: true,
      state: "applied",
      phase: "APPLIED",
      detail: "선택된 대화의 authoritative SSE phase가 applied 상태를 보고했습니다.",
      source: sessionPhase.source,
      tone: "done",
      jobId: sessionPhase.jobId || jobId,
      terminal: true,
      appendId: sessionPhase.appendId,
    });
  }
  return runStateSnapshot({
    visible: true,
    state: sessionPhase.value === "LIVE" ? "live" : "unknown",
    phase: sessionPhase.value === "LIVE" ? "LIVE" : "UNKNOWN",
    detail:
      sessionPhase.value === "LIVE"
        ? "선택된 대화가 live SSE에 연결되어 있지만 authoritative phase는 아직 확정되지 않았습니다."
        : "선택된 대화의 authoritative phase를 아직 확인하지 못했습니다.",
    source: sessionPhase.source,
    tone: sessionPhase.value === "LIVE" ? "running" : "idle",
    jobId: sessionPhase.jobId || jobId,
    terminal: false,
    appendId: sessionPhase.appendId,
  });
}

function latestMeaningfulConversationEvent(conversation, currentState) {
  const liveAuthorityEvent = selectedThreadSseAuthorityEvent(conversation, currentState);
  if (liveAuthorityEvent) {
    return liveAuthorityEvent;
  }
  const relevantEvents = sessionAuthorityEvents(conversation, currentState);
  for (let index = relevantEvents.length - 1; index >= 0; index -= 1) {
    const event = relevantEvents[index];
    if (isSessionAuthorityEvent(event)) {
      return event;
    }
  }
  return relevantEvents.length ? relevantEvents[relevantEvents.length - 1] : null;
}

function collapsedSessionSummary(conversation, currentState, liveRun) {
  const latestEvent = latestMeaningfulConversationEvent(conversation, currentState);
  const latestType = String(latestEvent?.type || "");
  const latestStatus = String(latestEvent?.status || "").toLowerCase();
  const appendId = Number(currentState.appendStream?.lastLiveAppendId || currentState.appendStream?.lastAppendId || maxConversationAppendId(conversation) || 0);
  const source = String(latestEvent?.delivery_source || currentState.appendStream?.lastRenderSource || "snapshot").toLowerCase();
  let outcomeLabel = liveRun.terminal ? "최근 실행 완료" : "대기 중";
  if (latestType === "goal.proposal.auto_apply.started") {
    outcomeLabel = "자동 적용";
  } else if (latestType.startsWith("goal.verify.phase.")) {
    outcomeLabel = "검증 단계";
  } else if (latestType.startsWith("goal.review.phase.")) {
    outcomeLabel = "리뷰 단계";
  } else if (latestType.startsWith("goal.proposal.phase.")) {
    outcomeLabel = "제안 단계";
  } else if (latestType === "proposal.ready") {
    outcomeLabel = "제안 준비";
  } else if (latestType === "codex.exec.applied" || latestStatus === "applied") {
    outcomeLabel = "적용 완료";
  } else if (latestType === "runtime.exception" || latestStatus === "failed") {
    outcomeLabel = "실패 기록";
  } else if (latestType) {
    outcomeLabel = eventLabel(latestType);
  }
  return {
    state: liveRun.terminal ? `DONE · ${outcomeLabel.toUpperCase()}` : `IDLE · ${(liveRun.phase || outcomeLabel).toUpperCase()}`,
    detail: liveRun.terminal
      ? `${outcomeLabel} 결과를 유지한 채 rail을 접었습니다.`
      : latestEvent
        ? `${outcomeLabel} 이후 현재는 idle 상태입니다.`
        : "현재 실행 중인 작업은 없지만 최근 결과 요약은 여기에서 다시 펼쳐볼 수 있습니다.",
    meta: `${source === "sse" ? "SSE" : source === "snapshot" ? "SNAPSHOT" : source.toUpperCase()} · append #${appendId || 0}`,
  };
}

function transportChip(status, presentation) {
  if (presentation === "sending") {
    return { label: "SEND", tone: "thinking" };
  }
  if (status === "live") {
    return { label: "LIVE", tone: "healthy" };
  }
  if (status === "reconnecting") {
    return { label: "RECONNECT", tone: "warning" };
  }
  if (status === "connecting") {
    return { label: "OPEN", tone: "neutral" };
  }
  return { label: "OFFLINE", tone: "danger" };
}

function phaseChip(liveRun, presentation) {
  if (presentation === "sending" && liveRun.state === "sending") {
    return { label: "SENDING", tone: "neutral" };
  }
  if (presentation === "sending" && liveRun.state === "generating") {
    return { label: "ACCEPTED", tone: "neutral" };
  }
  if (liveRun.state === "proposal-ready") {
    return { label: "READY", tone: "healthy" };
  }
  if (liveRun.state === "applied") {
    return { label: "APPLIED", tone: "healthy" };
  }
  if (liveRun.state === "failed") {
    return { label: "FAILED", tone: "danger" };
  }
  if (liveRun.phase) {
    return {
      label: liveRun.phase,
      tone:
        liveRun.tone === "done"
          ? "healthy"
          : liveRun.tone === "waiting"
            ? "warning"
            : liveRun.tone === "running"
              ? "danger"
              : liveRun.tone === "thinking"
                ? "neutral"
                : "muted",
    };
  }
  return { label: "IDLE", tone: "muted" };
}

function proposalChip(liveRun) {
  if (liveRun.state === "proposal-ready") {
    return { label: "READY", tone: "healthy" };
  }
  if (liveRun.state === "applied") {
    return { label: "APPLIED", tone: "healthy" };
  }
  if (liveRun.state === "failed") {
    return { label: "BLOCKED", tone: "warning" };
  }
  return { label: "NONE", tone: "muted" };
}

function phaseDetailHint(liveRun) {
  if (liveRun.state === "proposal-phase") {
    return "HYPOTHESIS";
  }
  if (liveRun.state === "review-phase") {
    return "REVIEW SIGNAL";
  }
  if (liveRun.state === "verify-phase") {
    return "VERIFY SIGNAL";
  }
  if (liveRun.state === "auto-apply") {
    return "AUTO APPLY";
  }
  if (liveRun.state === "proposal-ready") {
    return "READY TO APPLY";
  }
  if (liveRun.state === "applied") {
    return "APPLY COMPLETE";
  }
  if (liveRun.state === "accepted" || liveRun.phase === "ACCEPTED") {
    return "FIRST APPEND";
  }
  if (liveRun.state === "generating") {
    return "GENERATING";
  }
  if (liveRun.state === "failed") {
    return "CHECK FAILURE";
  }
  if (liveRun.state === "sending") {
    return "SEND LOCK";
  }
  return liveRun.detail ? compactTargetLabel(liveRun.detail, "SESSION ACTIVE") : "SESSION ACTIVE";
}

function composerActionHint(status, presentation, liveRun) {
  if (status === "reconnecting") {
    return "복구 중";
  }
  if (status === "offline") {
    return "복구 필요";
  }
  if (status === "connecting") {
    return "연결 중";
  }
  if (
    liveRun.state === "proposal-phase" ||
    liveRun.state === "review-phase" ||
    liveRun.state === "verify-phase" ||
    liveRun.state === "auto-apply" ||
    liveRun.state === "proposal-ready" ||
    liveRun.state === "applied"
  ) {
    return phaseDetailHint(liveRun);
  }
  if (liveRun.state === "proposal-ready") {
    return "적용 대기";
  }
  if (liveRun.state === "applied") {
    return "적용 완료";
  }
  if (liveRun.state === "failed") {
    return "실패 확인";
  }
  if (presentation === "sending") {
    return "전송 중";
  }
  if (liveRun.state === "accepted" || liveRun.phase === "ACCEPTED") {
    return "handoff 완료";
  }
  if (liveRun.state === "proposal-phase") {
    return "제안 중";
  }
  if (liveRun.state === "review-phase") {
    return "리뷰 중";
  }
  if (liveRun.state === "verify-phase") {
    return "검증 중";
  }
  if (liveRun.state === "auto-apply") {
    return "자동 적용";
  }
  if (liveRun.state === "running-tool" || liveRun.state === "waiting" || liveRun.state === "thinking") {
    return "실행 중";
  }
  if (liveRun.state === "generating") {
    return "응답 생성";
  }
  if (status === "live" || status === "reconnecting" || status === "connecting") {
    return "계속 입력";
  }
  return "입력 가능";
}

function threadMetaSummary(conversation, liveRun, messageCount, eventCount) {
  const parts = [conversation.updated_at ? new Date(conversation.updated_at).toLocaleString() : ""];
  if (liveRun?.visible && liveRun.phase && liveRun.phase !== "IDLE") {
    parts.push(compactPhaseDetailCopy(liveRun, String(liveRun.phase || "LIVE").toUpperCase()));
    return parts.filter(Boolean).join(" · ");
  }
  parts.push(`${messageCount} messages`);
  parts.push(`${eventCount} events`);
  return parts.filter(Boolean).join(" · ");
}

function renderThreadTransition(currentState, sessionStatus = deriveSelectedThreadSessionStatus(currentState, null)) {
  const targetTitle = String(sessionStatus.switchTargetTitle || sessionStatus.targetTitle || "선택한 대화").trim();
  return `
    <article class="timeline-transition" data-thread-transition="switching" data-thread-transition-phase="switching" data-thread-transition-conversation-id="${escapeHtml(String(sessionStatus.switchConversationId || sessionStatus.targetConversationId || ""))}" data-thread-transition-source="selected-thread-session">
      <p class="timeline-kind">세션 전환</p>
      <div class="timeline-transition-row">
        <span class="timeline-transition-chip">SWITCHING</span>
        <span class="timeline-transition-chip">${escapeHtml(targetTitle.toUpperCase())}</span>
      </div>
      <p class="timeline-body">이전 thread의 live 소유권을 정리했고, 새 선택 대화의 snapshot attach를 기다리는 중입니다.</p>
      <p class="timeline-meta">selected thread switching · snapshot attach pending</p>
    </article>
  `;
}

function selectedThreadWorkspacePlaceholder(currentState) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, null);
  const isSwitching = sessionStatus.presentation === "attach" && Boolean(sessionStatus.switchConversationId);
  const isRestore = !isSwitching && sessionStatus.presentation === "restore";
  if (isSwitching) {
    return {
      mode: "switching",
      conversationId: String(sessionStatus.switchConversationId || sessionStatus.targetConversationId || ""),
      title: String(sessionStatus.switchTargetTitle || sessionStatus.targetTitle || "대화 전환 중"),
      conversationState: "새 대화 스냅샷을 연결하는 중입니다.",
      workspaceSummary: "selected thread switching · target snapshot attach pending",
      timeline: renderThreadTransition(currentState, sessionStatus),
      liveRun: runStateSnapshot({
        visible: true,
        phase: "UNKNOWN",
        source: "thread-transition",
        tone: "neutral",
      }),
    };
  }
  if (isRestore) {
    return {
      mode: "restore",
      conversationId: String(sessionStatus.conversationId || ""),
      title: String(sessionStatus.conversationTitle || "저장된 대화 복구 중"),
      conversationState: sessionStatus.restoreResume
        ? "저장된 대화를 authoritative SSE resume으로 복구하는 중입니다."
        : "저장된 대화를 authoritative SSE attach로 복구하는 중입니다.",
      workspaceSummary: sessionStatus.restoreResume
        ? "selected thread restore · authoritative sse resume pending"
        : "selected thread restore · authoritative sse attach pending",
      timeline: renderRestoreSessionTimeline(currentState),
      liveRun: runStateSnapshot({
        visible: true,
        phase: sessionStatus.restoreResume ? "RESUME" : "ATTACH",
        source: "sse",
        tone: "neutral",
      }),
    };
  }
  return {
    mode: "empty",
    conversationId: "",
    title: "새 대화를 시작하세요",
    conversationState: "아직 대화 세션이 없습니다.",
    workspaceSummary: "선택된 대화가 없으면 현재 세션 맥락이 여기에 정리됩니다.",
    timeline: '<p class="timeline-empty">새 대화를 만들면 요청과 이벤트가 여기 쌓입니다.</p>',
    liveRun: runStateSnapshot({
      visible: true,
      phase: currentState.currentJobId ? "RUNNING" : "IDLE",
      source: "none",
      tone: currentState.currentJobId ? "running" : "idle",
    }),
  };
}

function sessionProvenance(status, lastAppendId, lastLiveAppendId, liveRun) {
  const sourceLabel =
    liveRun.source === "sse"
      ? "SSE"
      : liveRun.source === "snapshot"
        ? "SNAPSHOT"
        : liveRun.source.toUpperCase();
  const transportLabel =
    status === "live"
      ? "LIVE"
      : status === "reconnecting"
        ? "RECONNECT"
        : status === "connecting"
          ? "OPEN"
          : "OFFLINE";
  return `${sourceLabel} · ${transportLabel} · #${lastLiveAppendId || lastAppendId || 0}`;
}

export function toggleSessionRail(dom, currentState) {
  const rail = currentState.sessionRail || {};
  currentState.sessionRail = {
    conversationId: rail.conversationId || currentState.currentConversationId || "",
    expanded: !Boolean(rail.expanded),
  };
  renderSessionStrip(dom, currentState, currentState.conversationCache);
}

export function renderSessionStrip(dom, currentState, conversation) {
  if (!dom.sessionStrip || !dom.sessionStripState || !dom.sessionStripMeta || !dom.sessionStripDetail || !dom.threadScroller) {
    return;
  }

  const threadTransition = currentState.threadTransition || {};
  const conversationId = conversation?.conversation_id || "";
  const appendStream = currentState.appendStream || {};
  const status = String(appendStream.status || "offline").toLowerCase();
  const attachMode = String(appendStream.attachMode || "idle").toLowerCase();
  const bootstrapVersion = String(appendStream.bootstrapVersion || "");
  const resumeMode = String(appendStream.resumeMode || "idle").toLowerCase();
  const resumeCursor = Math.max(Number(appendStream.resumeCursor || 0), 0);
  const sessionPhase = selectedThreadSessionPhase(conversation, currentState);
  const lastAppendId = Number(appendStream.lastAppendId || maxConversationAppendId(conversation) || 0);
  const lastRenderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const lastLiveAppendId = Number(appendStream.lastLiveAppendId || 0);
  const liveRun = deriveLiveRunState(conversation, currentState);
  const handoffState = conversation ? pendingHandoffState(conversation, currentState) : { stage: "idle" };
  const inlineState = selectedThreadInlineSessionState(conversation, currentState, liveRun, handoffState);
  const ownerState = composerOwnerState(currentState, conversation);
  const transportState = composerTransportState(currentState, conversation, liveRun, handoffState);
  const sessionIndicator = selectedThreadLiveSessionIndicator(currentState, conversation, liveRun, handoffState);
  const proposalState = proposalChip(liveRun);
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const footerFollow = selectedThreadFooterFollowState(dom, currentState, conversationId, lastRenderSource);
  const footerDock = selectedThreadFooterDockModel(currentState, conversation, liveRun, footerFollow);
  currentState.sessionRail ||= { conversationId: "", expanded: false };

  if (!conversationId && !(threadTransition.active && threadTransition.targetConversationId) && !sessionStatus.conversationId) {
    dom.sessionStrip.hidden = true;
    dom.sessionStrip.dataset.sessionPresentation = "cleared";
    dom.sessionStrip.dataset.sessionTerminal = "false";
    dom.sessionStrip.dataset.streamState = "offline";
    dom.sessionStrip.dataset.attachMode = "idle";
    dom.sessionStrip.dataset.bootstrapVersion = "";
    dom.sessionStrip.dataset.resumeMode = "idle";
    dom.sessionStrip.dataset.resumeCursor = "0";
    dom.sessionStrip.dataset.phaseValue = "UNKNOWN";
    dom.sessionStrip.dataset.phaseAuthoritative = "false";
    dom.sessionStrip.dataset.phaseProvenance = "none";
    dom.sessionStrip.dataset.renderSource = "snapshot";
    dom.sessionStrip.dataset.liveConversationId = "";
    dom.sessionStrip.dataset.lastAppendId = "0";
    dom.sessionStrip.dataset.lastLiveAppendId = "0";
    dom.sessionStrip.dataset.liveRunState = "done";
    dom.sessionStrip.dataset.liveRunPhase = "IDLE";
    dom.sessionStrip.dataset.liveRunSource = "none";
    dom.sessionStrip.dataset.liveRunJob = "";
    dom.sessionStrip.dataset.liveRunTone = "idle";
    dom.sessionStrip.dataset.followState = "idle";
    dom.sessionStrip.dataset.sessionOwner = "none";
    dom.sessionStrip.dataset.composerState = "idle";
    dom.sessionStrip.dataset.composerTransport = "none";
    dom.sessionStrip.dataset.composerTransportSource = "none";
    dom.sessionStrip.dataset.composerTransportOwned = "false";
    dom.sessionStrip.dataset.composerTransportReason = "idle";
    dom.sessionStrip.dataset.composerTargetConversationId = "";
    dom.sessionStrip.dataset.sessionCollapsed = "false";
    dom.threadScroller.dataset.streamState = "offline";
    dom.threadScroller.dataset.attachMode = "idle";
    dom.threadScroller.dataset.bootstrapVersion = "";
    dom.threadScroller.dataset.resumeMode = "idle";
    dom.threadScroller.dataset.resumeCursor = "0";
    dom.threadScroller.dataset.phaseValue = "UNKNOWN";
    dom.threadScroller.dataset.phaseAuthoritative = "false";
    dom.threadScroller.dataset.phaseProvenance = "none";
    dom.threadScroller.dataset.renderSource = "snapshot";
    dom.threadScroller.dataset.liveConversationId = "";
    dom.threadScroller.dataset.lastAppendId = "0";
    dom.threadScroller.dataset.lastLiveAppendId = "0";
    dom.threadScroller.dataset.sessionOwner = "none";
    dom.threadScroller.dataset.sessionPresentation = "cleared";
    dom.threadScroller.dataset.sessionTerminal = "false";
    dom.threadScroller.dataset.liveRunState = "done";
    dom.threadScroller.dataset.liveRunPhase = "IDLE";
    dom.threadScroller.dataset.liveRunSource = "none";
    dom.threadScroller.dataset.liveRunJob = "";
    currentState.sessionRail = {
      conversationId: "",
      expanded: false,
    };
    if (dom.sessionStripToggle) {
      dom.sessionStripToggle.hidden = true;
      dom.sessionStripToggle.textContent = "세부 보기";
      dom.sessionStripToggle.dataset.sessionAction = "toggle-session-rail";
      dom.sessionStripToggle.dataset.followState = "idle";
      dom.sessionStripToggle.dataset.followCount = "0";
    }
    return;
  }

  const sessionConversationId =
    conversationId || String(threadTransition.targetConversationId || sessionStatus.conversationId || "");
  if (currentState.sessionRail.conversationId !== sessionConversationId) {
    currentState.sessionRail = {
      conversationId: sessionConversationId,
      expanded: false,
    };
  }

  const presentation =
    ownerState.state === "switching"
      ? "switching"
      : status === "reconnecting"
      ? "reconnecting"
      : status === "connecting"
        ? "connecting"
        : sessionStatus.presentation === "restore"
          ? "restore"
        : liveRun.state === "sending"
          ? "sending"
        : liveRun.state === "generating"
          ? "sending"
        : status === "live" && !liveRun.terminal && liveRun.tone !== "idle"
          ? "live"
          : liveRun.terminal
            ? "terminal"
            : "idle";
  const canCollapse = false;
  const shouldCollapse = false;
  const collapsedSummary = null;
  const phaseDatasetValue = ownerState.state === "switching" ? "UNKNOWN" : liveRun.phase || sessionPhase.value;
  const phaseDatasetAuthoritative = ownerState.state === "switching" ? "false" : liveRun.phase && sessionPhase.authoritative ? "true" : "false";
  const phaseDatasetProvenance =
    ownerState.state === "switching" ? "thread-transition" : liveRun.source || sessionPhase.source;
  const liveOwned =
    transportState.owned &&
    inlineState.selectedThreadSseOwned &&
    inlineState.status === "live" &&
    inlineState.renderSource === "sse";
  const stripLiveOwned = Boolean(footerDock.visible);
  const stripState = sessionStripStateRow(ownerState, transportState, liveRun, presentation, liveOwned, footerFollow, footerDock);
  dom.sessionStrip.hidden = !sessionConversationId ? true : false;
  dom.sessionStrip.dataset.liveOwned = stripLiveOwned ? "true" : "false";
  dom.sessionStrip.dataset.sessionOwner = stripLiveOwned ? "selected-thread" : "none";
  dom.sessionStrip.dataset.sessionPresentation = presentation;
  dom.sessionStrip.dataset.sessionTerminal = liveRun.terminal ? "true" : "false";
  dom.sessionStrip.dataset.sessionCollapsed = shouldCollapse ? "true" : "false";
  dom.sessionStrip.dataset.streamState = status;
  dom.sessionStrip.dataset.attachMode = attachMode;
  dom.sessionStrip.dataset.bootstrapVersion = bootstrapVersion;
  dom.sessionStrip.dataset.resumeMode = resumeMode;
  dom.sessionStrip.dataset.resumeCursor = String(resumeCursor);
  dom.sessionStrip.dataset.phaseValue = phaseDatasetValue;
  dom.sessionStrip.dataset.phaseAuthoritative = phaseDatasetAuthoritative;
  dom.sessionStrip.dataset.phaseProvenance = phaseDatasetProvenance;
  dom.sessionStrip.dataset.renderSource = lastRenderSource;
  dom.sessionStrip.dataset.liveConversationId = conversationId;
  dom.sessionStrip.dataset.lastAppendId = String(lastAppendId || 0);
  dom.sessionStrip.dataset.lastLiveAppendId = String(lastLiveAppendId || 0);
  dom.sessionStrip.dataset.liveRunState = liveRun.state;
  dom.sessionStrip.dataset.liveRunPhase = liveRun.phase;
  dom.sessionStrip.dataset.liveRunSource = liveRun.source;
  dom.sessionStrip.dataset.liveRunJob = liveRun.jobId || "";
  dom.sessionStrip.dataset.liveRunTone = liveRun.tone;
  dom.sessionStrip.dataset.followState = footerFollow.visible ? footerFollow.followState : stripLiveOwned ? sessionStatus.followState || "live" : transportState.owned ? "owned" : "idle";
  dom.sessionStrip.dataset.followCount = String(footerFollow.visible ? footerFollow.unseenCount : 0);
  dom.sessionStrip.dataset.footerDockOwned = stripLiveOwned ? "true" : "false";
  dom.sessionStrip.dataset.footerDockPhase = footerDock.phaseLabel || "IDLE";
  dom.sessionStrip.dataset.footerDockSource = footerDock.source || "none";
  dom.sessionStrip.dataset.footerDockMilestones = footerDock.visible ? "true" : "false";
  dom.sessionStrip.dataset.composerState = ownerState.state;
  dom.sessionStrip.dataset.composerTransport = transportState.key;
  dom.sessionStrip.dataset.composerTransportSource = transportState.source;
  dom.sessionStrip.dataset.composerTransportOwned = stripLiveOwned ? "true" : "false";
  dom.sessionStrip.dataset.composerTransportReason = transportState.reason;
  dom.sessionStrip.dataset.composerTargetConversationId = ownerState.conversationId;
  dom.sessionStrip.dataset.restoreStage = sessionStatus.restoreStage || "none";
  dom.sessionStrip.dataset.restorePath = sessionStatus.restorePath || "none";
  dom.sessionStrip.dataset.restoreProvenance = sessionStatus.restoreProvenance || "none";
  dom.sessionStripState.dataset.sessionStripRole = stripState.role;
  dom.sessionStripState.dataset.sessionStripLabel = stripState.label;
  dom.sessionStripState.dataset.sessionStripTone = stripState.tone;

  dom.sessionStripState.innerHTML = sessionStripStateChipMarkup(stripState.chips || stripState);
  dom.sessionStripMeta.textContent = ownerState.target;
  dom.sessionStripDetail.textContent = footerDock.visible
    ? footerDock.detail
    : sessionStripDetailCopy(
        ownerState,
        transportState,
        sessionIndicator,
        liveRun,
        proposalState,
        liveOwned,
        footerFollow,
      );
  if (dom.sessionStripToggle) {
    dom.sessionStripToggle.hidden = !footerFollow.visible;
    dom.sessionStripToggle.textContent = footerFollow.visible ? (footerFollow.followState === "new" ? "최신으로" : "재개") : "세부 보기";
    dom.sessionStripToggle.dataset.sessionAction = footerFollow.visible ? "jump-latest" : "toggle-session-rail";
    dom.sessionStripToggle.dataset.followState = footerFollow.visible ? footerFollow.followState : "idle";
    dom.sessionStripToggle.dataset.followCount = String(footerFollow.visible ? footerFollow.unseenCount : 0);
  }
  if (dom.draftStatus) {
    dom.draftStatus.hidden = true;
  }
  if (dom.sendRequestButton) {
    dom.sendRequestButton.textContent = status === "live" || presentation === "sending" ? "추가 지시 보내기" : "메시지 보내기";
  }
  if (dom.applyProposalButton) {
    dom.applyProposalButton.textContent = liveRun.state === "proposal-ready" ? "지금 제안 적용" : "제안 적용";
  }

  dom.threadScroller.dataset.streamState = status;
  dom.threadScroller.dataset.attachMode = attachMode;
  dom.threadScroller.dataset.bootstrapVersion = bootstrapVersion;
  dom.threadScroller.dataset.resumeMode = resumeMode;
  dom.threadScroller.dataset.resumeCursor = String(resumeCursor);
  dom.threadScroller.dataset.phaseValue = phaseDatasetValue;
  dom.threadScroller.dataset.phaseAuthoritative = phaseDatasetAuthoritative;
  dom.threadScroller.dataset.phaseProvenance = phaseDatasetProvenance;
  dom.threadScroller.dataset.renderSource = lastRenderSource;
  dom.threadScroller.dataset.liveConversationId = conversationId;
  dom.threadScroller.dataset.lastAppendId = String(lastAppendId || 0);
  dom.threadScroller.dataset.lastLiveAppendId = String(lastLiveAppendId || 0);
  dom.threadScroller.dataset.sessionOwner = liveOwned ? "selected-thread" : "none";
  dom.threadScroller.dataset.sessionPresentation = presentation;
  dom.threadScroller.dataset.sessionTerminal = liveRun.terminal ? "true" : "false";
  dom.threadScroller.dataset.liveRunState = liveRun.state;
  dom.threadScroller.dataset.liveRunPhase = liveRun.phase;
  dom.threadScroller.dataset.liveRunSource = liveRun.source;
  dom.threadScroller.dataset.liveRunJob = liveRun.jobId || "";
  dom.threadScroller.dataset.sessionCollapsed = shouldCollapse ? "true" : "false";
  dom.threadScroller.dataset.restoreStage = sessionStatus.restoreStage || "none";
  dom.threadScroller.dataset.restorePath = sessionStatus.restorePath || "none";
  dom.threadScroller.dataset.restoreProvenance = sessionStatus.restoreProvenance || "none";
}

export function renderComposerMeta(dom, { hint = "", count = 0 }) {
  if (hint) {
    dom.composerHint.textContent = hint;
  }
  dom.composerCount.textContent = `${count}자`;
}

function latestIteration(goal) {
  const iterations = Array.isArray(goal?.iterations) ? goal.iterations : [];
  return iterations.length ? iterations[iterations.length - 1] : null;
}

function summarizeVerifierAcceptability(iteration) {
  const reviews = Array.isArray(iteration?.verification_reviews) ? iteration.verification_reviews : [];
  if (!reviews.length) {
    return "PENDING";
  }
  if (reviews.some((review) => String(review?.path_acceptability || "").toLowerCase() === "disqualifying")) {
    return "DISQUALIFYING";
  }
  if (reviews.some((review) => String(review?.path_acceptability || "").toLowerCase() === "acceptable")) {
    return "ACCEPTABLE";
  }
  return "PENDING";
}

function blockerTone(blockerReason = "") {
  if (!blockerReason || blockerReason === "none") {
    return "healthy";
  }
  if (blockerReason === "goal_review_stop") {
    return "neutral";
  }
  return "blocked";
}

export function clearAutonomySummary(dom, message = "자율 goal이 생기면 continuation blocker와 verifier 판단이 여기에 요약됩니다.") {
  const autonomyCard = dom.autonomyDetail?.closest(".autonomy-detail-card");
  if (autonomyCard) {
    autonomyCard.hidden = false;
    autonomyCard.dataset.autonomySurface = "secondary-detail";
  }
  if (dom.autonomyDetailMeta) {
    dom.autonomyDetailMeta.textContent = "표시할 자율 goal이 없습니다.";
  }
  if (dom.autonomyDetail) {
    dom.autonomyDetail.dataset.surface = "secondary-detail";
    dom.autonomyDetail.dataset.empty = "true";
    dom.autonomyDetail.dataset.blockerReason = "none";
    dom.autonomyDetail.dataset.pathVerdict = "unknown";
    dom.autonomyDetail.dataset.verifierAcceptability = "pending";
    dom.autonomyDetail.innerHTML = `<p class="autonomy-empty">${escapeHtml(message)}</p>`;
  }
}

function setAutonomyDataset(target, { blockerReason, pathVerdict, verifierAcceptability, source = "none", freshnessState = "stale-or-missing", fallbackAllowed = true, generatedAt = "" }) {
  if (!target) {
    return;
  }
  target.dataset.empty = "false";
  target.dataset.blockerReason = blockerReason;
  target.dataset.pathVerdict = pathVerdict.toLowerCase();
  target.dataset.verifierAcceptability = verifierAcceptability.toLowerCase();
  target.dataset.autonomySource = String(source || "none").toLowerCase();
  target.dataset.autonomyFreshnessState = String(freshnessState || "stale-or-missing").toLowerCase();
  target.dataset.autonomyFallbackAllowed = fallbackAllowed ? "true" : "false";
  target.dataset.autonomyGeneratedAt = String(generatedAt || "");
}

export function renderAutonomySummary(dom, goal) {
  const summary = buildAutonomySummary(goal);
  if (!summary) {
    clearAutonomySummary(dom);
    return;
  }
  const blockerClass = blockerTone(summary.blockerReason);
  const autonomyCard = dom.autonomyDetail?.closest(".autonomy-detail-card");
  if (autonomyCard) {
    autonomyCard.hidden = false;
    autonomyCard.dataset.autonomySurface = "secondary-detail";
  }

  if (dom.autonomyDetailMeta) {
    dom.autonomyDetailMeta.textContent = summary.heading;
  }
  if (dom.autonomyDetail) {
    dom.autonomyDetail.dataset.surface = "secondary-detail";
    setAutonomyDataset(dom.autonomyDetail, {
      blockerReason: summary.blockerReason,
      pathVerdict: summary.pathVerdict,
      verifierAcceptability: summary.verifierAcceptability,
      source: summary.source,
      freshnessState: summary.freshnessState,
      fallbackAllowed: summary.fallbackAllowed,
      generatedAt: summary.generatedAt,
    });
    dom.autonomyDetail.innerHTML = `
      <div class="autonomy-chip-row autonomy-chip-row-compact">
        <span class="autonomy-chip ${autonomyChipTone(summary.pathVerdict)}">${summary.pathVerdict}</span>
        <span class="autonomy-chip ${autonomyChipTone(summary.verifierAcceptability)}">${summary.verifierAcceptability}</span>
        <span class="autonomy-chip ${blockerClass}">BLOCKER ${escapeHtml(summary.blockerReason.toUpperCase())}</span>
      </div>
      <div class="autonomy-inline-meta">
        <p class="autonomy-inline-item"><span>Iteration</span>${escapeHtml(String(summary.iteration))}</p>
        <p class="autonomy-inline-item"><span>Path</span>${escapeHtml(summary.expectedPath)}</p>
        <p class="autonomy-inline-item"><span>Signals</span>${escapeHtml(summary.degradedSignals.length ? summary.degradedSignals.join(", ") : "none")}</p>
      </div>
    `;
  }
}

function syncAutonomyDetailSurface(dom, currentState, conversation, liveRun, handoffState = { stage: "idle" }) {
  const autonomyCard = dom.autonomyDetail?.closest(".autonomy-detail-card");
  if (!autonomyCard || !dom.autonomyDetail) {
    return;
  }
  const liveAutonomy = conversation ? deriveSelectedThreadLiveAutonomy(currentState, conversation) : { visible: false };
  const hideForSelectedThreadLiveAutonomy = Boolean(liveAutonomy.owned);
  autonomyCard.hidden = hideForSelectedThreadLiveAutonomy;
  autonomyCard.dataset.autonomySurface = hideForSelectedThreadLiveAutonomy ? "center-lane" : "secondary-detail";
  dom.autonomyDetail.dataset.surface = hideForSelectedThreadLiveAutonomy ? "center-lane" : "secondary-detail";
}

function phaseLabel(status, eventType = "") {
  const normalizedStatus = String(status || "").toLowerCase();
  if (eventType.startsWith("proposal.")) {
    return "PROPOSAL";
  }
  if (eventType.startsWith("runtime.") || normalizedStatus === "planning") {
    return "PLANNING";
  }
  if (eventType.startsWith("codex.") || normalizedStatus === "running") {
    return "RUNNING";
  }
  if (normalizedStatus === "queued") {
    return "QUEUED";
  }
  if (normalizedStatus === "completed" || normalizedStatus === "applied") {
    return "DONE";
  }
  if (normalizedStatus === "failed") {
    return "FAILED";
  }
  return "IDLE";
}

function syncExecutionStatusSurface(dom, currentState, conversation, liveRun, selectedThreadSseOwned) {
  const statusCard = dom.statusOutput?.closest(".inspector-card");
  if (!statusCard || !dom.statusOutput || !dom.jobEvents || !dom.jobPhase || !dom.jobMeta) {
    return;
  }
  const promoteToCenterLane =
    Boolean(currentState) &&
    Boolean(conversation?.conversation_id) &&
    selectedThreadSseOwned &&
    liveRun?.visible &&
    !liveRun?.terminal &&
    Boolean(liveRun?.phase) &&
    liveRun.phase !== "IDLE";
  statusCard.hidden = promoteToCenterLane;
  statusCard.dataset.executionSurface = promoteToCenterLane ? "center-lane" : "secondary-detail";
  dom.statusOutput.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";
  dom.jobEvents.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";
  dom.jobPhase.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";
  dom.jobMeta.dataset.surface = promoteToCenterLane ? "center-lane" : "secondary-detail";
}

export function renderJobActivity(dom, conversation, currentJobId, jobPayload = null, currentState = null) {
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  const appendStream = currentState?.appendStream || {};
  const conversationId = String(conversation?.conversation_id || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const selectedThreadSseOwned =
    Boolean(currentState) &&
    Boolean(conversationId) &&
    String(currentState.currentConversationId || "") === conversationId &&
    streamConversationId === conversationId &&
    String(appendStream.transport || "polling").toLowerCase() === "sse" &&
    String(appendStream.lastRenderSource || "snapshot").toLowerCase() === "sse" &&
    String(appendStream.status || "offline").toLowerCase() === "live";
  const liveRun = currentState ? deriveLiveRunState(conversation, currentState) : runStateSnapshot({ visible: false, phase: "IDLE", source: "none" });
  syncExecutionStatusSurface(dom, currentState, conversation, liveRun, selectedThreadSseOwned);
  const eventJobId = currentState
    ? String(sessionAuthorityJobId(conversation, currentState) || currentJobId || conversation?.latest_job_id || "")
    : String(liveRun.jobId || currentJobId || conversation?.latest_job_id || "");
  const relevantEvents = (selectedThreadSseOwned ? eventJobId : currentJobId)
    ? events.filter((event) => !event.job_id || event.job_id === (selectedThreadSseOwned ? eventJobId : currentJobId))
    : events;
  const recentEvents = relevantEvents.slice(-4).reverse();

  const latestEvent = recentEvents[0];
  const phase = selectedThreadSseOwned
    ? String(liveRun.phase || "IDLE").toUpperCase()
    : phaseLabel(jobPayload?.status || latestEvent?.status || "", latestEvent?.type || "");
  dom.jobPhase.textContent = phase;
  dom.jobPhase.className = `activity-phase ${phase.toLowerCase()}`;

  if (currentState && dom.applyProposalButton && selectedThreadSseOwned) {
    currentState.latestProposalJobId =
      liveRun.state === "proposal-ready"
        ? String(liveRun.jobId || conversation?.latest_job_id || "")
        : "";
    updateProposalButton(dom, currentState.latestProposalJobId);
  }

  if (!recentEvents.length) {
    dom.jobEvents.innerHTML = '<p class="activity-empty">작업이 시작되면 최근 실행 이벤트가 여기에 표시됩니다.</p>';
    return;
  }

  dom.jobEvents.innerHTML = recentEvents
    .map(
      (event) => `
        <article class="activity-event ${event.status || "info"}">
          <p class="activity-event-kind">${event.type}</p>
          <p class="activity-event-body">${event.body}</p>
          <p class="activity-event-meta">${event.created_at}</p>
        </article>
      `,
    )
    .join("");
}

export function updateSelectedAppCard(dom, app) {
  const hasDeployment = Boolean(app && app.deploymentUrl);
  dom.openAppButton.disabled = !hasDeployment;

  if (!app) {
    dom.selectedAppUrl.textContent = "앱을 선택하면 여기에서 바로 열 수 있습니다.";
    if (dom.selectedAppSummary) {
      dom.selectedAppSummary.textContent = "앱을 고르면 현재 레인이 여기에 고정됩니다.";
    }
    updateHeroState(dom, {
      threadTitle: "앱을 먼저 고르세요",
      threadKicker: "작업 공간",
      conversationState: "대화 준비 전",
      liveRun: runStateSnapshot({ visible: false, phase: "IDLE", source: "none" }),
    });
    renderWorkspaceSummary(dom, "앱을 고르면 현재 작업 라인, 최근 대화, 배포 진입점이 여기에 요약됩니다.");
    return;
  }

  dom.selectedAppUrl.textContent = hasDeployment
    ? app.deploymentUrl
    : "deployment_url이 아직 등록되지 않았습니다.";
  if (dom.selectedAppSummary) {
    dom.selectedAppSummary.textContent = hasDeployment
      ? `${app.title} · 배포 링크 사용 가능`
      : `${app.title} · 배포 링크 없음`;
  }
}

export function updateProposalButton(dom, latestProposalJobId) {
  dom.applyProposalButton.disabled = !latestProposalJobId;
}

export function describeJob(payload) {
  const lines = [
    `job_id: ${payload.job_id}`,
    `status: ${payload.status}`,
    `created_at: ${payload.created_at}`,
    payload.started_at ? `started_at: ${payload.started_at}` : "",
    payload.completed_at ? `completed_at: ${payload.completed_at}` : "",
    payload.error ? `error: ${payload.error}` : "",
    payload.proposal ? `proposal_branch: ${payload.proposal.branch_name}` : "",
    payload.proposal ? `proposal_status: ${payload.proposal.status}` : "",
    payload.result_summary ? `\n${simplifyText(payload.result_summary)}` : "",
  ].filter(Boolean);
  return lines.join("\n");
}

export function clearLearningSummary(dom, message = "작업이 끝나면 여기에서 설계 판단과 검증 내용을 바로 읽을 수 있습니다.") {
  dom.learningMeta.textContent = "아직 기록된 학습 로그가 없습니다.";
  dom.learningSummary.innerHTML = `<p class="learning-empty">${message}</p>`;
}

export function renderLearningSummary(dom, summary, heading, status = "RECORDED") {
  const renderCards = (fields, payload) => {
    const cards = [];
    if (!payload) {
      return cards;
    }
    for (const [key, label] of fields) {
      const value = typeof payload[key] === "string" ? payload[key].trim() : "";
      if (!value) {
        continue;
      }
      cards.push(`
        <article class="learning-card">
          <p class="learning-label">${label}</p>
          <p class="learning-value">${escapeHtml(simplifyText(value))}</p>
        </article>
      `);
    }
    return cards;
  };

  const decisionCards = renderCards(DECISION_FIELDS, summary);

  if (!decisionCards.length) {
    clearLearningSummary(dom, "이번 작업에는 아직 구조화된 학습 로그가 없습니다.");
    return;
  }

  dom.learningMeta.textContent = `${status} · ${heading}`;
  dom.learningSummary.innerHTML = `<section class="learning-group"><p class="learning-group-head">설계 판단</p>${decisionCards.join("")}</section>`;
}

export function renderConversation(dom, currentState, conversation, onPersist) {
  const previousFollow = currentState.liveFollow || {};
  const previousConversationId = previousFollow.conversationId || "";
  const wasNearBottom = isThreadNearBottom(dom.threadScroller);
  const threadTransition = currentState.threadTransition || {};
  currentState.conversationCache = conversation;
  const appendStream = currentState.appendStream || {};
  currentState.currentConversationId = conversation
    ? conversation.conversation_id
    : String(currentState.currentConversationId || currentState.savedConversationId || appendStream.conversationId || "");
  if (conversation) {
    currentState.appendStream ||= {};
    currentState.appendStream.lastAppendId = Math.max(
      Number(currentState.appendStream.lastAppendId || 0),
      maxConversationAppendId(conversation),
    );
  }
  onPersist();

  if (!conversation) {
    const workspacePlaceholder = selectedThreadWorkspacePlaceholder(currentState);
    const isThreadTransition = workspacePlaceholder.mode === "switching";
    const isSavedRestore = workspacePlaceholder.mode === "restore";
    dom.conversationTimeline.dataset.workspacePlaceholder = workspacePlaceholder.mode;
    dom.conversationTimeline.dataset.workspaceConversationId = workspacePlaceholder.conversationId;
    dom.conversationTimeline.innerHTML = workspacePlaceholder.timeline;
    if (dom.threadScroller) {
      dom.threadScroller.dataset.workspacePlaceholder = workspacePlaceholder.mode;
      dom.threadScroller.dataset.workspacePlaceholderConversationId = workspacePlaceholder.conversationId;
      dom.threadScroller.dataset.pendingConversationId = isThreadTransition
        ? workspacePlaceholder.conversationId
        : isSavedRestore
          ? workspacePlaceholder.conversationId
          : "";
      dom.threadScroller.dataset.pendingHandoffStage = "idle";
      dom.threadScroller.dataset.pendingUserCount = "0";
      dom.threadScroller.dataset.pendingAssistantCount = "0";
      dom.threadScroller.dataset.threadTransitionState = isThreadTransition ? "switching" : "idle";
      dom.threadScroller.dataset.threadTransitionConversationId = isThreadTransition
        ? workspacePlaceholder.conversationId
        : "";
    }
    renderSessionStrip(dom, currentState, null);
    currentState.liveFollow = {
      conversationId: isThreadTransition
        ? workspacePlaceholder.conversationId
        : isSavedRestore
          ? workspacePlaceholder.conversationId
          : "",
      isFollowing: true,
      jumpVisible: false,
      lastAppendId: 0,
      lastSeenAppendId: 0,
      pendingAppendCount: 0,
    };
    syncJumpToLatest(dom, currentState, currentState.liveFollow.conversationId, "snapshot");
    updateHeroState(dom, {
      threadTitle: workspacePlaceholder.title,
      threadKicker: "선택된 대화",
      conversationState: workspacePlaceholder.conversationState,
      liveRun: workspacePlaceholder.liveRun,
    });
    renderWorkspaceSummary(dom, workspacePlaceholder.workspaceSummary);
    renderSessionSummary(
      dom,
      currentState,
      null,
      runStateSnapshot({
        visible: false,
        phase: "IDLE",
        source: "none",
        tone: "idle",
      }),
      { stage: "idle" },
    );
    syncAutonomyDetailSurface(
      dom,
      currentState,
      null,
      runStateSnapshot({
        visible: false,
        phase: "IDLE",
        source: "none",
        tone: "idle",
      }),
      { stage: "idle" },
    );
    syncComposerOwnership(dom, currentState, null);
    renderJobActivity(dom, null, "", null, currentState);
    return;
  }

  dom.conversationTimeline.dataset.workspacePlaceholder = "conversation";
  dom.conversationTimeline.dataset.workspaceConversationId = String(conversation.conversation_id || "");

  const messages = Array.isArray(conversation.messages) ? conversation.messages : [];
  const events = Array.isArray(conversation.events) ? conversation.events : [];
  const handoffState = pendingHandoffState(conversation, currentState);
  const items = [
    ...messages.map((item) => ({ ...item, kind: "message", sortAt: item.created_at })),
    ...events.map((item) => ({ ...item, kind: "event", sortAt: item.created_at })),
    ...handoffState.items,
  ].sort((a, b) => {
    const leftAppendId = Number(a.append_id || 0);
    const rightAppendId = Number(b.append_id || 0);
    if (leftAppendId && rightAppendId && leftAppendId !== rightAppendId) {
      return leftAppendId - rightAppendId;
    }
    return a.sortAt < b.sortAt ? -1 : 1;
  });

  const liveRun = deriveLiveRunState(conversation, currentState);
  const inlineSessionBlock = renderInlineSessionBlock(conversation, currentState, liveRun, handoffState);
  const transcriptLiveActivity = renderTranscriptLiveActivity(conversation, currentState, liveRun);
  if (dom.threadScroller) {
    dom.threadScroller.dataset.workspacePlaceholder = "conversation";
    dom.threadScroller.dataset.workspacePlaceholderConversationId = String(conversation.conversation_id || "");
    dom.threadScroller.dataset.pendingConversationId = "";
    dom.threadScroller.dataset.pendingHandoffStage = handoffState.stage;
    dom.threadScroller.dataset.pendingUserCount = String(handoffState.pendingUserCount);
    dom.threadScroller.dataset.pendingAssistantCount = String(handoffState.pendingAssistantCount);
    dom.threadScroller.dataset.threadTransitionState = "idle";
    dom.threadScroller.dataset.threadTransitionConversationId = "";
  }
  renderSessionStrip(dom, currentState, conversation);
  const latestAppendId = maxConversationAppendId(conversation);
  const isSameConversation = previousConversationId === conversation.conversation_id;
  const renderSource = String(currentState.appendStream?.lastRenderSource || "snapshot").toLowerCase();
  const sessionTerminal = String(dom.threadScroller?.dataset.sessionTerminal || "false") === "true";
  const shouldKeepFollowing = !isSameConversation || previousFollow.isFollowing || wasNearBottom;
  const previousSeenAppendId = Number(previousFollow.lastSeenAppendId || 0);
  const shouldShowJump = isSameConversation
    ? !sessionTerminal && !shouldKeepFollowing && latestAppendId > previousSeenAppendId
    : false;
  currentState.liveFollow = {
    conversationId: conversation.conversation_id,
    isFollowing: shouldKeepFollowing,
    jumpVisible: shouldShowJump,
    lastAppendId: latestAppendId,
    lastSeenAppendId: shouldKeepFollowing ? latestAppendId : previousSeenAppendId,
    pendingAppendCount: shouldShowJump ? Math.max(latestAppendId - previousSeenAppendId, 0) : 0,
  };
  updateHeroState(dom, {
    threadTitle: conversation.title || "제목 없는 대화",
    threadKicker: "선택된 대화",
    conversationState: threadMetaSummary(conversation, liveRun, messages.length, events.length),
    liveRun,
  });
  renderSessionSummary(dom, currentState, conversation, liveRun, handoffState);
  syncAutonomyDetailSurface(dom, currentState, conversation, liveRun, handoffState);
  syncComposerOwnership(dom, currentState, conversation);
  renderWorkspaceSummary(
    dom,
    [
      conversation.latest_job_id ? `job ${conversation.latest_job_id}` : "job 없음",
      messages.length ? `메시지 ${messages.length}` : "메시지 0",
      events.length ? `이벤트 ${events.length}` : "이벤트 0",
    ].join(" · "),
  );

  if (!items.length && !inlineSessionBlock && !transcriptLiveActivity) {
    dom.conversationTimeline.innerHTML = '<p class="timeline-empty">아직 메시지가 없습니다.</p>';
    return;
  }

  const renderedItems = items
    .map((item) => {
      if (item.kind === "event") {
        if (shouldCollapseHealthySessionEvent(item, currentState, conversation, liveRun)) {
          return "";
        }
        const sessionEvent = renderSessionTimelineEvent(item);
        if (sessionEvent) {
          return sessionEvent;
        }
        return `
            <article class="timeline-item event ${item.status || "info"}" data-append-id="${Number(item.append_id || 0)}" data-append-source="${escapeHtml(String(item.delivery_source || "snapshot"))}">
            <p class="timeline-kind">${escapeHtml(eventLabel(item.type))}</p>
            <p class="timeline-body">${escapeHtml(simplifyText(item.body))}</p>
            <p class="timeline-meta">${item.created_at}${item.job_id ? ` · ${item.job_id}` : ""}${item.delivery_source === "sse" ? ' · <span class="timeline-provenance">SSE LIVE</span>' : ""}</p>
          </article>
        `;
      }

      return `
        <article class="timeline-item message ${item.role || "assistant"}${item.pending_local ? " pending-local" : ""}${item.pending_assistant ? " pending-assistant" : ""}" data-append-id="${Number(item.append_id || 0)}" data-append-source="${escapeHtml(String(item.delivery_source || "snapshot"))}"${item.pending_local ? ' data-pending-local="true"' : ""}${item.pending_assistant ? ' data-pending-assistant="true"' : ""}>
          <p class="timeline-kind">${item.role === "user" ? "사용자" : "에이전트"}</p>
          <p class="timeline-body">${escapeHtml(simplifyText(item.body))}</p>
          <p class="timeline-meta">${item.created_at}${item.job_id ? ` · ${item.job_id}` : ""}${item.pending_local ? ' · <span class="timeline-provenance">SENDING</span>' : item.pending_assistant ? ' · <span class="timeline-provenance">GENERATING</span>' : item.delivery_source === "sse" ? ' · <span class="timeline-provenance">SSE LIVE</span>' : ""}</p>
        </article>
      `;
    })
    .join("");
  dom.conversationTimeline.innerHTML = renderedItems + transcriptLiveActivity + inlineSessionBlock;
  if (dom.threadScroller && currentState.liveFollow.isFollowing) {
    dom.threadScroller.scrollTop = dom.threadScroller.scrollHeight;
  }
  syncJumpToLatest(dom, currentState, conversation.conversation_id, renderSource);

  renderJobActivity(dom, conversation, currentState.currentJobId || conversation.latest_job_id || "", null, currentState);

  const assistantResult = [...messages].reverse().find((item) => item.role === "assistant");
  const decisionSummary = assistantResult && assistantResult.metadata ? assistantResult.metadata.decision_summary : null;
  if (decisionSummary) {
    renderLearningSummary(
      dom,
      decisionSummary,
      assistantResult.title || "이번 작업에서 배운 점",
      assistantResult.metadata?.status || "RECORDED",
    );
  }
}
