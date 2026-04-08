const backendInput = document.getElementById("backend-url");
const apiKeyInput = document.getElementById("api-key");
const appSelect = document.getElementById("app-select");
const refreshAppsButton = document.getElementById("refresh-apps");
const conversationSelect = document.getElementById("conversation-select");
const newConversationButton = document.getElementById("new-conversation");
const conversationMeta = document.getElementById("conversation-meta");
const conversationTimeline = document.getElementById("conversation-timeline");
const requestTextInput = document.getElementById("request-text");
const sendRequestButton = document.getElementById("send-request");
const openAppButton = document.getElementById("open-app");
const applyProposalButton = document.getElementById("apply-proposal");
const autoOpenInput = document.getElementById("auto-open-app");
const selectedAppUrl = document.getElementById("selected-app-url");
const statusOutput = document.getElementById("status-output");
const jobMeta = document.getElementById("job-meta");
const installButton = document.getElementById("install-button");
const learningSummary = document.getElementById("learning-summary");
const learningMeta = document.getElementById("learning-meta");

const STORAGE_KEY = "codex-ops-console";
const FIXED_RUNTIME_URL = "https://34.40.112.33";
const DECISION_FIELDS = [
  ["goal", "문제"],
  ["system_area", "영향 범위"],
  ["decision", "선택"],
  ["why", "왜 이 방식인가"],
  ["tradeoff", "트레이드오프"],
  ["issue_encountered", "실제 문제"],
  ["verification", "검증"],
  ["follow_up", "다음 단계"],
];

let deferredInstallPrompt = null;
let pollingTimer = null;
let latestProposalJobId = "";
let currentConversationId = "";
let currentJobId = "";
let conversationCache = null;

function saveSettings() {
  const selectedConversationId =
    currentConversationId ||
    conversationSelect.value ||
    conversationSelect.dataset.savedConversationId ||
    "";

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      apiKey: apiKeyInput.value.trim(),
      selectedAppId: appSelect.value,
      selectedConversationId,
      autoOpen: autoOpenInput.checked,
    }),
  );
}

function loadSettings() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return;
  }

  try {
    const payload = JSON.parse(raw);
    apiKeyInput.value = payload.apiKey || "";
    autoOpenInput.checked = Boolean(payload.autoOpen);
    appSelect.dataset.savedAppId = payload.selectedAppId || "";
    conversationSelect.dataset.savedConversationId = payload.selectedConversationId || "";
  } catch (_) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function normalizeBaseUrl() {
  return FIXED_RUNTIME_URL.replace(/\/+$/, "");
}

function setStatus(message) {
  statusOutput.textContent = message;
}

function setJobMeta(message) {
  jobMeta.textContent = message;
}

function requestHeaders(extraHeaders = {}) {
  const headers = {
    "Content-Type": "application/json",
    ...extraHeaders,
  };
  const apiKey = apiKeyInput.value.trim();
  if (apiKey) {
    headers["X-API-Key"] = apiKey;
  }
  return headers;
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: requestHeaders(options.headers || {}),
    ...options,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }

  return response.json();
}

function selectedAppData() {
  const option = appSelect.selectedOptions[0];
  if (!option) {
    return null;
  }

  return {
    appId: option.value,
    title: option.dataset.title || option.value,
    deploymentUrl: option.dataset.deploymentUrl || "",
  };
}

function updateSelectedAppCard() {
  const app = selectedAppData();
  const hasDeployment = Boolean(app && app.deploymentUrl);
  openAppButton.disabled = !hasDeployment;

  if (!app) {
    selectedAppUrl.textContent = "앱을 선택하면 여기에서 바로 열 수 있습니다.";
    return;
  }

  selectedAppUrl.textContent = hasDeployment
    ? app.deploymentUrl
    : "deployment_url이 아직 등록되지 않았습니다.";
}

function updateProposalButton() {
  applyProposalButton.disabled = !latestProposalJobId;
}

function describeJob(payload) {
  const lines = [
    `job_id: ${payload.job_id}`,
    `status: ${payload.status}`,
    payload.title ? `label: ${payload.title}` : "",
    `created_at: ${payload.created_at}`,
    payload.started_at ? `started_at: ${payload.started_at}` : "",
    payload.completed_at ? `completed_at: ${payload.completed_at}` : "",
    payload.error ? `error: ${payload.error}` : "",
    payload.proposal ? `proposal_branch: ${payload.proposal.branch_name}` : "",
    payload.proposal ? `proposal_status: ${payload.proposal.status}` : "",
    payload.result_summary ? `\n${payload.result_summary}` : "",
  ].filter(Boolean);
  return lines.join("\n");
}

function clearLearningSummary(message = "작업이 끝나면 여기에서 설계 판단과 검증 내용을 바로 읽을 수 있습니다.") {
  learningMeta.textContent = "아직 기록된 학습 로그가 없습니다.";
  learningSummary.innerHTML = `<p class="learning-empty">${message}</p>`;
}

function renderLearningSummary(summary, heading, status = "RECORDED") {
  const cards = [];
  if (summary) {
    for (const [key, label] of DECISION_FIELDS) {
      const value = typeof summary[key] === "string" ? summary[key].trim() : "";
      if (!value) {
        continue;
      }
      cards.push(`
        <article class="learning-card">
          <p class="learning-label">${label}</p>
          <p class="learning-value">${value}</p>
        </article>
      `);
    }
  }

  if (!cards.length) {
    clearLearningSummary("이번 작업에는 아직 구조화된 학습 로그가 없습니다.");
    return;
  }

  learningMeta.textContent = `${status} · ${heading}`;
  learningSummary.innerHTML = cards.join("");
}

function renderConversation(conversation) {
  conversationCache = conversation;
  currentConversationId = conversation ? conversation.conversation_id : "";
  saveSettings();

  if (!conversation) {
    conversationMeta.textContent = "아직 대화 세션이 없습니다.";
    conversationTimeline.innerHTML = '<p class="timeline-empty">새 대화를 만들면 요청과 이벤트가 여기 쌓입니다.</p>';
    return;
  }

  const messages = Array.isArray(conversation.messages) ? conversation.messages : [];
  const events = Array.isArray(conversation.events) ? conversation.events : [];
  const items = [
    ...messages.map((item) => ({ ...item, kind: "message", sortAt: item.created_at })),
    ...events.map((item) => ({ ...item, kind: "event", sortAt: item.created_at })),
  ].sort((a, b) => (a.sortAt < b.sortAt ? -1 : 1));

  conversationMeta.textContent = `${conversation.title} · ${items.length} items`;

  if (!items.length) {
    conversationTimeline.innerHTML = '<p class="timeline-empty">아직 메시지가 없습니다.</p>';
    return;
  }

  conversationTimeline.innerHTML = items
    .map((item) => {
      if (item.kind === "event") {
        return `
          <article class="timeline-item event ${item.status || "info"}">
            <p class="timeline-kind">${item.type}</p>
            <p class="timeline-body">${item.body}</p>
            <p class="timeline-meta">${item.created_at}${item.job_id ? ` · ${item.job_id}` : ""}</p>
          </article>
        `;
      }

      return `
        <article class="timeline-item message ${item.role || "assistant"}">
          <p class="timeline-kind">${item.role === "user" ? "사용자" : "에이전트"}${item.role !== "user" && item.title ? ` · ${item.title}` : ""}</p>
          <p class="timeline-body">${item.body}</p>
          <p class="timeline-meta">${item.created_at}${item.job_id ? ` · ${item.job_id}` : ""}</p>
        </article>
      `;
    })
    .join("");

  const assistantResult = [...messages].reverse().find((item) => item.role === "assistant");
  const decisionSummary = assistantResult && assistantResult.metadata ? assistantResult.metadata.decision_summary : null;
  if (decisionSummary) {
    renderLearningSummary(decisionSummary, assistantResult.title || "이번 작업에서 배운 점", assistantResult.metadata?.status || "RECORDED");
  }
}

async function loadApps() {
  const baseUrl = normalizeBaseUrl();
  setStatus("앱 목록을 불러오는 중...");

  try {
    const apps = await fetchJson(`${baseUrl}/api/apps`);
    const previousAppId = appSelect.value || appSelect.dataset.savedAppId || "";
    appSelect.innerHTML = "";

    for (const app of apps) {
      const option = document.createElement("option");
      option.value = app.app_id;
      option.textContent = `${app.title} (${app.app_id})`;
      option.dataset.deploymentUrl = app.deployment_url || "";
      option.dataset.title = app.title || app.app_id;
      appSelect.append(option);
    }

    if (!apps.length) {
      updateSelectedAppCard();
      setStatus("등록된 앱이 없습니다. 서버의 state/registry/apps를 확인하세요.");
      setJobMeta("앱이 등록되면 여기에서 작업 상태를 추적합니다.");
      renderConversation(null);
      clearLearningSummary();
      return;
    }

    if (previousAppId) {
      appSelect.value = previousAppId;
    }
    if (!appSelect.value) {
      appSelect.selectedIndex = 0;
    }

    updateSelectedAppCard();
    saveSettings();
    setStatus(`앱 ${apps.length}개를 불러왔습니다.`);
    setJobMeta("앱과 대화를 선택하고 에이전트와 계속 대화할 수 있습니다.");
    await loadConversations();
  } catch (error) {
    setStatus(`앱 목록을 불러오지 못했습니다.\n\n${error.message}`);
  }
}

async function loadConversations() {
  const baseUrl = normalizeBaseUrl();
  const app = selectedAppData();
  const preferredConversationId =
    currentConversationId ||
    conversationSelect.value ||
    conversationSelect.dataset.savedConversationId ||
    "";

  conversationSelect.innerHTML = "";
  conversationCache = null;

  if (!app) {
    currentConversationId = "";
    renderConversation(null);
    return;
  }

  try {
    const conversations = await fetchJson(`${baseUrl}/api/apps/${app.appId}/conversations`);

    for (const conversation of conversations) {
      const option = document.createElement("option");
      option.value = conversation.conversation_id;
      option.textContent = `${conversation.title} (${new Date(conversation.updated_at).toLocaleString()})`;
      conversationSelect.append(option);
    }

    if (preferredConversationId) {
      conversationSelect.value = preferredConversationId;
    }
    if (!conversationSelect.value && conversations.length) {
      conversationSelect.selectedIndex = 0;
    }

    if (conversationSelect.value) {
      conversationSelect.dataset.savedConversationId = conversationSelect.value;
      await fetchConversation(conversationSelect.value);
    } else {
      currentConversationId = "";
      currentJobId = "";
      renderConversation(null);
      conversationMeta.textContent = "이 앱에는 아직 대화가 없습니다.";
    }
  } catch (error) {
    currentConversationId = "";
    currentJobId = "";
    renderConversation(null);
    conversationMeta.textContent = `대화를 불러오지 못했습니다: ${error.message}`;
  }
}

async function fetchConversation(conversationId, options = {}) {
  const { syncJob = true } = options;
  const baseUrl = normalizeBaseUrl();
  if (!conversationId) {
    renderConversation(null);
    return;
  }
  const conversation = await fetchJson(`${baseUrl}/api/conversations/${conversationId}`);
  currentConversationId = conversation.conversation_id;
  conversationSelect.value = currentConversationId;
  conversationSelect.dataset.savedConversationId = currentConversationId;
  renderConversation(conversation);

  if (!syncJob) {
    return;
  }

  if (conversation.latest_job_id) {
    currentJobId = conversation.latest_job_id;
    const payload = await syncLatestJob();
    if (payload && payload.status !== "completed" && payload.status !== "failed") {
      ensurePollingForJob();
    } else {
      currentJobId = "";
    }
  } else {
    currentJobId = "";
    latestProposalJobId = "";
    updateProposalButton();
  }
}

async function ensureConversation() {
  if (currentConversationId) {
    return currentConversationId;
  }

  const app = selectedAppData();
  if (!app) {
    throw new Error("대상 앱을 먼저 선택하세요.");
  }

  const payload = await fetchJson(`${normalizeBaseUrl()}/api/conversations`, {
    method: "POST",
    body: JSON.stringify({
      app_id: app.appId,
      source: "mobile-ops-console",
    }),
  });
  await loadConversations();
  currentConversationId = payload.conversation_id;
  conversationSelect.value = currentConversationId;
  await fetchConversation(currentConversationId);
  return currentConversationId;
}

async function createConversation() {
  try {
    await ensureConversation();
    setStatus("새 대화 세션을 만들었습니다.");
    setJobMeta(`CONVERSATION · ${currentConversationId}`);
  } catch (error) {
    setStatus(`새 대화 생성에 실패했습니다.\n\n${error.message}`);
  }
}

async function syncLatestJob() {
  if (!currentJobId) {
    return null;
  }

  const payload = await fetchJson(`${normalizeBaseUrl()}/api/jobs/${currentJobId}`);
  setStatus(describeJob(payload));
  setJobMeta(`${payload.status.toUpperCase()} · ${payload.job_id}`);
  latestProposalJobId = payload.proposal ? payload.proposal.job_id : "";
  updateProposalButton();

  if (payload.decision_summary) {
    renderLearningSummary(payload.decision_summary, payload.title || "이번 작업에서 배운 점", payload.status || "RECORDED");
  }

  return payload;
}

function ensurePollingForJob() {
  if (!currentJobId || pollingTimer) {
    return;
  }
  pollingTimer = setInterval(() => {
    pollCurrentState();
  }, 3000);
}

async function pollCurrentState() {
  try {
    const payload = await syncLatestJob();

    if (currentConversationId) {
      try {
        await fetchConversation(currentConversationId, { syncJob: false });
      } catch (_) {
        // Keep the last rendered conversation and let the job panel carry the visible error if needed.
      }
    }

    if (!payload) {
      return;
    }

    if (payload.status === "completed" || payload.status === "failed") {
      if (payload.status === "completed" && autoOpenInput.checked) {
        openAppButton.focus();
      }
      currentJobId = "";
      if (pollingTimer) {
        clearInterval(pollingTimer);
        pollingTimer = null;
      }
      if (currentConversationId) {
        await fetchConversation(currentConversationId, { syncJob: false });
      }
    }
  } catch (error) {
    setStatus(`작업 상태를 가져오지 못했습니다.\n\n${error.message}`);
    setJobMeta("작업 상태 조회 실패");
  }
}

async function sendMessage() {
  const app = selectedAppData();
  const messageText = requestTextInput.value.trim();

  if (!apiKeyInput.value.trim()) {
    setStatus("API key를 입력하세요.");
    return;
  }
  if (!app) {
    setStatus("대상 앱을 선택하세요.");
    return;
  }
  if (!messageText) {
    setStatus("메시지를 입력하세요.");
    return;
  }

  saveSettings();
  sendRequestButton.disabled = true;
  latestProposalJobId = "";
  updateProposalButton();
  clearLearningSummary("작업이 끝나면 이번 수정의 판단 근거와 검증 결과가 여기에 정리됩니다.");
  setStatus("에이전트에 메시지를 전달하는 중...");
  setJobMeta(`${app.title} · 메시지 전송 중`);

  try {
    const conversationId = await ensureConversation();
    const payload = await fetchJson(`${normalizeBaseUrl()}/api/conversations/${conversationId}/messages`, {
      method: "POST",
      body: JSON.stringify({
        message_text: messageText,
        source: "mobile-ops-console",
        execute_now: true,
      }),
    });

    currentConversationId = conversationId;
    currentJobId = payload.job.job_id;
    requestTextInput.value = "";
    renderConversation(payload.conversation);
    setStatus(
      [
        "메시지가 등록되었습니다.",
        `conversation_id: ${conversationId}`,
        `request_id: ${payload.request.request_id}`,
        `job_id: ${payload.job.job_id}`,
      ].join("\n"),
    );
    setJobMeta(`QUEUED · ${payload.job.job_id}`);

    if (pollingTimer) {
      clearInterval(pollingTimer);
    }
    await pollCurrentState();
    ensurePollingForJob();
  } catch (error) {
    setStatus(`메시지 전송에 실패했습니다.\n\n${error.message}`);
    setJobMeta("메시지 전송 실패");
    clearLearningSummary("메시지 전송이 실패해서 학습 로그가 생성되지 않았습니다.");
  } finally {
    sendRequestButton.disabled = false;
  }
}

async function applyProposal() {
  if (!latestProposalJobId) {
    setStatus("적용할 proposal이 없습니다.");
    return;
  }

  applyProposalButton.disabled = true;
  setJobMeta(`APPLYING · ${latestProposalJobId}`);

  try {
    const payload = await fetchJson(`${normalizeBaseUrl()}/api/proposals/${latestProposalJobId}/apply`, {
      method: "POST",
    });
    latestProposalJobId = "";
    updateProposalButton();
    setStatus(
      [
        "proposal이 적용되었습니다.",
        `job_id: ${payload.job_id}`,
        `branch: ${payload.branch_name}`,
        `commit: ${payload.head_commit}`,
      ].join("\n"),
    );
    setJobMeta(`APPLIED · ${payload.job_id}`);
    renderLearningSummary(payload.decision_summary || {}, `제안 적용 · ${payload.title || payload.job_id}`, payload.status || "APPLIED");
    if (currentConversationId) {
      await fetchConversation(currentConversationId);
    }
  } catch (error) {
    setStatus(`proposal 적용에 실패했습니다.\n\n${error.message}`);
    setJobMeta("proposal 적용 실패");
    updateProposalButton();
    clearLearningSummary("proposal 적용이 실패해서 새 학습 로그를 표시하지 못했습니다.");
  }
}

function openSelectedApp() {
  const app = selectedAppData();
  if (!app || !app.deploymentUrl) {
    setStatus("선택한 앱의 deployment_url이 등록되지 않았습니다.");
    return;
  }
  window.open(app.deploymentUrl, "_blank", "noopener,noreferrer");
}

window.addEventListener("beforeinstallprompt", (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  installButton.hidden = false;
});

installButton.addEventListener("click", async () => {
  if (!deferredInstallPrompt) {
    return;
  }
  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  installButton.hidden = true;
});

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("./service-worker.js").catch(() => {});
  });
}

apiKeyInput.addEventListener("change", saveSettings);
appSelect.addEventListener("change", async () => {
  updateSelectedAppCard();
  conversationSelect.dataset.savedConversationId = "";
  await loadConversations();
  saveSettings();
});
conversationSelect.addEventListener("change", async () => {
  if (conversationSelect.value) {
    await fetchConversation(conversationSelect.value);
  }
  saveSettings();
});
autoOpenInput.addEventListener("change", saveSettings);
refreshAppsButton.addEventListener("click", loadApps);
newConversationButton.addEventListener("click", createConversation);
sendRequestButton.addEventListener("click", sendMessage);
openAppButton.addEventListener("click", openSelectedApp);
applyProposalButton.addEventListener("click", applyProposal);

loadSettings();
backendInput.value = FIXED_RUNTIME_URL;
updateSelectedAppCard();
updateProposalButton();
clearLearningSummary();
loadApps();
