import { dom } from "./ops-dom.js";
import {
  appsUrl,
  conversationMessagesUrl,
  fetchJson,
  proposalsApplyUrl,
  selectedAppData,
  jobUrl,
  appConversationsUrl,
  conversationUrl,
} from "./ops-api.js";
import { FIXED_RUNTIME_URL } from "./ops-constants.js";
import { createConversationController } from "./ops-conversations.js";
import { createJobController } from "./ops-jobs.js";
import {
  clearLearningSummary,
  describeJob,
  renderLearningSummary,
  renderConversation,
  setJobMeta,
  setStatus,
  updateProposalButton,
  updateSelectedAppCard,
} from "./ops-render.js";
import { loadSettings, normalizeBaseUrl, saveSettings, state } from "./ops-store.js";

function persistSettings() {
  saveSettings(dom, state);
}

let conversationController;
let jobController;

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
    dom.requestTextInput.value = "";
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
  dom.appSelect.addEventListener("change", conversationController.handleAppChange);
  dom.conversationSelect.addEventListener("change", conversationController.handleConversationChange);
  dom.autoOpenInput.addEventListener("change", persistSettings);
  dom.refreshAppsButton.addEventListener("click", conversationController.loadApps);
  dom.newConversationButton.addEventListener("click", conversationController.createConversation);
  dom.sendRequestButton.addEventListener("click", sendMessage);
  dom.openAppButton.addEventListener("click", openSelectedApp);
  dom.applyProposalButton.addEventListener("click", applyProposal);
}

function initControllers() {
  jobController = createJobController({
    describeJob,
    dom,
    fetchConversation: (...args) => conversationController.fetchConversation(...args),
    fetchJson,
    jobUrl,
    renderLearningSummary,
    setJobMeta,
    setStatus,
    state,
    updateProposalButton,
  });

  conversationController = createConversationController({
    appConversationsUrl,
    appsUrl,
    clearLearningSummary,
    dom,
    ensurePollingForJob: jobController.ensurePollingForJob,
    fetchJson,
    normalizeBaseUrl,
    persistSettings,
    renderConversation,
    selectedAppData,
    setJobMeta,
    setStatus,
    state,
    stopPolling: jobController.stopPolling,
    syncLatestJob: jobController.syncLatestJob,
    updateProposalButton,
    updateSelectedAppCard,
    conversationUrl,
  });
}

function init() {
  loadSettings(dom);
  dom.backendInput.value = FIXED_RUNTIME_URL;
  updateSelectedAppCard(dom, selectedAppData(dom));
  updateProposalButton(dom, state.latestProposalJobId);
  clearLearningSummary(dom);
  initControllers();
  wireInstallPrompt();
  wireServiceWorker();
  wireEvents();
  conversationController.loadApps();
}

init();
