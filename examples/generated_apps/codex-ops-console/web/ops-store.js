import { DRAFTS_KEY, FIXED_RUNTIME_URL, STORAGE_KEY } from "./ops-constants.js";

export const state = {
  deferredInstallPrompt: null,
  pollingTimer: null,
  latestProposalJobId: "",
  currentConversationId: "",
  currentJobId: "",
  savedAppId: "",
  savedConversationId: "",
  appSession: {
    appId: "",
    sessionId: "",
    previousSessionId: "",
    rotationDetected: false,
    rotationDetectedAt: "",
  },
  conversationCache: null,
  recentConversations: [],
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
    attachMode: "idle",
    bootstrapVersion: "",
    resumeMode: "idle",
    resumeCursor: 0,
    reconnectAttempt: 0,
    reconnectTimerId: 0,
    sessionPhase: {
      value: "UNKNOWN",
      authoritative: false,
      reason: "idle",
      appendId: 0,
      source: "none",
      eventType: "",
      status: "",
      jobId: "",
    },
  },
  liveFollow: {
    conversationId: "",
    isFollowing: true,
    jumpVisible: false,
    lastAppendId: 0,
    lastSeenAppendId: 0,
    pendingAppendCount: 0,
  },
  autonomySummary: null,
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

export function isAppendStreamAuthoritative(currentState, conversationId = "") {
  const appendStream = currentState.appendStream || {};
  return (
    appendStream.transport === "sse" &&
    (appendStream.status === "connecting" || appendStream.status === "live") &&
    appendStream.conversationId &&
    (!conversationId || appendStream.conversationId === conversationId)
  );
}

export function deriveSelectedThreadSessionStatus(currentState, conversation = null) {
  const appendStream = currentState.appendStream || {};
  const appSession = currentState.appSession || {};
  const pendingOutgoing = currentState.pendingOutgoing || {};
  const threadTransition = currentState.threadTransition || {};
  const liveFollow = currentState.liveFollow || {};
  const sessionPhase = appendStream.sessionPhase || {};
  const events = Array.isArray(conversation?.events) ? conversation.events : [];
  const conversationId = String(conversation?.conversation_id || currentState.currentConversationId || "");
  const conversationTitle = String(conversation?.title || "현재 대화").trim() || "현재 대화";
  const currentConversationId = String(currentState.currentConversationId || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const transport = String(appendStream.transport || "polling").toLowerCase();
  const renderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const streamStatus = String(appendStream.status || "offline").toLowerCase();
  const pendingStatus = String(pendingOutgoing.status || "idle");
  const phaseValue = String(sessionPhase.value || "UNKNOWN").toUpperCase();
  const phaseSource = String(sessionPhase.source || "none").toLowerCase();
  const targetConversationId = String(threadTransition.targetConversationId || "");
  const targetTitle = String(threadTransition.targetTitle || "").trim() || conversationTitle;
  const latestEvent = events.length ? events[events.length - 1] : null;
  const latestType = String(latestEvent?.type || "");
  const retrying = latestType === "codex.exec.retrying";
  const sessionRotationDetected = Boolean(appSession.rotationDetected) && Boolean(appSession.appId);
  const selectedThreadStream =
    Boolean(conversationId) &&
    currentConversationId === conversationId &&
    streamConversationId === conversationId;
  const selectedThreadSse = selectedThreadStream && transport === "sse";
  const selectedThreadSseAuthoritative =
    selectedThreadSse &&
    renderSource === "sse" &&
    (streamStatus === "connecting" || streamStatus === "live");
  const selectedThreadSseOwned =
    selectedThreadSse &&
    renderSource === "sse" &&
    streamStatus === "live";
  const pendingHandoff =
    Boolean(conversationId) &&
    pendingOutgoing.conversationId === conversationId &&
    (pendingStatus === "sending-user" || pendingStatus === "awaiting-assistant");
  const phaseOwned =
    phaseValue === "LIVE" ||
    (Boolean(sessionPhase.authoritative) &&
      (
        phaseValue === "PROPOSAL" ||
        phaseValue === "REVIEW" ||
        phaseValue === "VERIFY" ||
        phaseValue === "READY" ||
        phaseValue === "APPLIED"
      ));
  const followPaused = selectedThreadSseOwned && !Boolean(liveFollow.isFollowing);
  const unseenCount =
    selectedThreadSseOwned && Boolean(liveFollow.jumpVisible)
      ? Math.max(Number(liveFollow.pendingAppendCount || 0), 0)
      : 0;

  let transportState = "snapshot";
  let transportLabel = "";
  let transportTone = "muted";
  let transportReason = "snapshot";
  if (selectedThreadStream && streamStatus === "reconnecting") {
    transportState = "reconnect";
    transportLabel = "RECONNECT";
    transportTone = "warning";
    transportReason = "reconnecting";
  } else if (retrying || sessionRotationDetected || (selectedThreadStream && (transport !== "sse" || renderSource !== "sse"))) {
    transportState = "polling";
    transportLabel = "POLLING";
    transportTone = sessionRotationDetected ? "danger" : "warning";
    transportReason = sessionRotationDetected ? "session-rotation" : retrying ? "retrying" : "polling-fallback";
  } else if (selectedThreadSseAuthoritative) {
    transportState = "sse";
    transportLabel = "SSE OWNER";
    transportTone = "healthy";
    transportReason = followPaused ? "selected-thread-follow-paused" : "selected-thread-following";
  } else if (threadTransition.active && targetConversationId) {
    transportState = "attach";
    transportLabel = "ATTACH";
    transportTone = "warning";
    transportReason = "thread-switch";
  } else if (pendingHandoff && selectedThreadSse) {
    transportState = "sse";
    transportReason = "pending-handoff";
  } else if (!conversationId) {
    transportState = "none";
    transportReason = threadTransition.active && targetConversationId ? "thread-switch" : "no-selection";
  }

  let presentation = "cleared";
  let clearReason = "idle";
  let liveIndicatorVisible = false;
  let liveOwned = false;
  let handoffVisible = false;
  let followState = "idle";
  let railLabel = "";

  if (threadTransition.active && targetConversationId) {
    presentation = "attach";
    clearReason = "thread-switch";
  } else if (pendingHandoff && selectedThreadSse) {
    presentation = "handoff";
    clearReason = "none";
    handoffVisible = true;
    followState = "handoff";
    railLabel = "HANDOFF";
  } else if (selectedThreadSseOwned && phaseOwned) {
    presentation = "owned";
    clearReason = "none";
    liveIndicatorVisible = true;
    liveOwned = true;
    followState = unseenCount > 0 ? "new" : followPaused ? "paused" : "live";
    railLabel = unseenCount > 0 ? "NEW" : followPaused ? "PAUSED" : "LIVE";
  } else if (transportState === "reconnect" || transportState === "polling") {
    presentation = "degraded";
    clearReason = transportReason;
    liveIndicatorVisible = true;
  } else if (!conversationId) {
    presentation = "cleared";
    clearReason = transportReason;
  } else {
    presentation = "cleared";
    clearReason = selectedThreadStream ? "non-authoritative" : "snapshot";
  }

  return {
    conversationId,
    conversationTitle,
    targetConversationId,
    targetTitle,
    selectedThreadStream,
    selectedThreadSse,
    selectedThreadSseAuthoritative,
    selectedThreadSseOwned,
    pendingHandoff,
    phaseValue,
    phaseSource,
    phaseAuthoritative: Boolean(sessionPhase.authoritative),
    phaseOwned,
    transport,
    renderSource,
    streamStatus,
    transportState,
    transportLabel,
    transportTone,
    transportReason,
    presentation,
    clearReason,
    liveIndicatorVisible,
    liveOwned,
    handoffVisible,
    followPaused,
    followState,
    unseenCount,
    railLabel,
    authoritative: pendingHandoff ? selectedThreadSse : selectedThreadSseAuthoritative && phaseOwned,
    retrying,
    sessionRotationDetected,
  };
}

export function isSelectedThreadSessionOwned(currentState, conversationId = "") {
  const selectedThreadStatus = deriveSelectedThreadSessionStatus(currentState, { conversation_id: conversationId });
  return Boolean(selectedThreadStatus.authoritative);
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
