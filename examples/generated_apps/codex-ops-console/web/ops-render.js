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

export function updateHeroState(dom, { appName = "", conversationState = "", jobState = "" }) {
  if (appName) {
    dom.heroAppName.textContent = appName;
  }
  if (conversationState) {
    dom.heroConversationState.textContent = conversationState;
  }
  if (jobState) {
    dom.heroJobState.textContent = jobState;
  }
}

export function renderWorkspaceSummary(dom, summary) {
  dom.workspaceSummaryText.textContent = summary;
}

export function renderDraftStatus(dom, message) {
  dom.draftStatus.textContent = message;
}

function deriveLiveRunState(conversation, currentState) {
  const jobId = String(currentState.currentJobId || conversation?.latest_job_id || "");
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  const relevantEvents = jobId ? events.filter((event) => !event.job_id || event.job_id === jobId) : events;
  const latestEvent = relevantEvents.length ? relevantEvents[relevantEvents.length - 1] : null;
  const latestType = String(latestEvent?.type || "");
  const latestStatus = String(latestEvent?.status || "").toLowerCase();
  const eventSource = String(latestEvent?.delivery_source || "snapshot").toLowerCase();

  if (!conversation?.conversation_id) {
    return {
      visible: false,
      state: "done",
      detail: "",
      source: "none",
      tone: "idle",
      jobId: "",
      terminal: false,
    };
  }

  if (!latestEvent) {
    return {
      visible: true,
      state: "done",
      detail: "현재 이 대화에서 실행 중인 작업이 없습니다.",
      source: "none",
      tone: "idle",
      jobId,
      terminal: false,
    };
  }

  if (latestType === "codex.exec.started") {
    return {
      visible: true,
      state: "running-tool",
      detail: "에이전트가 현재 tool 또는 Codex 실행 단계를 처리 중입니다.",
      source: `${eventSource}-event`,
      tone: "running",
      jobId,
      terminal: false,
    };
  }

  if (
    latestType === "message.accepted" ||
    latestType === "job.queued" ||
    latestType === "codex.exec.finished"
  ) {
    return {
      visible: true,
      state: "waiting",
      detail: "다음 실행 단계나 응답 정리를 기다리는 중입니다.",
      source: `${eventSource}-event`,
      tone: "waiting",
      jobId,
      terminal: false,
    };
  }

  if (
    latestType === "intent.interpreted" ||
    latestType.startsWith("runtime.") ||
    latestType === "job.running" ||
    latestType.includes(".phase.started")
  ) {
    return {
      visible: true,
      state: "thinking",
      detail: "에이전트가 현재 맥락을 읽고 다음 단계를 준비 중입니다.",
      source: `${eventSource}-event`,
      tone: "thinking",
      jobId,
      terminal: false,
    };
  }

  if (
    latestType === "job.completed" ||
    latestStatus === "completed" ||
    latestType === "proposal.ready" ||
    latestType === "codex.exec.applied"
  ) {
    return {
      visible: true,
      state: "done",
      detail: "현재 활성 실행이 끝났고 최신 결과가 반영되었습니다.",
      source: `${eventSource}-event`,
      tone: "done",
      jobId,
      terminal: true,
    };
  }

  if (latestStatus === "failed" || latestType === "runtime.exception") {
    return {
      visible: true,
      state: "done",
      detail: "실행이 끝났지만 예외 또는 실패 신호가 기록되었습니다.",
      source: `${eventSource}-event`,
      tone: "done",
      jobId,
      terminal: true,
    };
  }

  return {
    visible: true,
    state: "thinking",
    detail: "선택된 대화의 최신 실행 신호를 처리 중입니다.",
    source: `${eventSource}-event`,
    tone: "thinking",
    jobId,
    terminal: false,
  };
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
    dom.sessionStrip.dataset.liveRunSource = "none";
    dom.sessionStrip.dataset.liveRunJob = "";
    dom.sessionStrip.dataset.liveRunTone = "idle";
    dom.threadScroller.dataset.streamState = "offline";
    dom.threadScroller.dataset.renderSource = "snapshot";
    dom.threadScroller.dataset.liveConversationId = "";
    dom.threadScroller.dataset.lastAppendId = "0";
    dom.threadScroller.dataset.lastLiveAppendId = "0";
    dom.threadScroller.dataset.sessionPresentation = "cleared";
    dom.threadScroller.dataset.sessionTerminal = "false";
    dom.threadScroller.dataset.liveRunState = "done";
    dom.threadScroller.dataset.liveRunSource = "none";
    dom.threadScroller.dataset.liveRunJob = "";
    return;
  }

  const presentation =
    status === "reconnecting"
      ? "reconnecting"
      : status === "connecting"
        ? "connecting"
        : status === "live" && !liveRun.terminal && liveRun.tone !== "idle"
          ? "live"
          : liveRun.terminal
            ? "terminal"
            : "idle";
  const shouldCollapse = presentation === "idle" || presentation === "terminal";
  dom.sessionStrip.hidden = shouldCollapse;
  dom.sessionStrip.dataset.sessionPresentation = presentation;
  dom.sessionStrip.dataset.sessionTerminal = liveRun.terminal ? "true" : "false";
  dom.sessionStrip.dataset.streamState = status;
  dom.sessionStrip.dataset.renderSource = lastRenderSource;
  dom.sessionStrip.dataset.liveConversationId = conversationId;
  dom.sessionStrip.dataset.lastAppendId = String(lastAppendId || 0);
  dom.sessionStrip.dataset.lastLiveAppendId = String(lastLiveAppendId || 0);
  dom.sessionStrip.dataset.liveRunState = liveRun.state;
  dom.sessionStrip.dataset.liveRunSource = liveRun.source;
  dom.sessionStrip.dataset.liveRunJob = liveRun.jobId || "";
  dom.sessionStrip.dataset.liveRunTone = liveRun.tone;

  const streamLabelByStatus = {
    connecting: "CONNECTING",
    live: "LIVE",
    reconnecting: "RECONNECTING",
    offline: "OFFLINE",
  };
  const runLabel = liveRun.state.replaceAll("-", " ").toUpperCase();
  dom.sessionStripState.textContent = `${streamLabelByStatus[status] || "OFFLINE"} · ${runLabel}`;
  dom.sessionStripMeta.textContent =
    `${status === "live" ? "SSE" : status === "reconnecting" ? "SSE RESUME" : status === "connecting" ? "SSE OPEN" : "SNAPSHOT"} · append #${lastLiveAppendId || lastAppendId || 0} · ${liveRun.source.toUpperCase()}`;
  dom.sessionStripDetail.textContent =
    status === "live"
      ? `${liveRun.detail} 새 append는 SSE로 바로 반영됩니다.`
      : status === "reconnecting"
        ? `${liveRun.detail} 연결을 복구하는 동안 최근 append 이후를 resume 대기합니다.`
        : status === "connecting"
          ? `${liveRun.detail} 선택된 대화의 live stream을 여는 중입니다.`
          : `${liveRun.detail} 현재는 snapshot 또는 polling 경로만 사용합니다.`;

  dom.threadScroller.dataset.streamState = status;
  dom.threadScroller.dataset.renderSource = lastRenderSource;
  dom.threadScroller.dataset.liveConversationId = conversationId;
  dom.threadScroller.dataset.lastAppendId = String(lastAppendId || 0);
  dom.threadScroller.dataset.lastLiveAppendId = String(lastLiveAppendId || 0);
  dom.threadScroller.dataset.sessionPresentation = presentation;
  dom.threadScroller.dataset.sessionTerminal = liveRun.terminal ? "true" : "false";
  dom.threadScroller.dataset.liveRunState = liveRun.state;
  dom.threadScroller.dataset.liveRunSource = liveRun.source;
  dom.threadScroller.dataset.liveRunJob = liveRun.jobId || "";
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
  dom.autonomyMeta.textContent = "표시할 자율 goal이 없습니다.";
  dom.autonomySummary.dataset.empty = "true";
  dom.autonomySummary.dataset.blockerReason = "none";
  dom.autonomySummary.dataset.pathVerdict = "unknown";
  dom.autonomySummary.dataset.verifierAcceptability = "pending";
  dom.autonomySummary.innerHTML = `<p class="autonomy-empty">${escapeHtml(message)}</p>`;
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

  dom.autonomyMeta.textContent = `${goal.title || "Autonomy Goal"} · ${goal.status || "unknown"} · iteration ${iteration.iteration}`;
  dom.autonomySummary.dataset.empty = "false";
  dom.autonomySummary.dataset.blockerReason = blockerReason;
  dom.autonomySummary.dataset.pathVerdict = pathVerdict.toLowerCase();
  dom.autonomySummary.dataset.verifierAcceptability = verifierAcceptability.toLowerCase();
  dom.autonomySummary.innerHTML = `
    <div class="autonomy-chip-row autonomy-chip-row-compact">
      <span class="autonomy-chip ${pathVerdict === "EXPECTED" ? "healthy" : "blocked"}">${pathVerdict}</span>
      <span class="autonomy-chip ${verifierAcceptability === "DISQUALIFYING" ? "blocked" : verifierAcceptability === "ACCEPTABLE" ? "healthy" : "neutral"}">${verifierAcceptability}</span>
      <span class="autonomy-chip ${blockerClass}">BLOCKER ${escapeHtml(blockerReason.toUpperCase())}</span>
    </div>
    <div class="autonomy-inline-meta">
      <p class="autonomy-inline-item"><span>Path</span>${escapeHtml(expectedPath)}</p>
      <p class="autonomy-inline-item"><span>Signals</span>${escapeHtml(degradedSignals.length ? degradedSignals.join(", ") : "none")}</p>
    </div>
  `;
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
  updateHeroState(dom, { jobState: phase });

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
    updateHeroState(dom, {
      appName: "앱 미선택",
      conversationState: "대화 준비 전",
      jobState: "IDLE",
    });
    renderWorkspaceSummary(dom, "앱을 고르면 현재 작업 라인, 최근 대화, 배포 진입점이 여기에 요약됩니다.");
    return;
  }

  dom.selectedAppUrl.textContent = hasDeployment
    ? app.deploymentUrl
    : "deployment_url이 아직 등록되지 않았습니다.";
  updateHeroState(dom, { appName: app.title || app.appId });
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
    dom.conversationMeta.textContent = "아직 대화 세션이 없습니다.";
    dom.conversationTimeline.innerHTML = '<p class="timeline-empty">새 대화를 만들면 요청과 이벤트가 여기 쌓입니다.</p>';
    if (dom.threadScroller) {
      dom.threadScroller.dataset.pendingConversationId ||= "";
    }
    renderSessionStrip(dom, currentState, null);
    updateHeroState(dom, {
      conversationState: "새 대화 필요",
      jobState: currentState.currentJobId ? "RUNNING" : "IDLE",
    });
    renderWorkspaceSummary(dom, "아직 대화가 없습니다. 새 대화를 만들거나 바로 메시지를 보내면 현재 앱 레인에서 이어서 작업합니다.");
    renderJobActivity(dom, null, "");
    return;
  }

  const messages = Array.isArray(conversation.messages) ? conversation.messages : [];
  const events = Array.isArray(conversation.events) ? conversation.events : [];
  const items = [
    ...messages.map((item) => ({ ...item, kind: "message", sortAt: item.created_at })),
    ...events.map((item) => ({ ...item, kind: "event", sortAt: item.created_at })),
  ].sort((a, b) => {
    const leftAppendId = Number(a.append_id || 0);
    const rightAppendId = Number(b.append_id || 0);
    if (leftAppendId && rightAppendId && leftAppendId !== rightAppendId) {
      return leftAppendId - rightAppendId;
    }
    return a.sortAt < b.sortAt ? -1 : 1;
  });

  dom.conversationMeta.textContent = `${messages.length} messages · ${events.length} events`;
  if (dom.threadScroller) {
    dom.threadScroller.dataset.pendingConversationId = "";
  }
  renderSessionStrip(dom, currentState, conversation);
  updateHeroState(dom, {
    conversationState: `${messages.length} msgs · ${events.length} evts`,
  });
  renderWorkspaceSummary(
    dom,
    [
      conversation.title,
      conversation.latest_job_id ? `최근 job: ${conversation.latest_job_id}` : "최근 job 없음",
      messages.length ? `메시지 ${messages.length}개` : "메시지 없음",
      events.length ? `이벤트 ${events.length}개` : "이벤트 없음",
    ].join(" · "),
  );

  if (!items.length) {
    dom.conversationTimeline.innerHTML = '<p class="timeline-empty">아직 메시지가 없습니다.</p>';
    return;
  }

  dom.conversationTimeline.innerHTML = items
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
        <article class="timeline-item message ${item.role || "assistant"}" data-append-id="${Number(item.append_id || 0)}" data-append-source="${escapeHtml(String(item.delivery_source || "snapshot"))}">
          <p class="timeline-kind">${item.role === "user" ? "사용자" : "에이전트"}</p>
          <p class="timeline-body">${escapeHtml(simplifyText(item.body))}</p>
          <p class="timeline-meta">${item.created_at}${item.job_id ? ` · ${item.job_id}` : ""}${item.delivery_source === "sse" ? ' · <span class="timeline-provenance">SSE LIVE</span>' : ""}</p>
        </article>
      `;
    })
    .join("");
  if (dom.threadScroller) {
    dom.threadScroller.scrollTop = dom.threadScroller.scrollHeight;
  }

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
