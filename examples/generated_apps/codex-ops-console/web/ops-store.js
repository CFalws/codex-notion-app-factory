import { DRAFTS_KEY, FIXED_RUNTIME_URL, STORAGE_KEY } from "./ops-constants.js";

export const state = {
  deferredInstallPrompt: null,
  pollingTimer: null,
  latestProposalJobId: "",
  currentConversationId: "",
  currentJobId: "",
  savedAppId: "",
  savedConversationId: "",
  conversationCache: null,
  draftCache: {},
  pendingAttachmentPreviews: [],
  pendingOutgoing: {
    conversationId: "",
    body: "",
    createdAt: "",
    assistantCreatedAt: "",
    baselineAppendId: 0,
    status: "idle",
    source: "none",
  },
  appendStream: {
    source: null,
    conversationId: "",
    status: "offline",
    lastAppendId: 0,
    transport: "polling",
    lastRenderSource: "snapshot",
    lastLiveAppendId: 0,
  },
  liveFollow: {
    conversationId: "",
    isFollowing: true,
    jumpVisible: false,
    lastAppendId: 0,
    lastSeenAppendId: 0,
    pendingAppendCount: 0,
  },
  threadTransition: {
    active: false,
    targetConversationId: "",
    targetTitle: "",
    sourceConversationId: "",
    startedAt: "",
  },
  sessionRail: {
    conversationId: "",
    expanded: false,
  },
};

export function maxConversationAppendId(conversation) {
  if (!conversation || typeof conversation !== "object") {
    return 0;
  }
  const messages = Array.isArray(conversation.messages) ? conversation.messages : [];
  const events = Array.isArray(conversation.events) ? conversation.events : [];
  return [...messages, ...events].reduce((maxValue, item) => {
    const appendId = Number(item?.append_id || 0);
    return appendId > maxValue ? appendId : maxValue;
  }, 0);
}

export function isAppendStreamConnected(currentState, conversationId = "") {
  const appendStream = currentState.appendStream || {};
  return (
    appendStream.status === "live" &&
    appendStream.transport === "sse" &&
    appendStream.conversationId &&
    (!conversationId || appendStream.conversationId === conversationId)
  );
}

export function draftKey(appId, conversationId = "") {
  return `${appId || "no-app"}::${conversationId || "new-conversation"}`;
}

export function loadDrafts() {
  const raw = localStorage.getItem(DRAFTS_KEY);
  if (!raw) {
    return {};
  }

  try {
    const payload = JSON.parse(raw);
    return payload && typeof payload === "object" ? payload : {};
  } catch (_) {
    localStorage.removeItem(DRAFTS_KEY);
    return {};
  }
}

export function saveDrafts(currentState) {
  localStorage.setItem(DRAFTS_KEY, JSON.stringify(currentState.draftCache || {}));
}

export function setDraft(currentState, appId, conversationId, text) {
  currentState.draftCache ||= {};
  const key = draftKey(appId, conversationId);
  const value = String(text || "");
  if (value.trim()) {
    currentState.draftCache[key] = value;
  } else {
    delete currentState.draftCache[key];
  }
  saveDrafts(currentState);
}

export function getDraft(currentState, appId, conversationId) {
  const drafts = currentState.draftCache || {};
  return drafts[draftKey(appId, conversationId)] || drafts[draftKey(appId, "")] || "";
}

export function normalizeBaseUrl() {
  return FIXED_RUNTIME_URL.replace(/\/+$/, "");
}

export function saveSettings(dom, currentState) {
  localStorage.setItem(
    STORAGE_KEY,
    JSON.stringify({
      selectedAppId: dom.appSelect.value,
      selectedConversationId: currentState.currentConversationId || currentState.savedConversationId || "",
      autoOpen: dom.autoOpenInput.checked,
    }),
  );
}

export function loadSettings(dom, currentState) {
  currentState.draftCache = loadDrafts();
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return;
  }

  try {
    const payload = JSON.parse(raw);
    dom.autoOpenInput.checked = Boolean(payload.autoOpen);
    currentState.savedAppId = payload.selectedAppId || "";
    currentState.savedConversationId = payload.selectedConversationId || "";
  } catch (_) {
    localStorage.removeItem(STORAGE_KEY);
  }
}
