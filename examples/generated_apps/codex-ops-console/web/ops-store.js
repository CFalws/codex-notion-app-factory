import { FIXED_RUNTIME_URL, STORAGE_KEY } from "./ops-constants.js";

export const state = {
  deferredInstallPrompt: null,
  pollingTimer: null,
  latestProposalJobId: "",
  currentConversationId: "",
  currentJobId: "",
  conversationCache: null,
};

export function normalizeBaseUrl() {
  return FIXED_RUNTIME_URL.replace(/\/+$/, "");
}

export function saveSettings(dom, currentState) {
  const selectedConversationId =
    currentState.currentConversationId ||
    dom.conversationSelect.value ||
    dom.conversationSelect.dataset.savedConversationId ||
    "";

  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      selectedAppId: dom.appSelect.value,
      selectedConversationId,
      autoOpen: dom.autoOpenInput.checked,
    }),
  );
}

export function loadSettings(dom) {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return;
  }

  try {
    const payload = JSON.parse(raw);
    dom.autoOpenInput.checked = Boolean(payload.autoOpen);
    dom.appSelect.dataset.savedAppId = payload.selectedAppId || "";
    dom.conversationSelect.dataset.savedConversationId = payload.selectedConversationId || "";
  } catch (_) {
    localStorage.removeItem(STORAGE_KEY);
  }
}
