import { DECISION_FIELDS, UX_REVIEW_FIELDS } from "./ops-constants.js";

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

export function renderComposerMeta(dom, { hint = "", count = 0 }) {
  if (hint) {
    dom.composerHint.textContent = hint;
  }
  dom.composerCount.textContent = `${count}자`;
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

export function renderLearningSummary(dom, summary, heading, status = "RECORDED", uxReview = null) {
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
  const uxCards = renderCards(UX_REVIEW_FIELDS, uxReview);

  if (!decisionCards.length && !uxCards.length) {
    clearLearningSummary(dom, "이번 작업에는 아직 구조화된 학습 로그가 없습니다.");
    return;
  }

  dom.learningMeta.textContent = `${status} · ${heading}`;
  dom.learningSummary.innerHTML = [
    decisionCards.length
      ? `<section class="learning-group"><p class="learning-group-head">설계 판단</p>${decisionCards.join("")}</section>`
      : "",
    uxCards.length
      ? `<section class="learning-group"><p class="learning-group-head">UX 해석</p>${uxCards.join("")}</section>`
      : "",
  ]
    .filter(Boolean)
    .join("");
}

export function renderConversation(dom, currentState, conversation, onPersist) {
  currentState.conversationCache = conversation;
  currentState.currentConversationId = conversation ? conversation.conversation_id : "";
  onPersist();

  if (!conversation) {
    dom.conversationMeta.textContent = "아직 대화 세션이 없습니다.";
    dom.conversationTimeline.innerHTML = '<p class="timeline-empty">새 대화를 만들면 요청과 이벤트가 여기 쌓입니다.</p>';
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
  ].sort((a, b) => (a.sortAt < b.sortAt ? -1 : 1));

  dom.conversationMeta.textContent = `${messages.length} messages · ${events.length} events`;
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
            <article class="timeline-item event ${item.status || "info"}">
            <p class="timeline-kind">${escapeHtml(eventLabel(item.type))}</p>
            <p class="timeline-body">${escapeHtml(simplifyText(item.body))}</p>
            <p class="timeline-meta">${item.created_at}${item.job_id ? ` · ${item.job_id}` : ""}</p>
          </article>
        `;
      }

      return `
        <article class="timeline-item message ${item.role || "assistant"}">
          <p class="timeline-kind">${item.role === "user" ? "사용자" : "에이전트"}</p>
          <p class="timeline-body">${escapeHtml(simplifyText(item.body))}</p>
          <p class="timeline-meta">${item.created_at}${item.job_id ? ` · ${item.job_id}` : ""}</p>
        </article>
      `;
    })
    .join("");
  dom.conversationTimeline.scrollTop = dom.conversationTimeline.scrollHeight;

  renderJobActivity(dom, conversation, currentState.currentJobId || conversation.latest_job_id || "");

  const assistantResult = [...messages].reverse().find((item) => item.role === "assistant");
  const decisionSummary = assistantResult && assistantResult.metadata ? assistantResult.metadata.decision_summary : null;
  const uxReview = assistantResult && assistantResult.metadata ? assistantResult.metadata.ux_review : null;
  if (decisionSummary || uxReview) {
    renderLearningSummary(
      dom,
      decisionSummary,
      assistantResult.title || "이번 작업에서 배운 점",
      assistantResult.metadata?.status || "RECORDED",
      uxReview,
    );
  }
}
