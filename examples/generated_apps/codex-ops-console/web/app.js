import { dom } from "./ops-dom.js";
import {
  appsUrl,
  appGoalsUrl,
  conversationMessagesUrl,
  fetchJson,
  internalConversationAppendStreamUrl,
  proposalsApplyUrl,
  selectedAppData,
  jobUrl,
  appConversationsUrl,
  conversationUrl,
} from "./ops-api.js";
import { createConversationController } from "./ops-conversations.js";
import { createJobController } from "./ops-jobs.js";
import {
  clearLearningSummary,
  clearAutonomySummary,
  describeJob,
  renderComposerMeta,
  renderDraftStatus,
  renderJobActivity,
  renderSessionStrip,
  renderLearningSummary,
  renderConversation,
  renderAutonomySummary,
  renderWorkspaceSummary,
  setJobMeta,
  setStatus,
  updateHeroState,
  updateProposalButton,
  updateSelectedAppCard,
} from "./ops-render.js";
import { getDraft, isAppendStreamConnected, loadSettings, normalizeBaseUrl, saveSettings, setDraft, state } from "./ops-store.js";

function persistSettings() {
  saveSettings(dom, state);
}

let conversationController;
let jobController;

function currentAppId() {
  return selectedAppData(dom)?.appId || "";
}

function setNavigationOpen(isOpen) {
  document.body.dataset.navOpen = isOpen ? "true" : "false";
  if (dom.navSheetScrim) {
    dom.navSheetScrim.hidden = !isOpen;
  }
}

function syncComposerMeta() {
  const app = selectedAppData(dom);
  const text = dom.requestTextInput.value;
  renderComposerMeta(dom, {
    hint: app
      ? `${app.title}에 이어서 보낼 지시입니다. 필요하면 현재 대화 맥락을 짧게 적고, 검증 방법을 마지막 줄에 남기세요.`
      : "먼저 앱을 고르면 이 입력창이 앱 레인에 연결됩니다.",
    count: text.length,
  });
}

function syncDraftStatus() {
  const app = selectedAppData(dom);
  if (!app) {
    renderDraftStatus(dom, "앱을 고르면 앱별 초안이 자동 저장됩니다.");
    return;
  }
  const text = dom.requestTextInput.value.trim();
  if (text) {
    renderDraftStatus(dom, `${app.title} · ${state.currentConversationId || "새 대화"} 초안을 이 기기에 저장 중입니다.`);
    return;
  }
  const savedDraft = getDraft(state, app.appId, state.currentConversationId);
  renderDraftStatus(
    dom,
    savedDraft ? `${app.title}에 저장된 초안이 있습니다. 필요하면 이어서 작성하세요.` : `${app.title}에 저장된 초안이 없습니다.`,
  );
}

function persistDraft() {
  const appId = currentAppId();
  if (!appId) {
    syncComposerMeta();
    return;
  }
  setDraft(state, appId, state.currentConversationId, dom.requestTextInput.value);
  syncComposerMeta();
  syncDraftStatus();
}

function restoreDraft() {
  const appId = currentAppId();
  dom.requestTextInput.value = appId ? getDraft(state, appId, state.currentConversationId) : "";
  syncComposerMeta();
  syncDraftStatus();
}

async function sendMessage() {
  const app = selectedAppData(dom);
  const messageText = dom.requestTextInput.value.trim();

  if (!app) {
    setStatus(dom, "대상 앱을 선택하세요.");
    return;
  }
  if (!messageText) {
    setStatus(dom, "메시지를 입력하세요.");
    return;
  }

  persistSettings();
  dom.sendRequestButton.disabled = true;
  state.latestProposalJobId = "";
  updateProposalButton(dom, state.latestProposalJobId);
  clearLearningSummary(dom, "작업이 끝나면 이번 수정의 판단 근거와 검증 결과가 여기에 정리됩니다.");
  setStatus(dom, "에이전트에 메시지를 전달하는 중...");
  setJobMeta(dom, `${app.title} · 메시지 전송 중`);

  try {
    const conversationId = await conversationController.ensureConversation();
    const payload = await fetchJson(dom, conversationMessagesUrl(conversationId), {
      method: "POST",
      body: JSON.stringify({
        message_text: messageText,
        source: "mobile-ops-console",
        execute_now: true,
      }),
    });

    state.currentConversationId = conversationId;
    state.currentJobId = payload.job.job_id;
    setDraft(state, app.appId, "", "");
    setDraft(state, app.appId, conversationId, "");
    dom.requestTextInput.value = "";
    syncComposerMeta();
    syncDraftStatus();
    renderConversation(dom, state, payload.conversation, persistSettings);
    setStatus(
      dom,
      [
        "메시지가 등록되었습니다.",
        `conversation_id: ${conversationId}`,
        `request_id: ${payload.request.request_id}`,
        `job_id: ${payload.job.job_id}`,
      ].join("\n"),
    );
    setJobMeta(dom, `QUEUED · ${payload.job.job_id}`);

    jobController.stopPolling();
    await jobController.pollCurrentState();
    jobController.ensurePollingForJob();
  } catch (error) {
    setStatus(dom, `메시지 전송에 실패했습니다.\n\n${error.message}`);
    setJobMeta(dom, "메시지 전송 실패");
    clearLearningSummary(dom, "메시지 전송이 실패해서 학습 로그가 생성되지 않았습니다.");
  } finally {
    dom.sendRequestButton.disabled = false;
  }
}

async function applyProposal() {
  if (!state.latestProposalJobId) {
    setStatus(dom, "적용할 proposal이 없습니다.");
    return;
  }

  dom.applyProposalButton.disabled = true;
  setJobMeta(dom, `APPLYING · ${state.latestProposalJobId}`);

  try {
    const payload = await fetchJson(dom, proposalsApplyUrl(state.latestProposalJobId), {
      method: "POST",
    });
    state.latestProposalJobId = "";
    updateProposalButton(dom, state.latestProposalJobId);
    setStatus(
      dom,
      [
        "proposal이 적용되었습니다.",
        `job_id: ${payload.job_id}`,
        `branch: ${payload.branch_name}`,
        `commit: ${payload.head_commit}`,
      ].join("\n"),
    );
    setJobMeta(dom, `APPLIED · ${payload.job_id}`);
    renderLearningSummary(
      dom,
      payload.decision_summary || {},
      `제안 적용 · ${payload.title || payload.job_id}`,
      payload.status || "APPLIED",
    );
    if (state.currentConversationId) {
      await conversationController.fetchConversation(state.currentConversationId);
    }
  } catch (error) {
    setStatus(dom, `proposal 적용에 실패했습니다.\n\n${error.message}`);
    setJobMeta(dom, "proposal 적용 실패");
    updateProposalButton(dom, state.latestProposalJobId);
    clearLearningSummary(dom, "proposal 적용이 실패해서 새 학습 로그를 표시하지 못했습니다.");
  }
}

function openSelectedApp() {
  const app = selectedAppData(dom);
  if (!app || !app.deploymentUrl) {
    setStatus(dom, "선택한 앱의 deployment_url이 등록되지 않았습니다.");
    return;
  }
  window.open(app.deploymentUrl, "_blank", "noopener,noreferrer");
}

function wireInstallPrompt() {
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    state.deferredInstallPrompt = event;
    dom.installButton.hidden = false;
  });

  dom.installButton.addEventListener("click", async () => {
    if (!state.deferredInstallPrompt) {
      return;
    }
    state.deferredInstallPrompt.prompt();
    await state.deferredInstallPrompt.userChoice;
    state.deferredInstallPrompt = null;
    dom.installButton.hidden = true;
  });
}

function wireServiceWorker() {
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register("./service-worker.js").catch(() => {});
    });
  }
}

function wireEvents() {
  dom.navSheetToggle?.addEventListener("click", () => setNavigationOpen(true));
  dom.navSheetClose?.addEventListener("click", () => setNavigationOpen(false));
  dom.navSheetScrim?.addEventListener("click", () => setNavigationOpen(false));
  window.addEventListener("resize", () => {
    if (window.innerWidth > 860) {
      setNavigationOpen(false);
    }
  });
  dom.appSelect.addEventListener("change", async () => {
    await conversationController.handleAppChange();
    setNavigationOpen(false);
  });
  dom.autoOpenInput.addEventListener("change", persistSettings);
  dom.refreshAppsButton.addEventListener("click", async () => {
    await conversationController.loadApps();
    setNavigationOpen(false);
  });
  dom.newConversationButton.addEventListener("click", async () => {
    await conversationController.createConversation();
    setNavigationOpen(false);
  });
  dom.sendRequestButton.addEventListener("click", sendMessage);
  dom.openAppButton.addEventListener("click", openSelectedApp);
  dom.applyProposalButton.addEventListener("click", applyProposal);
  dom.requestTextInput.addEventListener("input", persistDraft);
  dom.requestTextInput.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  });
  dom.conversationList.addEventListener("click", async (event) => {
    const button = event.target.closest("[data-conversation-id]");
    if (!button) {
      return;
    }
    state.savedConversationId = button.dataset.conversationId || "";
    await conversationController.handleConversationChange();
    setNavigationOpen(false);
  });
}

function initControllers() {
  jobController = createJobController({
    describeJob,
    dom,
    fetchConversation: (...args) => conversationController.fetchConversation(...args),
    fetchJson,
    jobUrl,
    refreshGoalSummary: () => conversationController.refreshGoalSummary(),
    renderLearningSummary,
    renderJobActivity,
    setJobMeta,
    setStatus,
    state,
    isAppendStreamConnected,
    updateProposalButton,
  });

  conversationController = createConversationController({
    appConversationsUrl,
    appGoalsUrl,
    appsUrl,
    clearAutonomySummary,
    clearLearningSummary,
    dom,
    ensurePollingForJob: jobController.ensurePollingForJob,
    fetchJson,
    internalConversationAppendStreamUrl,
    normalizeBaseUrl,
    persistSettings,
    renderAutonomySummary,
    renderConversation,
    renderSessionStrip,
    selectedAppData,
    setJobMeta,
    setStatus,
    state,
    stopPolling: jobController.stopPolling,
    syncLatestJob: jobController.syncLatestJob,
    updateProposalButton,
    updateSelectedAppCard,
    updateHeroState,
    renderWorkspaceSummary,
    restoreDraft,
    syncDraftStatus,
    conversationUrl,
  });
}

function init() {
  setNavigationOpen(false);
  loadSettings(dom, state);
  updateSelectedAppCard(dom, selectedAppData(dom));
  updateProposalButton(dom, state.latestProposalJobId);
  updateHeroState(dom, {
    appName: "앱을 불러오는 중입니다.",
    conversationState: "대화 준비 전",
    jobState: "IDLE",
  });
  renderWorkspaceSummary(dom, "앱 목록과 최근 대화를 불러오면 현재 세션 맥락이 여기에 정리됩니다.");
  clearAutonomySummary(dom);
  clearLearningSummary(dom);
  syncComposerMeta();
  syncDraftStatus();
  initControllers();
  wireInstallPrompt();
  wireServiceWorker();
  wireEvents();
  conversationController.loadApps();
}

init();
