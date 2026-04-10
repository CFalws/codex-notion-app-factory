import { DECISION_FIELDS } from "./ops-constants.js";
import { maxConversationAppendId } from "./ops-store.js";

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
  }
}

export function renderWorkspaceSummary(dom, summary) {
  dom.workspaceSummaryText.textContent = summary;
}

export function renderDraftStatus(dom, message) {
  dom.draftStatus.textContent = message;
}

function composerOwnerState(currentState, conversation) {
  const threadTransition = currentState.threadTransition || {};
  const pendingOutgoing = currentState.pendingOutgoing || {};
  const conversationId = String(conversation?.conversation_id || "");
  const conversationTitle = String(conversation?.title || "현재 대화").trim() || "현재 대화";

  if (threadTransition.active && threadTransition.targetConversationId) {
    return {
      state: "switching",
      label: "SWITCHING",
      tone: "warning",
      conversationId: String(threadTransition.targetConversationId || ""),
      target: String(threadTransition.targetTitle || "선택한 대화").trim() || "선택한 대화",
      copy: "새 selected-thread snapshot을 붙이는 중이라 이전 thread로는 보낼 수 없습니다.",
      blocked: true,
      blockedReason: "selected-thread attach가 끝날 때까지 잠시 기다려 주세요.",
    };
  }

  if (
    conversationId &&
    pendingOutgoing.conversationId === conversationId &&
    (pendingOutgoing.status === "sending-user" || pendingOutgoing.status === "awaiting-assistant")
  ) {
    return {
      state: "handoff",
      label: "HANDOFF",
      tone: "neutral",
      conversationId,
      target: conversationTitle,
      copy:
        pendingOutgoing.status === "sending-user"
          ? "현재 메시지를 selected thread에 handoff하는 중입니다."
          : "handoff는 확인되었고 첫 assistant append를 기다리는 중입니다.",
      blocked: false,
      blockedReason: "",
    };
  }

  if (conversationId) {
    return {
      state: "ready",
      label: "READY",
      tone: "healthy",
      conversationId,
      target: conversationTitle,
      copy: "이 입력창은 현재 선택된 thread에 바로 연결됩니다.",
      blocked: false,
      blockedReason: "",
    };
  }

  return {
    state: "idle",
    label: "IDLE",
    tone: "muted",
    conversationId: "",
    target: "대상을 선택하면 이 입력창의 연결 상태가 여기에 표시됩니다.",
    copy: "선택된 대화의 target ownership을 이 줄에서 바로 확인합니다.",
    blocked: false,
    blockedReason: "",
  };
}

function syncComposerOwnership(dom, currentState, conversation) {
  if (!dom.composerOwnerRow || !dom.composerOwnerState || !dom.composerOwnerTarget || !dom.composerOwnerCopy) {
    return;
  }
  const owner = composerOwnerState(currentState, conversation);
  dom.composerOwnerRow.dataset.composerOwner = owner.state;
  dom.composerOwnerRow.dataset.composerOwnerConversationId = owner.conversationId;
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

function renderSessionSummary(dom, currentState, conversation, liveRun, handoffState = { stage: "idle" }) {
  if (
    !dom.sessionSummaryRow ||
    !dom.sessionSummaryScope ||
    !dom.sessionSummaryPath ||
    !dom.sessionSummaryState ||
    !dom.sessionSummaryCopy
  ) {
    return;
  }

  const appendStream = currentState.appendStream || {};
  const threadTransition = currentState.threadTransition || {};
  const conversationId = String(conversation?.conversation_id || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const renderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const transport = String(appendStream.transport || "polling").toLowerCase();
  const status = String(appendStream.status || "offline").toLowerCase();
  const sseLiveOwner =
    conversationId &&
    streamConversationId === conversationId &&
    transport === "sse" &&
    renderSource === "sse";

  let pathLabel = "SNAPSHOT";
  let stateLabel = conversationId ? "READY" : "IDLE";
  let copy = conversationId
    ? `${String(conversation?.title || "현재 대화")} 기준의 session context입니다.`
    : "대화를 선택하면 selected-thread context가 여기에 고정됩니다.";

  if (threadTransition.active && threadTransition.targetConversationId) {
    pathLabel = "SWITCHING";
    stateLabel = "ATTACH";
    copy = `${String(threadTransition.targetTitle || "선택한 대화")} snapshot과 selected-thread path를 붙이는 중입니다.`;
  } else if (handoffState.stage === "pending-user") {
    pathLabel = "HANDOFF";
    stateLabel = "SENDING";
    copy = "이전 메시지 handoff를 확인하는 중이라 composer ownership을 잠시 고정했습니다.";
  } else if (handoffState.stage === "pending-assistant") {
    pathLabel = "HANDOFF";
    stateLabel = "ACCEPTED";
    copy = "첫 assistant append가 붙을 때까지 selected-thread ownership을 유지합니다.";
  } else if (status === "reconnecting") {
    pathLabel = "DEGRADED";
    stateLabel = "RESUME";
    copy = "selected-thread attach는 유지하지만 live transport는 복구 중입니다.";
  } else if (sseLiveOwner) {
    pathLabel = "SSE";
    stateLabel = String(liveRun?.phase || "LIVE").toUpperCase();
    copy = liveRun?.jobId
      ? `selected-thread live path · ${liveRun.jobId}`
      : "selected-thread live path가 현재 중심 workspace를 소유합니다.";
  }

  dom.sessionSummaryRow.dataset.summaryPath = pathLabel.toLowerCase();
  dom.sessionSummaryRow.dataset.summaryState = stateLabel.toLowerCase();
  dom.sessionSummaryScope.textContent = "SELECTED THREAD";
  dom.sessionSummaryPath.textContent = pathLabel;
  dom.sessionSummaryState.textContent = stateLabel;
  dom.sessionSummaryCopy.textContent = copy;
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

function runStateSnapshot({
  visible = true,
  state = "idle",
  phase = "IDLE",
  detail = "",
  source = "none",
  tone = "idle",
  jobId = "",
  terminal = false,
}) {
  return { visible, state, phase, detail, source, tone, jobId, terminal };
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

function shouldShowComposerLiveStrip(appendStream, conversationId, lastRenderSource, liveRun) {
  const streamConversationId = String(appendStream?.conversationId || "");
  const transport = String(appendStream?.transport || "polling").toLowerCase();
  const status = String(appendStream?.status || "offline").toLowerCase();
  const ownsSelectedThread = conversationId && streamConversationId === conversationId && transport === "sse";

  if (
    !ownsSelectedThread ||
    !liveRun?.visible ||
    liveRun.terminal ||
    !liveRun.phase ||
    liveRun.phase === "IDLE"
  ) {
    return false;
  }

  if (status === "live") {
    return lastRenderSource === "sse";
  }

  if (status === "reconnecting" || status === "connecting" || status === "offline") {
    return true;
  }

  return false;
}

function renderInlineSessionBlock(conversation, currentState, liveRun, handoffState) {
  const appendStream = currentState.appendStream || {};
  const conversationId = String(conversation?.conversation_id || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const renderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const transport = String(appendStream.transport || "polling").toLowerCase();
  const status = String(appendStream.status || "offline").toLowerCase();
  const sseLiveOwner =
    conversationId &&
    streamConversationId === conversationId &&
    transport === "sse" &&
    renderSource === "sse";
  const showComposerLiveStrip = shouldShowComposerLiveStrip(appendStream, conversationId, renderSource, liveRun);

  if (showComposerLiveStrip) {
    return "";
  }

  if (handoffState?.stage === "pending-assistant") {
    return `
      <section class="session-inline-block" data-selected-thread-live-block="true" data-live-block-stage="pending-assistant" data-live-block-source="accepted-event">
        <p class="session-inline-kicker">In Flight Assistant</p>
        <div class="session-inline-row">
          <span class="session-inline-chip" data-tone="neutral">ASSISTANT</span>
          <span class="session-inline-chip" data-tone="neutral">ACCEPTED</span>
        </div>
        <p class="session-inline-body">첫 응답을 준비 중입니다. 선택된 대화의 handoff가 이미 확인되었고, 실제 assistant append를 기다리고 있습니다.</p>
        <p class="session-inline-meta">selected thread · ACCEPTED · ${escapeHtml(status.toUpperCase())}</p>
      </section>
    `;
  }

  if (
    !sseLiveOwner ||
    !liveRun?.visible ||
    liveRun.terminal ||
    !liveRun.phase ||
    liveRun.phase === "IDLE" ||
    liveRun.state === "sending" ||
    liveRun.state === "generating"
  ) {
    return "";
  }

  const tone = transcriptLiveTone(liveRun);
  const detail = simplifyText(phaseDetailHint(liveRun) || liveRun.detail || "");
  const appendId = Number(appendStream.lastLiveAppendId || appendStream.lastAppendId || 0);
  return `
    <section class="session-inline-block" data-selected-thread-live-block="true" data-live-block-stage="${escapeHtml(liveRun.state)}" data-live-block-source="sse">
      <p class="session-inline-kicker">Selected Thread Session</p>
      <div class="session-inline-row">
        <span class="session-inline-chip" data-tone="neutral">LIVE</span>
        <span class="session-inline-chip" data-tone="${escapeHtml(tone)}">${escapeHtml(String(liveRun.phase || "LIVE").toUpperCase())}</span>
      </div>
      <p class="session-inline-body">${escapeHtml(detail || "선택된 대화의 최신 live 진행 상태를 표시하는 중입니다.")}</p>
      <p class="session-inline-meta">selected thread · SSE · ${escapeHtml(status.toUpperCase())} · append #${appendId || 0}${liveRun.jobId ? ` · ${escapeHtml(liveRun.jobId)}` : ""}</p>
    </section>
  `;
}

function renderTranscriptLiveActivity(conversation, currentState, liveRun) {
  const appendStream = currentState.appendStream || {};
  const conversationId = String(conversation?.conversation_id || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const renderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const transport = String(appendStream.transport || "polling").toLowerCase();
  const status = String(appendStream.status || "offline").toLowerCase();
  const showComposerLiveStrip = shouldShowComposerLiveStrip(appendStream, conversationId, renderSource, liveRun);
  if (showComposerLiveStrip || (liveRun?.visible && !liveRun?.terminal)) {
    return "";
  }
  if (!conversationId || streamConversationId !== conversationId) {
    return "";
  }
  if (transport !== "sse" || renderSource !== "sse") {
    return "";
  }
  if (!liveRun?.visible || !liveRun.phase || liveRun.phase === "IDLE") {
    return "";
  }
  if (liveRun.state === "sending" || liveRun.state === "generating") {
    return "";
  }
  const tone = transcriptLiveTone(liveRun);
  const detail = simplifyText(phaseDetailHint(liveRun) || liveRun.detail || "");
  const appendId = Number(appendStream.lastLiveAppendId || appendStream.lastAppendId || 0);
  return `
    <article class="timeline-item live-activity" data-live-activity-turn="true" data-live-run-state="${escapeHtml(liveRun.state)}" data-live-run-phase="${escapeHtml(liveRun.phase)}" data-live-run-source="${escapeHtml(liveRun.source)}" data-append-id="${appendId}" data-append-source="sse-live-activity">
      <p class="timeline-kind">실시간 진행</p>
      <div class="timeline-live-row">
        <span class="timeline-live-chip" data-tone="neutral">LIVE</span>
        <span class="timeline-live-chip" data-tone="${escapeHtml(tone)}">${escapeHtml(String(liveRun.phase || "LIVE").toUpperCase())}</span>
      </div>
      <p class="timeline-body">${escapeHtml(detail || "선택된 대화의 최신 live 진행 상태를 반영하는 중입니다.")}</p>
      <p class="timeline-meta">selected thread · ${escapeHtml(status.toUpperCase())}${liveRun.jobId ? ` · ${escapeHtml(liveRun.jobId)}` : ""} · <span class="timeline-provenance">SSE LIVE</span></p>
    </article>
  `;
}

function pendingHandoffState(conversation, currentState) {
  const conversationId = String(conversation?.conversation_id || "");
  const pendingOutgoing = currentState.pendingOutgoing || {};
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
  const liveFollow = currentState.liveFollow || {};
  const unseenCount = Math.max(
    Number(liveFollow.pendingAppendCount || 0),
    Number(liveFollow.lastAppendId || 0) - Number(liveFollow.lastSeenAppendId || 0),
  );
  const followState = renderSource === "sse" ? "new" : "paused";
  const isVisible = Boolean(conversationId && liveFollow.jumpVisible && unseenCount > 0);
  const stateLabel = followState === "new" ? "NEW" : "PAUSED";
  const detailLabel =
    followState === "new"
      ? unseenCount > 1
        ? `새 live append ${unseenCount}개`
        : "새 live append"
      : "live follow paused";
  dom.jumpToLatestButton.hidden = !isVisible;
  dom.jumpToLatestButton.dataset.followConversationId = conversationId || "";
  dom.jumpToLatestButton.dataset.followMode = liveFollow.isFollowing ? "following" : "paused";
  dom.jumpToLatestButton.dataset.followState = isVisible ? followState : "hidden";
  dom.jumpToLatestButton.dataset.followCount = String(isVisible ? unseenCount : 0);
  dom.jumpToLatestButton.dataset.followRenderSource = renderSource || "snapshot";
  dom.jumpToLatestButton.setAttribute(
    "aria-label",
    isVisible ? `${stateLabel}. ${detailLabel}. 최신 응답으로 이동` : "최신 응답으로 이동",
  );
  dom.jumpToLatestButton.innerHTML = isVisible
    ? `<span class="jump-to-latest-chip">${stateLabel}</span><span class="jump-to-latest-copy">${detailLabel}</span>`
    : '<span class="jump-to-latest-chip">NEW</span><span class="jump-to-latest-copy">최신 응답으로 이동</span>';
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
  const jobId = String(currentState.currentJobId || conversation?.latest_job_id || "");
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  const relevantEvents = jobId ? events.filter((event) => !event.job_id || event.job_id === jobId) : events;
  const latestEvent = relevantEvents.length ? relevantEvents[relevantEvents.length - 1] : null;
  const latestType = String(latestEvent?.type || "");
  const latestStatus = String(latestEvent?.status || "").toLowerCase();
  const eventSource = String(latestEvent?.delivery_source || "snapshot").toLowerCase();
  const pendingOutgoing = currentState.pendingOutgoing || {};

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

  if (pendingOutgoing.status === "awaiting-assistant" && pendingOutgoing.conversationId === conversation.conversation_id) {
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

  if (!latestEvent) {
    return runStateSnapshot({
      visible: true,
      state: "done",
      phase: "IDLE",
      detail: "현재 이 대화에서 실행 중인 작업이 없습니다.",
      source: "none",
      tone: "idle",
      jobId,
      terminal: false,
    });
  }

  if (latestStatus === "failed" || latestType === "runtime.exception") {
    return runStateSnapshot({
      visible: true,
      state: "failed",
      phase: "FAILED",
      detail: phaseDetail("실행이 실패 또는 예외 상태로 끝났습니다.", latestEvent, "실행이 끝났지만 예외 또는 실패 신호가 기록되었습니다."),
      source: `${eventSource}-event`,
      tone: "done",
      jobId,
      terminal: true,
    });
  }

  if (latestType === "goal.proposal.auto_apply.started") {
    return runStateSnapshot({
      visible: true,
      state: "auto-apply",
      phase: "AUTO APPLY",
      detail: phaseDetail("승인된 proposal을 자동 적용 중입니다.", latestEvent, "승인된 proposal을 자동 적용 중입니다."),
      source: `${eventSource}-event`,
      tone: "running",
      jobId,
      terminal: false,
    });
  }

  if (latestType.startsWith("goal.verify.phase.")) {
    return runStateSnapshot({
      visible: true,
      state: "verify-phase",
      phase: "VERIFY",
      detail:
        latestType === "goal.verify.phase.completed"
          ? phaseDetail("검증 단계가 최신 결과를 정리했습니다.", latestEvent, "검증 단계가 최신 결과를 정리했습니다.")
          : phaseDetail("Verifier가 구현 결과를 검증 중입니다.", latestEvent, "Verifier가 구현 결과를 검증 중입니다."),
      source: `${eventSource}-event`,
      tone: "running",
      jobId,
      terminal: false,
    });
  }

  if (latestType.startsWith("goal.review.phase.")) {
    return runStateSnapshot({
      visible: true,
      state: "review-phase",
      phase: "REVIEW",
      detail:
        latestType === "goal.review.phase.completed"
          ? phaseDetail("리뷰 단계가 최신 평가를 남겼습니다.", latestEvent, "리뷰 단계가 최신 평가를 남겼습니다.")
          : phaseDetail("Reviewer가 현재 bounded hypothesis를 검토 중입니다.", latestEvent, "Reviewer가 현재 bounded hypothesis를 검토 중입니다."),
      source: `${eventSource}-event`,
      tone: "thinking",
      jobId,
      terminal: false,
    });
  }

  if (latestType.startsWith("goal.proposal.phase.")) {
    return runStateSnapshot({
      visible: true,
      state: "proposal-phase",
      phase: "PROPOSAL",
      detail:
        latestType === "goal.proposal.phase.completed"
          ? phaseDetail("제안 단계가 최신 bounded hypothesis를 정리했습니다.", latestEvent, "제안 단계가 최신 bounded hypothesis를 정리했습니다.")
          : phaseDetail("현재 bounded hypothesis를 제안 중입니다.", latestEvent, "현재 bounded hypothesis를 제안 중입니다."),
      source: `${eventSource}-event`,
      tone: "thinking",
      jobId,
      terminal: false,
    });
  }

  if (latestType === "proposal.ready") {
    return runStateSnapshot({
      visible: true,
      state: "proposal-ready",
      phase: "READY",
      detail: phaseDetail("Proposal이 준비되어 다음 승인 또는 적용 결정을 기다립니다.", latestEvent, "Proposal이 준비되어 다음 승인 또는 적용 결정을 기다립니다."),
      source: `${eventSource}-event`,
      tone: "waiting",
      jobId,
      terminal: true,
    });
  }

  if (latestType === "codex.exec.applied" || latestStatus === "applied") {
    return runStateSnapshot({
      visible: true,
      state: "applied",
      phase: "APPLIED",
      detail: phaseDetail("최신 proposal 적용이 반영되었습니다.", latestEvent, "최신 proposal 적용이 반영되었습니다."),
      source: `${eventSource}-event`,
      tone: "done",
      jobId,
      terminal: true,
    });
  }

  if (latestType === "codex.exec.started") {
    return runStateSnapshot({
      visible: true,
      state: "running-tool",
      phase: "RUNNING",
      detail: "에이전트가 현재 tool 또는 Codex 실행 단계를 처리 중입니다.",
      source: `${eventSource}-event`,
      tone: "running",
      jobId,
      terminal: false,
    });
  }

  if (
    latestType === "message.accepted" ||
    latestType === "job.queued" ||
    latestType === "codex.exec.finished"
  ) {
    return runStateSnapshot({
      visible: true,
      state: latestType === "message.accepted" ? "accepted" : "waiting",
      phase: latestType === "message.accepted" ? "ACCEPTED" : "QUEUED",
      detail:
        latestType === "message.accepted"
          ? phaseDetail("서버 handoff가 확인되어 첫 live 응답을 기다리는 중입니다.", latestEvent, "서버 handoff가 확인되어 첫 live 응답을 기다리는 중입니다.")
          : "다음 실행 단계나 응답 정리를 기다리는 중입니다.",
      source: `${eventSource}-event`,
      tone: "waiting",
      jobId,
      terminal: false,
    });
  }

  if (
    latestType === "intent.interpreted" ||
    latestType.startsWith("runtime.") ||
    latestType === "job.running" ||
    latestType.includes(".phase.started")
  ) {
    return runStateSnapshot({
      visible: true,
      state: "thinking",
      phase: latestType === "job.running" ? "RUNNING" : "PLANNING",
      detail:
        latestType === "job.running"
          ? "에이전트가 현재 실행 단계를 처리 중입니다."
          : "에이전트가 현재 맥락을 읽고 다음 단계를 준비 중입니다.",
      source: `${eventSource}-event`,
      tone: latestType === "job.running" ? "running" : "thinking",
      jobId,
      terminal: false,
    });
  }

  if (latestType === "job.completed" || latestStatus === "completed") {
    return runStateSnapshot({
      visible: true,
      state: "done",
      phase: "DONE",
      detail: "현재 활성 실행이 끝났고 최신 결과가 반영되었습니다.",
      source: `${eventSource}-event`,
      tone: "done",
      jobId,
      terminal: true,
    });
  }

  return runStateSnapshot({
    visible: true,
    state: "thinking",
    phase: "PLANNING",
    detail: "선택된 대화의 최신 실행 신호를 처리 중입니다.",
    source: `${eventSource}-event`,
    tone: "thinking",
    jobId,
    terminal: false,
  });
}

function latestMeaningfulConversationEvent(conversation, currentState) {
  const jobId = String(currentState.currentJobId || conversation?.latest_job_id || "");
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  const relevantEvents = jobId ? events.filter((event) => !event.job_id || event.job_id === jobId) : events;
  for (let index = relevantEvents.length - 1; index >= 0; index -= 1) {
    const event = relevantEvents[index];
    const type = String(event?.type || "");
    const status = String(event?.status || "").toLowerCase();
    if (
      type.startsWith("goal.proposal.phase.") ||
      type.startsWith("goal.review.phase.") ||
      type.startsWith("goal.verify.phase.") ||
      type === "goal.proposal.auto_apply.started" ||
      type === "proposal.ready" ||
      type === "codex.exec.applied" ||
      type === "job.completed" ||
      type === "job.running" ||
      type === "job.queued" ||
      type === "message.accepted" ||
      type === "runtime.exception" ||
      type === "codex.exec.started" ||
      type === "codex.exec.finished" ||
      status === "failed" ||
      status === "completed" ||
      status === "applied"
    ) {
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
    return { label: "GENERATING", tone: "neutral" };
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
    return "bounded hypothesis 정리 중";
  }
  if (liveRun.state === "review-phase") {
    return "review 승인 신호 확인 중";
  }
  if (liveRun.state === "verify-phase") {
    return "verify 결과 수집 중";
  }
  if (liveRun.state === "auto-apply") {
    return "승인 후 자동 적용 진행 중";
  }
  if (liveRun.state === "proposal-ready") {
    return "proposal 승인 또는 적용 대기";
  }
  if (liveRun.state === "applied") {
    return "proposal 적용 반영 완료";
  }
  if (liveRun.state === "accepted" || liveRun.phase === "ACCEPTED") {
    return "첫 응답 대기";
  }
  if (liveRun.state === "generating") {
    return "첫 응답 생성 중";
  }
  if (liveRun.state === "failed") {
    return "실패 또는 예외 확인 필요";
  }
  if (liveRun.state === "sending") {
    return "메시지 handoff 진행 중";
  }
  return liveRun.detail || "현재 상태를 확인할 수 있습니다.";
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
    parts.push(phaseDetailHint(liveRun));
    return parts.filter(Boolean).join(" · ");
  }
  parts.push(`${messageCount} messages`);
  parts.push(`${eventCount} events`);
  return parts.filter(Boolean).join(" · ");
}

function renderThreadTransition(currentState) {
  const threadTransition = currentState.threadTransition || {};
  const targetTitle = String(threadTransition.targetTitle || "선택한 대화").trim();
  return `
    <article class="timeline-transition" data-thread-transition="loading" data-thread-transition-conversation-id="${escapeHtml(String(threadTransition.targetConversationId || ""))}">
      <p class="timeline-kind">세션 전환</p>
      <div class="timeline-transition-row">
        <span class="timeline-transition-chip">SWITCH</span>
        <span class="timeline-transition-chip">${escapeHtml(targetTitle.toUpperCase())}</span>
      </div>
      <p class="timeline-body">이전 thread의 live 소유권은 정리했고, 새 선택 대화의 snapshot과 append stream을 연결하는 중입니다.</p>
      <p class="timeline-meta">selected thread handoff · snapshot attach pending</p>
    </article>
  `;
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

  const conversationId = conversation?.conversation_id || "";
  const appendStream = currentState.appendStream || {};
  const status = String(appendStream.status || "offline").toLowerCase();
  const lastAppendId = Number(appendStream.lastAppendId || maxConversationAppendId(conversation) || 0);
  const lastRenderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const lastLiveAppendId = Number(appendStream.lastLiveAppendId || 0);
  const liveRun = deriveLiveRunState(conversation, currentState);
  currentState.sessionRail ||= { conversationId: "", expanded: false };

  if (!conversationId) {
    dom.sessionStrip.hidden = true;
    dom.sessionStrip.dataset.sessionPresentation = "cleared";
    dom.sessionStrip.dataset.sessionTerminal = "false";
    dom.sessionStrip.dataset.streamState = "offline";
    dom.sessionStrip.dataset.renderSource = "snapshot";
    dom.sessionStrip.dataset.liveConversationId = "";
    dom.sessionStrip.dataset.lastAppendId = "0";
    dom.sessionStrip.dataset.lastLiveAppendId = "0";
    dom.sessionStrip.dataset.liveRunState = "done";
    dom.sessionStrip.dataset.liveRunPhase = "IDLE";
    dom.sessionStrip.dataset.liveRunSource = "none";
    dom.sessionStrip.dataset.liveRunJob = "";
    dom.sessionStrip.dataset.liveRunTone = "idle";
    dom.sessionStrip.dataset.sessionCollapsed = "false";
    dom.threadScroller.dataset.streamState = "offline";
    dom.threadScroller.dataset.renderSource = "snapshot";
    dom.threadScroller.dataset.liveConversationId = "";
    dom.threadScroller.dataset.lastAppendId = "0";
    dom.threadScroller.dataset.lastLiveAppendId = "0";
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
    }
    return;
  }

  if (currentState.sessionRail.conversationId !== conversationId) {
    currentState.sessionRail = {
      conversationId,
      expanded: false,
    };
  }

  const presentation =
    status === "reconnecting"
      ? "reconnecting"
      : status === "connecting"
        ? "connecting"
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
  const transportState = transportChip(status, presentation);
  const phaseState = phaseChip(liveRun, presentation);
  const proposalState = proposalChip(liveRun);
  const showComposerLiveStrip = shouldShowComposerLiveStrip(appendStream, conversationId, lastRenderSource, liveRun);
  const liveOwned = showComposerLiveStrip && status === "live" && lastRenderSource === "sse";
  dom.sessionStrip.hidden = !showComposerLiveStrip;
  dom.sessionStrip.dataset.liveOwned = liveOwned ? "true" : "false";
  dom.sessionStrip.dataset.sessionPresentation = presentation;
  dom.sessionStrip.dataset.sessionTerminal = liveRun.terminal ? "true" : "false";
  dom.sessionStrip.dataset.sessionCollapsed = shouldCollapse ? "true" : "false";
  dom.sessionStrip.dataset.streamState = status;
  dom.sessionStrip.dataset.renderSource = lastRenderSource;
  dom.sessionStrip.dataset.liveConversationId = conversationId;
  dom.sessionStrip.dataset.lastAppendId = String(lastAppendId || 0);
  dom.sessionStrip.dataset.lastLiveAppendId = String(lastLiveAppendId || 0);
  dom.sessionStrip.dataset.liveRunState = liveRun.state;
  dom.sessionStrip.dataset.liveRunPhase = liveRun.phase;
  dom.sessionStrip.dataset.liveRunSource = liveRun.source;
  dom.sessionStrip.dataset.liveRunJob = liveRun.jobId || "";
  dom.sessionStrip.dataset.liveRunTone = liveRun.tone;

  dom.sessionStripState.innerHTML = [
    `<span class="session-chip" data-tone="${escapeHtml(transportState.tone)}">${escapeHtml(transportState.label)}</span>`,
    `<span class="session-chip" data-tone="${escapeHtml(phaseState.tone)}">${escapeHtml(phaseState.label)}</span>`,
    `<span class="session-chip" data-tone="${escapeHtml(proposalState.tone)}">${escapeHtml(proposalState.label)}</span>`,
  ].join("");
  dom.sessionStripMeta.textContent = sessionProvenance(status, lastAppendId, lastLiveAppendId, liveRun);
  dom.sessionStripDetail.textContent = phaseDetailHint(liveRun);
  if (dom.sessionStripToggle) {
    dom.sessionStripToggle.hidden = true;
    dom.sessionStripToggle.textContent = "세부 보기";
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
  dom.threadScroller.dataset.renderSource = lastRenderSource;
  dom.threadScroller.dataset.liveConversationId = conversationId;
  dom.threadScroller.dataset.lastAppendId = String(lastAppendId || 0);
  dom.threadScroller.dataset.lastLiveAppendId = String(lastLiveAppendId || 0);
  dom.threadScroller.dataset.sessionPresentation = presentation;
  dom.threadScroller.dataset.sessionTerminal = liveRun.terminal ? "true" : "false";
  dom.threadScroller.dataset.liveRunState = liveRun.state;
  dom.threadScroller.dataset.liveRunPhase = liveRun.phase;
  dom.threadScroller.dataset.liveRunSource = liveRun.source;
  dom.threadScroller.dataset.liveRunJob = liveRun.jobId || "";
  dom.threadScroller.dataset.sessionCollapsed = shouldCollapse ? "true" : "false";
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
  if (dom.autonomyDetailMeta) {
    dom.autonomyDetailMeta.textContent = "표시할 자율 goal이 없습니다.";
  }
  if (dom.autonomyDetail) {
    dom.autonomyDetail.dataset.empty = "true";
    dom.autonomyDetail.dataset.blockerReason = "none";
    dom.autonomyDetail.dataset.pathVerdict = "unknown";
    dom.autonomyDetail.dataset.verifierAcceptability = "pending";
    dom.autonomyDetail.innerHTML = `<p class="autonomy-empty">${escapeHtml(message)}</p>`;
  }
}

function setAutonomyDataset(target, { blockerReason, pathVerdict, verifierAcceptability }) {
  if (!target) {
    return;
  }
  target.dataset.empty = "false";
  target.dataset.blockerReason = blockerReason;
  target.dataset.pathVerdict = pathVerdict.toLowerCase();
  target.dataset.verifierAcceptability = verifierAcceptability.toLowerCase();
}

export function renderAutonomySummary(dom, goal) {
  const iteration = latestIteration(goal);
  if (!goal || !iteration) {
    clearAutonomySummary(dom);
    return;
  }

  const intendedPath = iteration.intended_path || {};
  const pathVerdict = String(intendedPath.verdict || "").toLowerCase() === "expected" ? "EXPECTED" : "DEGRADED";
  const verifierAcceptability = summarizeVerifierAcceptability(iteration);
  const blockerReason = String(iteration.continuation_blocker_reason || goal.stop_reason || "none");
  const degradedSignals = Array.isArray(intendedPath.degraded_signals) ? intendedPath.degraded_signals : [];
  const expectedPath = String(intendedPath.expected_path || "").trim() || "unknown";
  const blockerClass = blockerTone(blockerReason);
  const heading = `${goal.title || "Autonomy Goal"} · ${goal.status || "unknown"} · iteration ${iteration.iteration}`;

  if (dom.autonomyDetailMeta) {
    dom.autonomyDetailMeta.textContent = heading;
  }
  if (dom.autonomyDetail) {
    setAutonomyDataset(dom.autonomyDetail, { blockerReason, pathVerdict, verifierAcceptability });
    dom.autonomyDetail.innerHTML = `
      <div class="autonomy-chip-row autonomy-chip-row-compact">
        <span class="autonomy-chip ${pathVerdict === "EXPECTED" ? "healthy" : "blocked"}">${pathVerdict}</span>
        <span class="autonomy-chip ${verifierAcceptability === "DISQUALIFYING" ? "blocked" : verifierAcceptability === "ACCEPTABLE" ? "healthy" : "neutral"}">${verifierAcceptability}</span>
        <span class="autonomy-chip ${blockerClass}">BLOCKER ${escapeHtml(blockerReason.toUpperCase())}</span>
      </div>
      <div class="autonomy-inline-meta">
        <p class="autonomy-inline-item"><span>Iteration</span>${escapeHtml(String(iteration.iteration))}</p>
        <p class="autonomy-inline-item"><span>Path</span>${escapeHtml(expectedPath)}</p>
        <p class="autonomy-inline-item"><span>Signals</span>${escapeHtml(degradedSignals.length ? degradedSignals.join(", ") : "none")}</p>
      </div>
    `;
  }
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

export function renderJobActivity(dom, conversation, currentJobId, jobPayload = null) {
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  const relevantEvents = currentJobId ? events.filter((event) => event.job_id === currentJobId) : events;
  const recentEvents = relevantEvents.slice(-4).reverse();

  const latestEvent = recentEvents[0];
  const phase = phaseLabel(jobPayload?.status || latestEvent?.status || "", latestEvent?.type || "");
  dom.jobPhase.textContent = phase;
  dom.jobPhase.className = `activity-phase ${phase.toLowerCase()}`;

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
  currentState.currentConversationId = conversation ? conversation.conversation_id : "";
  if (conversation) {
    currentState.appendStream ||= {};
    currentState.appendStream.lastAppendId = Math.max(
      Number(currentState.appendStream.lastAppendId || 0),
      maxConversationAppendId(conversation),
    );
  }
  onPersist();

  if (!conversation) {
    const isThreadTransition = Boolean(threadTransition.active && threadTransition.targetConversationId);
    dom.conversationTimeline.innerHTML = isThreadTransition
      ? renderThreadTransition(currentState)
      : '<p class="timeline-empty">새 대화를 만들면 요청과 이벤트가 여기 쌓입니다.</p>';
    if (dom.threadScroller) {
      dom.threadScroller.dataset.pendingConversationId = isThreadTransition
        ? String(threadTransition.targetConversationId || "")
        : "";
      dom.threadScroller.dataset.pendingHandoffStage = "idle";
      dom.threadScroller.dataset.pendingUserCount = "0";
      dom.threadScroller.dataset.pendingAssistantCount = "0";
      dom.threadScroller.dataset.threadTransitionState = isThreadTransition ? "loading" : "idle";
      dom.threadScroller.dataset.threadTransitionConversationId = isThreadTransition
        ? String(threadTransition.targetConversationId || "")
        : "";
    }
    renderSessionStrip(dom, currentState, null);
    currentState.liveFollow = {
      conversationId: isThreadTransition ? String(threadTransition.targetConversationId || "") : "",
      isFollowing: true,
      jumpVisible: false,
      lastAppendId: 0,
      lastSeenAppendId: 0,
      pendingAppendCount: 0,
    };
    syncJumpToLatest(dom, currentState, currentState.liveFollow.conversationId, "snapshot");
    updateHeroState(dom, {
      threadTitle: isThreadTransition ? String(threadTransition.targetTitle || "대화 전환 중") : "새 대화를 시작하세요",
      threadKicker: "선택된 대화",
      conversationState: isThreadTransition ? "새 대화 스냅샷을 연결하는 중입니다." : "아직 대화 세션이 없습니다.",
      liveRun: runStateSnapshot({
        visible: true,
        phase: currentState.currentJobId ? "RUNNING" : "IDLE",
        source: "none",
        tone: currentState.currentJobId ? "running" : "idle",
      }),
    });
    renderWorkspaceSummary(
      dom,
      isThreadTransition
        ? "더 깊은 실행 맥락은 이 패널에서 확인합니다."
        : "더 깊은 실행 맥락은 이 패널에서 확인합니다.",
    );
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
    syncComposerOwnership(dom, currentState, null);
    renderJobActivity(dom, null, "");
    return;
  }

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
  if (dom.threadScroller) {
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
  syncComposerOwnership(dom, currentState, conversation);
  renderWorkspaceSummary(
    dom,
    [
      conversation.latest_job_id ? `job ${conversation.latest_job_id}` : "job 없음",
      messages.length ? `메시지 ${messages.length}` : "메시지 0",
      events.length ? `이벤트 ${events.length}` : "이벤트 0",
    ].join(" · "),
  );

  if (!items.length && !inlineSessionBlock) {
    dom.conversationTimeline.innerHTML = '<p class="timeline-empty">아직 메시지가 없습니다.</p>';
    return;
  }

  const liveActivityTurn = renderTranscriptLiveActivity(conversation, currentState, liveRun);
  dom.conversationTimeline.innerHTML = inlineSessionBlock + items
    .map((item) => {
      if (item.kind === "event") {
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
    .join("") + liveActivityTurn;
  if (dom.threadScroller && currentState.liveFollow.isFollowing) {
    dom.threadScroller.scrollTop = dom.threadScroller.scrollHeight;
  }
  syncJumpToLatest(dom, currentState, conversation.conversation_id, renderSource);

  renderJobActivity(dom, conversation, currentState.currentJobId || conversation.latest_job_id || "");

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
