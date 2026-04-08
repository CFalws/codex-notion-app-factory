const backendInput = document.getElementById("backend-url");
const apiKeyInput = document.getElementById("api-key");
const appSelect = document.getElementById("app-select");
const refreshAppsButton = document.getElementById("refresh-apps");
const requestTitleInput = document.getElementById("request-title");
const requestTextInput = document.getElementById("request-text");
const sendRequestButton = document.getElementById("send-request");
const openAppButton = document.getElementById("open-app");
const applyProposalButton = document.getElementById("apply-proposal");
const autoOpenInput = document.getElementById("auto-open-app");
const selectedAppUrl = document.getElementById("selected-app-url");
const statusOutput = document.getElementById("status-output");
const jobMeta = document.getElementById("job-meta");
const installButton = document.getElementById("install-button");

const STORAGE_KEY = "codex-ops-console";
let deferredInstallPrompt = null;
let pollingTimer = null;
let latestProposalJobId = "";

function saveSettings() {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      backendUrl: backendInput.value.trim(),
      apiKey: apiKeyInput.value.trim(),
      selectedAppId: appSelect.value,
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
    backendInput.value = payload.backendUrl || "";
    apiKeyInput.value = payload.apiKey || "";
    autoOpenInput.checked = Boolean(payload.autoOpen);
    appSelect.dataset.savedAppId = payload.selectedAppId || "";
  } catch (_) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function normalizeBaseUrl() {
  return backendInput.value.trim().replace(/\/+$/, "");
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
    `title: ${payload.title}`,
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

async function loadApps() {
  const baseUrl = normalizeBaseUrl();
  if (!baseUrl) {
    setStatus("런타임 URL을 먼저 입력하세요.");
    return;
  }

  saveSettings();
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
    setJobMeta("앱을 선택하고 바로 에이전트 작업을 실행할 수 있습니다.");
  } catch (error) {
    setStatus(`앱 목록을 불러오지 못했습니다.\n\n${error.message}`);
  }
}

async function pollJob(jobId) {
  const baseUrl = normalizeBaseUrl();
  if (!baseUrl) {
    return;
  }

  try {
    const payload = await fetchJson(`${baseUrl}/api/jobs/${jobId}`);
    setStatus(describeJob(payload));
    setJobMeta(`${payload.status.toUpperCase()} · ${payload.job_id}`);
    latestProposalJobId = payload.proposal ? payload.proposal.job_id : "";
    updateProposalButton();

    if (payload.status === "completed" || payload.status === "failed") {
      clearInterval(pollingTimer);
      pollingTimer = null;
      updateSelectedAppCard();
      if (payload.status === "completed" && autoOpenInput.checked) {
        openAppButton.focus();
      }
    }
  } catch (error) {
    clearInterval(pollingTimer);
    pollingTimer = null;
    setStatus(`작업 상태를 가져오지 못했습니다.\n\n${error.message}`);
    setJobMeta("작업 상태 조회 실패");
    latestProposalJobId = "";
    updateProposalButton();
  }
}

async function sendRequest() {
  const baseUrl = normalizeBaseUrl();
  const app = selectedAppData();
  const title = requestTitleInput.value.trim();
  const requestText = requestTextInput.value.trim();

  if (!baseUrl) {
    setStatus("런타임 URL을 입력하세요.");
    return;
  }
  if (!apiKeyInput.value.trim()) {
    setStatus("API key를 입력하세요.");
    return;
  }
  if (!app) {
    setStatus("대상 앱을 선택하세요.");
    return;
  }
  if (!title || !requestText) {
    setStatus("요청 제목과 내용을 모두 입력하세요.");
    return;
  }

  saveSettings();
  sendRequestButton.disabled = true;
  latestProposalJobId = "";
  updateProposalButton();
  setStatus("에이전트 작업을 등록하는 중...");
  setJobMeta(`${app.title} · 요청 전송 중`);

  try {
    const payload = await fetchJson(`${baseUrl}/api/requests`, {
      method: "POST",
      body: JSON.stringify({
        app_id: app.appId,
        title,
        request_text: requestText,
        source: "mobile-ops-console",
        execute_now: true,
      }),
    });

    requestTitleInput.value = "";
    requestTextInput.value = "";
    setStatus(
      [
        "요청이 등록되었습니다.",
        `request_id: ${payload.request.request_id}`,
        `job_id: ${payload.job.job_id}`,
      ].join("\n"),
    );
    setJobMeta(`QUEUED · ${payload.job.job_id}`);

    if (pollingTimer) {
      clearInterval(pollingTimer);
    }
    await pollJob(payload.job.job_id);
    pollingTimer = setInterval(() => {
      pollJob(payload.job.job_id);
    }, 3000);
  } catch (error) {
    setStatus(`요청 전송에 실패했습니다.\n\n${error.message}`);
    setJobMeta("요청 전송 실패");
  } finally {
    sendRequestButton.disabled = false;
  }
}

async function applyProposal() {
  const baseUrl = normalizeBaseUrl();
  if (!baseUrl) {
    setStatus("런타임 URL을 입력하세요.");
    return;
  }
  if (!latestProposalJobId) {
    setStatus("적용할 proposal이 없습니다.");
    return;
  }

  applyProposalButton.disabled = true;
  setJobMeta(`APPLYING · ${latestProposalJobId}`);

  try {
    const payload = await fetchJson(`${baseUrl}/api/proposals/${latestProposalJobId}/apply`, {
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
  } catch (error) {
    setStatus(`proposal 적용에 실패했습니다.\n\n${error.message}`);
    setJobMeta("proposal 적용 실패");
    updateProposalButton();
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

backendInput.addEventListener("change", saveSettings);
apiKeyInput.addEventListener("change", saveSettings);
appSelect.addEventListener("change", () => {
  updateSelectedAppCard();
  saveSettings();
});
autoOpenInput.addEventListener("change", saveSettings);
refreshAppsButton.addEventListener("click", loadApps);
sendRequestButton.addEventListener("click", sendRequest);
openAppButton.addEventListener("click", openSelectedApp);
applyProposalButton.addEventListener("click", applyProposal);

loadSettings();
updateSelectedAppCard();
updateProposalButton();
if (backendInput.value) {
  loadApps();
}
