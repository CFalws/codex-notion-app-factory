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
    degradedReason: "",
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
    sessionStatus: null,
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
  const savedConversationId = String(currentState.savedConversationId || "");
  const attachMode = String(appendStream.attachMode || "idle").toLowerCase();
  const resumeMode = String(appendStream.resumeMode || "idle").toLowerCase();
  const conversationId = String(conversation?.conversation_id || currentState.currentConversationId || savedConversationId || "");
  const conversationTitle = String(conversation?.title || "현재 대화").trim() || "현재 대화";
  const currentConversationId = String(currentState.currentConversationId || savedConversationId || "");
  const streamConversationId = String(appendStream.conversationId || "");
  const transport = String(appendStream.transport || "polling").toLowerCase();
  const renderSource = String(appendStream.lastRenderSource || "snapshot").toLowerCase();
  const streamStatus = String(appendStream.status || "offline").toLowerCase();
  const degradedReason = String(appendStream.degradedReason || "").trim();
  const pendingStatus = String(pendingOutgoing.status || "idle");
  const phaseValue = String(sessionPhase.value || "UNKNOWN").toUpperCase();
  const phaseSource = String(sessionPhase.source || "none").toLowerCase();
  const targetConversationId = String(threadTransition.targetConversationId || "");
  const targetTitle = String(threadTransition.targetTitle || "").trim() || conversationTitle;
  const switchActive = Boolean(threadTransition.active && targetConversationId);
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
  const selectedThreadProvisional =
    Boolean(conversationId) &&
    !threadTransition.active &&
    selectedThreadSse &&
    renderSource !== "sse" &&
    (streamStatus === "connecting" || streamStatus === "live") &&
    (attachMode === "awaiting-bootstrap" || attachMode === "sse-resume");
  const selectedThreadRestore =
    Boolean(savedConversationId) &&
    conversationId === savedConversationId &&
    !threadTransition.active &&
    !selectedThreadProvisional &&
    (!selectedThreadStream && transport === "sse" && (attachMode === "awaiting-bootstrap" || attachMode === "sse-resume"));
  const restoreResume =
    selectedThreadRestore &&
    (resumeMode === "resuming" || resumeMode === "resumed" || attachMode === "sse-resume");
  const provisionalResume =
    selectedThreadProvisional &&
    (resumeMode === "resuming" || resumeMode === "resumed" || attachMode === "sse-resume");
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
  } else if (selectedThreadProvisional) {
    transportState = provisionalResume ? "resume" : "attach";
    transportLabel = provisionalResume ? "RESUME" : "ATTACH";
    transportTone = provisionalResume ? "warning" : "neutral";
    transportReason = provisionalResume ? "selected-thread-resume" : "selected-thread-attach";
  } else if (
    retrying ||
    sessionRotationDetected ||
    (selectedThreadStream && (transport !== "sse" || (renderSource !== "sse" && !selectedThreadProvisional)))
  ) {
    transportState = "polling";
    transportLabel = "POLLING";
    transportTone = sessionRotationDetected ? "danger" : "warning";
    transportReason = sessionRotationDetected
      ? "session-rotation"
      : retrying
        ? "retrying"
        : degradedReason || "polling-fallback";
  } else if (selectedThreadSseAuthoritative) {
    transportState = "sse";
    transportLabel = "SSE OWNER";
    transportTone = "healthy";
    transportReason = followPaused ? "selected-thread-follow-paused" : "selected-thread-following";
  } else if (selectedThreadRestore) {
    transportState = restoreResume ? "resume" : "attach";
    transportLabel = restoreResume ? "RESUME" : "ATTACH";
    transportTone = restoreResume ? "warning" : "neutral";
    transportReason = restoreResume ? "saved-restore-resume" : "saved-restore-attach";
  } else if (switchActive) {
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
  let restoreStage = "none";
  let restorePath = "none";
  let restoreProvenance = "none";

  if (switchActive) {
    presentation = "attach";
    clearReason = "thread-switch";
  } else if (selectedThreadProvisional) {
    presentation = "provisional";
    clearReason = "none";
    liveIndicatorVisible = true;
    restoreStage = provisionalResume ? "resume-open" : "attach-open";
    restorePath = provisionalResume ? "resume" : "attach";
    restoreProvenance = "sse-open";
  } else if (selectedThreadRestore) {
    presentation = "restore";
    clearReason = "none";
    liveIndicatorVisible = true;
    restoreStage = restoreResume ? "resume-pending" : "attach-pending";
    restorePath = restoreResume ? "resume" : "attach";
    restoreProvenance = "sse-bootstrap";
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
    switchActive,
    switchConversationId: targetConversationId,
    switchTargetTitle: targetTitle,
    selectedThreadProvisional,
    selectedThreadRestore,
    restoreResume,
    provisionalResume,
    restoreStage,
    restorePath,
    restoreProvenance,
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

export function deriveSelectedThreadHealthyPromotionModel(currentState, conversation = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const sessionStatusPayload = currentState.appendStream?.sessionStatus || null;
  const conversationId = String(sessionStatus.conversationId || conversation?.conversation_id || "");
  const payloadConversationId = String(
    sessionStatusPayload?.conversationId || sessionStatusPayload?.conversation_id || "",
  );
  const payloadTransportState = String(
    sessionStatusPayload?.transportState || sessionStatusPayload?.transport?.state || "idle",
  ).toLowerCase();
  const payloadSource = String(
    sessionStatusPayload?.source || sessionStatusPayload?.transport?.channel || "none",
  ).toLowerCase();
  const sameConversation =
    Boolean(conversationId) &&
    Boolean(payloadConversationId) &&
    conversationId === payloadConversationId;
  const selectedThreadAuthoritative =
    Boolean(sessionStatus.selectedThreadSseOwned) &&
    sessionStatus.transportState === "sse" &&
    sessionStatus.presentation === "owned" &&
    Boolean(sessionStatus.liveOwned) &&
    Boolean(sessionStatus.phaseOwned);
  const payloadHealthy = sameConversation && payloadTransportState === "sse-live";
  const promoted = selectedThreadAuthoritative && payloadHealthy;
  const reason = promoted
    ? "selected-thread-healthy-promotion"
    : !conversationId
      ? "no-selection"
      : !payloadConversationId
        ? "missing-session-status-conversation"
        : !sameConversation
          ? "conversation-mismatch"
          : payloadTransportState !== "sse-live"
            ? `session-status-${payloadTransportState || "idle"}`
            : String(sessionStatus.transportReason || sessionStatus.clearReason || "non-authoritative");
  return {
    promoted,
    conversationId,
    payloadConversationId,
    sameConversation,
    selectedThreadAuthoritative,
    payloadHealthy,
    payloadTransportState,
    payloadSource,
    reason,
    sessionStatus,
  };
}

export function deriveSelectedThreadFollowControlModel(currentState) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, null);
  const liveFollow = currentState.liveFollow || {};
  const detachedHealthyFollow =
    sessionStatus.transportState === "sse" &&
    sessionStatus.selectedThreadSseOwned &&
    (sessionStatus.followState === "new" || sessionStatus.followState === "paused");
  const unseenCount = detachedHealthyFollow
    ? Math.max(Number(sessionStatus.unseenCount || liveFollow.pendingAppendCount || 0), 0)
    : 0;
  const followState = detachedHealthyFollow ? sessionStatus.followState : "hidden";
  const stateLabel = followState === "new" ? "NEW" : followState === "paused" ? "PAUSED" : "";
  const detailLabel =
    followState === "new"
      ? `새 live append ${Math.max(unseenCount, 1)}개`
      : followState === "paused"
        ? `live follow paused · unseen ${unseenCount}`
        : "";
  return {
    conversationId: String(sessionStatus.conversationId || ""),
    liveOwned: detachedHealthyFollow,
    visible: detachedHealthyFollow,
    followState,
    unseenCount,
    stateLabel,
    detailLabel,
    renderSource: String(sessionStatus.renderSource || "snapshot"),
    clearReason: detachedHealthyFollow ? "none" : String(sessionStatus.clearReason || sessionStatus.transportReason || "idle"),
  };
}

export function deriveSelectedThreadActiveSessionRowModel(currentState, conversation = null) {
  const sessionSnapshot = deriveSelectedThreadSessionSnapshot(currentState, conversation);
  const authority = sessionSnapshot.authority;
  const sessionStatus = sessionSnapshot.sessionStatus;
  const conversationTitle = sessionStatus.conversationTitle || "현재 대화";
  if (authority.state === "switching") {
    return {
      visible: false,
      conversationId: "",
      presentation: "cleared",
      rowState: "idle",
      ownerLabel: "",
      stateLabel: "",
      followLabel: "",
      title: String(sessionStatus.targetTitle || "선택한 대화").trim() || "선택한 대화",
      meta: "selected thread",
      rowOwned: false,
      canonical: false,
      rowSource: "none",
      rowPhase: "IDLE",
      rowUnseenCount: 0,
      clearReason: "thread-switch",
    };
  }
  if (authority.state === "restore") {
    return {
      visible: true,
      conversationId: String(sessionStatus.conversationId || ""),
      presentation: "restore",
      rowState: sessionStatus.restoreResume ? "resume" : "attach",
      ownerLabel: sessionSnapshot.transportLabel || (sessionStatus.restoreResume ? "RESUME" : "ATTACH"),
      stateLabel: "RESTORE",
      followLabel: sessionStatus.restoreResume ? "RESUME" : "ATTACH",
      title: conversationTitle,
      meta: sessionStatus.restoreResume
        ? "selected thread · restore · sse resume pending"
        : "selected thread · restore · sse attach pending",
      rowOwned: false,
      canonical: true,
      rowSource: "sse",
      rowPhase: sessionSnapshot.phaseLabel || (sessionStatus.restoreResume ? "RESUME" : "ATTACH"),
      rowUnseenCount: 0,
      clearReason: "none",
    };
  }
  if (authority.state === "provisional") {
    return {
      visible: true,
      conversationId: String(sessionStatus.conversationId || ""),
      presentation: "provisional",
      rowState: sessionStatus.provisionalResume ? "resume" : "attach",
      ownerLabel: sessionSnapshot.transportLabel || (sessionStatus.provisionalResume ? "RESUME" : "ATTACH"),
      stateLabel: sessionStatus.provisionalResume ? "RESUME" : "ATTACH",
      followLabel: "PENDING",
      title: conversationTitle,
      meta: sessionStatus.provisionalResume
        ? "selected thread · provisional · sse resume pending"
        : "selected thread · provisional · sse attach pending",
      rowOwned: false,
      canonical: true,
      rowSource: "sse",
      rowPhase: sessionSnapshot.phaseLabel || (sessionStatus.provisionalResume ? "RESUME" : "ATTACH"),
      rowUnseenCount: 0,
      clearReason: "none",
    };
  }
  if (authority.state === "degraded") {
    return {
      visible: true,
      conversationId: String(sessionStatus.conversationId || ""),
      presentation: "degraded",
      rowState: sessionStatus.transportState === "reconnect" ? "reconnect" : "polling",
      ownerLabel: sessionSnapshot.transportLabel || "POLLING",
      stateLabel: sessionSnapshot.phaseLabel || sessionSnapshot.transportLabel || "POLLING",
      followLabel: "WATCH",
      title: conversationTitle,
      meta: `selected thread · ${String(sessionSnapshot.transportLabel || "polling").toLowerCase()} · fallback visible`,
      rowOwned: false,
      canonical: true,
      rowSource: sessionSnapshot.source || "polling",
      rowPhase: sessionSnapshot.phaseLabel || sessionSnapshot.transportLabel || "POLLING",
      rowUnseenCount: 0,
      clearReason: "none",
    };
  }
  return {
    visible: false,
    conversationId: "",
    presentation: "cleared",
    rowState: "idle",
    ownerLabel: "OWNER",
    stateLabel: "SESSION",
    followLabel: "LIVE",
    title: "선택된 대화",
    meta: "selected thread",
    rowOwned: false,
    canonical: false,
    rowSource: "none",
    rowPhase: "IDLE",
    rowUnseenCount: 0,
    clearReason: String(authority.clearReason || sessionStatus.clearReason || sessionStatus.transportReason || "idle"),
  };
}

export function deriveSelectedThreadConversationRowLiveModel(currentState, conversation = null) {
  const sessionSnapshot = deriveSelectedThreadSessionSnapshot(currentState, conversation);
  if (!sessionSnapshot.rowOwned || !sessionSnapshot.conversationId || sessionSnapshot.rowSource !== "sse") {
    return {
      visible: false,
      conversationId: "",
      markerLabel: "",
      cueLabel: "",
      cueKind: "idle",
      rowState: "idle",
      rowPhase: "IDLE",
      rowSource: "none",
      rowOwned: false,
      rowUnseenCount: 0,
    };
  }

  const markerLabel =
    sessionSnapshot.rowState === "handoff"
      ? "HANDOFF"
      : sessionSnapshot.rowState === "new"
        ? "NEW"
        : sessionSnapshot.rowState === "paused"
          ? "PAUSED"
          : "LIVE";
  const cueLabel =
    sessionSnapshot.rowState === "handoff"
      ? "FIRST"
      : sessionSnapshot.rowState === "new"
        ? `+${Math.max(Number(sessionSnapshot.rowUnseenCount || 0), 1)}`
        : sessionSnapshot.rowState === "paused"
          ? Number(sessionSnapshot.rowUnseenCount || 0) > 0
            ? `+${Number(sessionSnapshot.rowUnseenCount || 0)}`
            : "OFF"
          : "FOLLOW";
  const cueKind =
    sessionSnapshot.rowState === "handoff"
      ? "handoff"
      : sessionSnapshot.rowState === "new"
        ? "unread"
        : sessionSnapshot.rowState === "paused"
          ? "paused"
          : "follow";

  return {
    visible: true,
    conversationId: String(sessionSnapshot.conversationId || ""),
    markerLabel,
    cueLabel,
    cueKind,
    rowState: String(sessionSnapshot.rowState || "live"),
    rowPhase: String(sessionSnapshot.rowPhase || "LIVE"),
    rowSource: String(sessionSnapshot.rowSource || "sse"),
    rowOwned: Boolean(sessionSnapshot.rowOwned),
    rowUnseenCount: Math.max(Number(sessionSnapshot.rowUnseenCount || 0), 0),
  };
}

export function deriveSelectedThreadComposerTargetRowModel(currentState, conversation = null) {
  const sessionSnapshot = deriveSelectedThreadSessionSnapshot(currentState, conversation);
  return {
    state: String(sessionSnapshot.composerState || "idle"),
    label: String(sessionSnapshot.composerLabel || "IDLE"),
    tone: String(sessionSnapshot.composerTone || "muted"),
    conversationId: String(sessionSnapshot.composerConversationId || ""),
    target: String(sessionSnapshot.composerTarget || "NO TARGET"),
    copy: String(sessionSnapshot.composerCopy || "SELECT"),
    blocked: Boolean(sessionSnapshot.composerBlocked),
    blockedReason: String(sessionSnapshot.composerBlockedReason || ""),
  };
}

export function deriveSelectedThreadLiveAutonomy(currentState, conversation = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, conversation);
  const autonomySummary = currentState.autonomySummary;
  const sessionStatusPayload = currentState.appendStream?.sessionStatus || null;
  const phaseValue = String(sessionStatusPayload?.phase?.value || "UNKNOWN").toUpperCase();
  const proposalStatus = String(sessionStatusPayload?.proposalStatus || "").toLowerCase();
  const sessionStatusSummary =
    sessionStatusPayload && typeof sessionStatusPayload === "object"
      ? {
          goalTitle: String(sessionStatusPayload?.goalTitle || autonomySummary?.goalTitle || "Autonomy Goal"),
          goalStatus:
            String(autonomySummary?.goalStatus || "").trim() ||
            (proposalStatus
              ? proposalStatus
              : phaseValue === "READY"
                ? "ready"
                : phaseValue === "APPLIED"
                  ? "applied"
                  : String(sessionStatusPayload?.pathVerdict || "UNKNOWN").toUpperCase() === "DEGRADED"
                    ? "blocked"
                    : "running"),
          iteration: String(autonomySummary?.iteration || ""),
          pathVerdict: String(sessionStatusPayload?.pathVerdict || autonomySummary?.pathVerdict || "UNKNOWN").toUpperCase(),
          verifierAcceptability: String(
            sessionStatusPayload?.verifierAcceptability || autonomySummary?.verifierAcceptability || "PENDING",
          ).toUpperCase(),
          blockerReason: String(sessionStatusPayload?.blockerReason || autonomySummary?.blockerReason || "none"),
          expectedPath: String(sessionStatusPayload?.expectedPath || autonomySummary?.expectedPath || "unknown"),
          degradedSignals: Array.isArray(sessionStatusPayload?.degradedSignals)
            ? sessionStatusPayload.degradedSignals
            : Array.isArray(autonomySummary?.degradedSignals)
              ? autonomySummary.degradedSignals
              : [],
          heading:
            String(sessionStatusPayload?.heading || "").trim() ||
            String(sessionStatusPayload?.goalTitle || autonomySummary?.goalTitle || "Autonomy Goal").trim() +
              " · " +
              (
                String(sessionStatusPayload?.goalStatus || autonomySummary?.goalStatus || "").trim() ||
                (proposalStatus || "running")
              ) +
              " · iteration " +
              String(sessionStatusPayload?.iteration || autonomySummary?.iteration || "unknown"),
          source: "session-status",
          generatedAt: String(sessionStatusPayload?.createdAt || autonomySummary?.generatedAt || ""),
          freshnessState: sessionStatus.liveOwned ? "fresh" : "stale-or-missing",
          fallbackAllowed: !sessionStatus.liveOwned,
        }
      : null;
  const canonicalAutonomySummary = sessionStatusSummary || autonomySummary;
  if (sessionStatus.presentation === "restore" || sessionStatus.presentation === "provisional") {
    return {
      visible: true,
      owned: false,
      presentation: sessionStatus.presentation,
      label: sessionStatus.transportLabel || "ATTACH",
      reason: sessionStatus.transportReason,
      source: sessionStatus.transport || "sse",
      freshnessState: String(canonicalAutonomySummary?.freshnessState || "stale-or-missing").toLowerCase(),
      fallbackAllowed: false,
      summary: canonicalAutonomySummary || null,
    };
  }
  if (!canonicalAutonomySummary || typeof canonicalAutonomySummary !== "object") {
    return {
      visible: false,
      owned: false,
      presentation: "cleared",
      label: "",
      reason: sessionStatus.clearReason,
      source: "none",
      freshnessState: "stale-or-missing",
      fallbackAllowed: true,
      summary: null,
    };
  }
  if (sessionStatus.presentation === "attach") {
    return {
      visible: false,
      owned: false,
      presentation: "cleared",
      label: "",
      reason: "thread-switch",
      source: "none",
      freshnessState: String(canonicalAutonomySummary.freshnessState || "stale-or-missing").toLowerCase(),
      fallbackAllowed: Boolean(canonicalAutonomySummary.fallbackAllowed ?? true),
      summary: canonicalAutonomySummary,
    };
  }
  if (sessionStatus.transportState === "reconnect" || sessionStatus.transportState === "polling") {
    return {
      visible: true,
      owned: false,
      presentation: "degraded",
      label: sessionStatus.transportLabel,
      reason: sessionStatus.transportReason,
      source: sessionStatus.transport === "sse" ? sessionStatus.renderSource || "snapshot" : sessionStatus.transport || "polling",
      freshnessState: String(canonicalAutonomySummary.freshnessState || "stale-or-missing").toLowerCase(),
      fallbackAllowed: Boolean(canonicalAutonomySummary.fallbackAllowed ?? true),
      summary: canonicalAutonomySummary,
    };
  }
  if (sessionStatus.liveOwned) {
    return {
      visible: healthyPromotion.promoted,
      owned: healthyPromotion.promoted,
      presentation: healthyPromotion.promoted ? "owned" : "cleared",
      label: sessionStatus.transportLabel || "SSE OWNER",
      reason: healthyPromotion.reason,
      source: healthyPromotion.promoted
        ? String(canonicalAutonomySummary.source || healthyPromotion.payloadSource || "sse").toLowerCase()
        : "none",
      freshnessState: String(
        canonicalAutonomySummary.freshnessState || (healthyPromotion.promoted ? "fresh" : "stale-or-missing"),
      ).toLowerCase(),
      fallbackAllowed: healthyPromotion.promoted
        ? Boolean(canonicalAutonomySummary.fallbackAllowed ?? false)
        : true,
      summary: canonicalAutonomySummary,
    };
  }
  return {
    visible: false,
    owned: false,
    presentation: "cleared",
    label: "",
    reason: sessionStatus.clearReason,
    source: "none",
    freshnessState: String(canonicalAutonomySummary.freshnessState || "stale-or-missing").toLowerCase(),
    fallbackAllowed: Boolean(canonicalAutonomySummary.fallbackAllowed ?? true),
    summary: canonicalAutonomySummary,
  };
}

export function deriveSelectedThreadPhaseProgression(currentState, conversation = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, conversation);
  const appendStream = currentState.appendStream || {};
  const sessionPhase = appendStream.sessionPhase || {};
  const phaseValue = String(sessionPhase.value || "UNKNOWN").toUpperCase();
  const eventType = String(sessionPhase.eventType || sessionPhase.event_type || "");
  const phaseSource = String(sessionPhase.source || "none").toLowerCase();

  if (sessionStatus.presentation === "restore" || sessionStatus.presentation === "provisional") {
    const sessionStatusPayload = currentState.appendStream?.sessionStatus || null;
    const fallbackPhaseLabel =
      sessionStatus.presentation === "provisional"
        ? canonicalPhaseLabelFromStatus(sessionStatusPayload, sessionStatus.transportLabel || "ATTACH")
        : sessionStatus.transportLabel || "ATTACH";
    return {
      visible: true,
      label: fallbackPhaseLabel,
      state:
        sessionStatus.presentation === "provisional"
          ? "provisional"
          : sessionStatus.restoreResume
            ? "resume"
            : "attach",
      source: "sse",
      authoritative: false,
      owned: false,
      reason: sessionStatus.transportReason,
      appendId: 0,
      jobId: "",
    };
  }
  if (sessionStatus.presentation === "attach" || !sessionStatus.conversationId) {
    return {
      visible: false,
      label: "",
      state: "idle",
      source: "none",
      authoritative: false,
      owned: false,
      reason: sessionStatus.clearReason,
      appendId: 0,
      jobId: "",
    };
  }
  if (sessionStatus.pendingHandoff && sessionStatus.selectedThreadSse) {
    return {
      visible: true,
      label: "HANDOFF",
      state: "handoff",
      source: "handoff",
      authoritative: false,
      owned: false,
      reason: "pending-handoff",
      appendId: 0,
      jobId: "",
    };
  }
  if (sessionStatus.transportState === "reconnect" || sessionStatus.transportState === "polling") {
    return {
      visible: true,
      label: sessionStatus.transportLabel,
      state: sessionStatus.transportState,
      source: sessionStatus.transport === "sse" ? sessionStatus.renderSource || "snapshot" : sessionStatus.transport || "polling",
      authoritative: false,
      owned: false,
      reason: sessionStatus.transportReason,
      appendId: 0,
      jobId: "",
    };
  }
  if (!sessionStatus.selectedThreadSseAuthoritative) {
    return {
      visible: false,
      label: "",
      state: "idle",
      source: "none",
      authoritative: false,
      owned: false,
      reason: "non-authoritative",
      appendId: 0,
      jobId: "",
    };
  }

  let label = phaseValue;
  if (eventType === "goal.proposal.auto_apply.started") {
    label = "AUTO APPLY";
  } else if (phaseValue === "LIVE") {
    label = "LIVE";
  } else if (!phaseValue || phaseValue === "UNKNOWN") {
    label = "UNKNOWN";
  }

  return {
    visible: true,
    label,
    state: String(label || "unknown").toLowerCase().replace(/\s+/g, "-"),
    source: phaseSource || "sse",
    authoritative: Boolean(sessionPhase.authoritative),
    owned: healthyPromotion.promoted,
    reason: healthyPromotion.reason,
    appendId: Math.max(Number(sessionPhase.appendId || sessionPhase.append_id || 0), 0),
    jobId: String(sessionPhase.jobId || sessionPhase.job_id || ""),
  };
}

export function deriveSelectedThreadShellPhaseLabel(currentState, conversation = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  if (
    !sessionStatus.liveOwned ||
    !phaseProgression.visible ||
    !phaseProgression.owned ||
    !phaseProgression.authoritative
  ) {
    return "";
  }
  const label = String(phaseProgression.label || "").toUpperCase();
  return ["PROPOSAL", "REVIEW", "VERIFY", "AUTO APPLY", "READY", "APPLIED", "FAILED"].includes(label)
    ? label
    : "";
}

export function deriveSelectedThreadTimelineMilestones(currentState, conversation = null) {
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  const summary = liveAutonomy.summary;
  if (!liveAutonomy.owned || !summary || !phaseProgression.visible) {
    return {
      visible: false,
      currentLabel: String(phaseProgression.label || "").toUpperCase(),
      source: String(phaseProgression.source || liveAutonomy.source || "none").toLowerCase(),
      items: [],
    };
  }

  const currentPhase = String(phaseProgression.label || "LIVE").toUpperCase();
  const phaseRank =
    currentPhase === "PROPOSAL"
      ? 0
      : currentPhase === "REVIEW"
        ? 1
        : currentPhase === "VERIFY"
          ? 2
          : currentPhase === "AUTO APPLY"
            ? 3
            : currentPhase === "READY"
              ? 4
              : currentPhase === "APPLIED"
                ? 5
                : 0;
  const items = [
    { key: "proposal", label: "PROPOSAL", state: phaseRank > 0 ? "complete" : currentPhase === "PROPOSAL" ? "active" : "active" },
    { key: "review", label: "REVIEW", state: phaseRank > 1 ? "complete" : currentPhase === "REVIEW" ? "active" : "pending" },
    { key: "verify", label: "VERIFY", state: phaseRank > 2 ? "complete" : currentPhase === "VERIFY" ? "active" : "pending" },
    { key: "auto-apply", label: "AUTO APPLY", state: phaseRank > 3 ? "complete" : currentPhase === "AUTO APPLY" ? "active" : "pending" },
    { key: "ready", label: "READY", state: phaseRank > 4 ? "complete" : currentPhase === "READY" ? "active" : "pending" },
    { key: "applied", label: "APPLIED", state: currentPhase === "APPLIED" ? "active" : "pending" },
  ];

  if (String(summary.pathVerdict || "").toUpperCase() === "DEGRADED") {
    const activeItem = items.find((item) => item.state === "active") || items[0];
    if (activeItem) {
      activeItem.state = "blocked";
    }
  }

  return {
    visible: true,
    currentLabel: currentPhase,
    source: String(phaseProgression.source || liveAutonomy.source || "sse").toLowerCase(),
    items,
  };
}

export function deriveSelectedThreadSessionSurfaceModel(currentState, conversation = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, conversation);
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  const quorumModel = deriveSelectedThreadSessionQuorumModel(currentState, conversation);
  const milestoneModel = deriveSelectedThreadTimelineMilestones(currentState, conversation);
  const shellPhaseLabel = deriveSelectedThreadShellPhaseLabel(currentState, conversation);
  const liveOwned = Boolean(healthyPromotion.promoted && liveAutonomy.owned && phaseProgression.visible);
  const degradedVisible = sessionStatus.transportState === "reconnect" || sessionStatus.transportState === "polling";
  const handoffVisible = Boolean(sessionStatus.pendingHandoff && sessionStatus.selectedThreadSse);
  const restoreVisible = Boolean(sessionStatus.presentation === "restore" && liveAutonomy.visible && phaseProgression.visible);
  const provisionalVisible = Boolean(
    sessionStatus.presentation === "provisional" && liveAutonomy.visible && phaseProgression.visible,
  );
  const phaseLabel = degradedVisible
    ? String(sessionStatus.transportLabel || "POLLING").toUpperCase()
    : handoffVisible
      ? "HANDOFF"
      : String(shellPhaseLabel || phaseProgression.label || "").toUpperCase();
  const summary = liveAutonomy.summary || null;
  const summaryVisible = Boolean(summary && typeof summary === "object");
  return {
    sessionStatus,
    liveAutonomy,
    phaseProgression,
    quorumModel,
    milestoneModel,
    liveOwned,
    degradedVisible,
    handoffVisible,
    restoreVisible,
    phaseLabel,
    pathVerdict: summaryVisible ? String(summary?.pathVerdict || "UNKNOWN").toUpperCase() : "",
    verifierAcceptability: summaryVisible ? String(summary?.verifierAcceptability || "PENDING").toUpperCase() : "",
    blockerReason: summaryVisible ? String(summary?.blockerReason || "none").toUpperCase() : "",
    expectedPath: summaryVisible ? String(summary?.expectedPath || "unknown").toUpperCase() : "",
    degradedSignals: summaryVisible && Array.isArray(summary?.degradedSignals) ? summary.degradedSignals : [],
    reviewQuorumLabel: liveOwned ? String(quorumModel.reviewLabel || "") : "",
    verifyQuorumLabel: liveOwned ? String(quorumModel.verifyLabel || "") : "",
    readyLabel: liveOwned ? String(quorumModel.readyLabel || "") : "",
    source: String(
      degradedVisible
        ? sessionStatus.transport || "polling"
        : restoreVisible || provisionalVisible
          ? phaseProgression.source || liveAutonomy.source || "sse"
          : phaseProgression.source || liveAutonomy.source || "none",
    ).toLowerCase(),
  };
}

export function deriveSelectedThreadSessionAuthorityModel(currentState, conversation = null, liveRun = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, conversation);
  const sessionSurface = deriveSelectedThreadSessionSurfaceModel(currentState, conversation);
  const sessionStrip = deriveSelectedThreadSessionStripModel(currentState, conversation, liveRun);
  const shellPhaseLabel = String(deriveSelectedThreadShellPhaseLabel(currentState, conversation) || "").toUpperCase();
  const conversationId = String(sessionStatus.conversationId || "");
  const terminalClear = Boolean(liveRun?.terminal && sessionStatus.presentation !== "restore");

  let state = "cleared";
  let presentation = "cleared";
  let owned = false;
  let authoritative = false;
  let visible = false;
  let ownerLabel = "";
  let badgeStateLabel = "";
  let phaseLabel = "";
  let pathLabel = "";
  let source = "none";
  let reason = String(sessionStatus.clearReason || sessionStatus.transportReason || "idle");
  let clearReason = reason;

  if (sessionStatus.switchActive) {
    state = "switching";
    presentation = "switching";
    phaseLabel = "SWITCHING";
    pathLabel = "SWITCH";
    source = "thread-transition";
    reason = "thread-switch";
    clearReason = "thread-switch";
  } else if (sessionStatus.presentation === "provisional") {
    state = "provisional";
    presentation = "provisional";
    visible = true;
    ownerLabel = String(sessionStatus.transportLabel || (sessionStatus.provisionalResume ? "RESUME" : "ATTACH")).toUpperCase();
    badgeStateLabel = ownerLabel;
    phaseLabel = String(sessionSurface.phaseLabel || ownerLabel).toUpperCase();
    pathLabel = sessionStatus.provisionalResume ? "RESUME" : "ATTACH";
    source = String(sessionStatus.restoreProvenance || sessionStrip.source || "sse").toLowerCase();
    reason = String(sessionStatus.transportReason || "selected-thread-attach");
    clearReason = "none";
  } else if (sessionStatus.presentation === "restore") {
    state = "restore";
    presentation = "restore";
    visible = true;
    ownerLabel = String(sessionStatus.transportLabel || (sessionStatus.restoreResume ? "RESUME" : "ATTACH")).toUpperCase();
    badgeStateLabel = ownerLabel;
    phaseLabel = String(sessionSurface.phaseLabel || ownerLabel).toUpperCase();
    pathLabel = sessionStatus.restoreResume ? "RESUME" : "ATTACH";
    source = String(sessionStatus.restoreProvenance || sessionStrip.source || "sse").toLowerCase();
    reason = String(sessionStatus.transportReason || "saved-restore-attach");
    clearReason = "none";
  } else if (sessionStatus.pendingHandoff && sessionStatus.selectedThreadSse) {
    state = "handoff";
    presentation = "handoff";
    visible = true;
    owned = true;
    ownerLabel = String(sessionStatus.transportLabel || "SSE OWNER").toUpperCase();
    badgeStateLabel = "HANDOFF";
    phaseLabel = "HANDOFF";
    pathLabel = "HANDOFF";
    source = "handoff";
    reason = "pending-handoff";
    clearReason = "none";
  } else if (!terminalClear && healthyPromotion.promoted && sessionSurface.liveOwned && sessionStrip.visible && sessionStrip.owned) {
    state = "healthy";
    presentation = "healthy";
    visible = true;
    owned = true;
    authoritative = true;
    ownerLabel = String(sessionStatus.transportLabel || sessionStrip.stateLabel || "SSE OWNER").toUpperCase();
    badgeStateLabel = "SSE";
    phaseLabel = String(shellPhaseLabel || sessionSurface.phaseLabel || sessionStrip.phaseLabel || "LIVE").toUpperCase();
    pathLabel = String(sessionSurface.pathVerdict || sessionStrip.pathVerdict || "EXPECTED").toUpperCase();
    source = String(sessionStrip.source || sessionSurface.source || healthyPromotion.payloadSource || "sse").toLowerCase();
    reason = String(healthyPromotion.reason || sessionStatus.transportReason || "selected-thread-following");
    clearReason = "none";
  } else if (
    !terminalClear &&
    (sessionStatus.transportState === "reconnect" ||
      sessionStatus.transportState === "polling" ||
      sessionSurface.degradedVisible ||
      sessionStrip.presentation === "degraded")
  ) {
    state = "degraded";
    presentation = "degraded";
    visible = true;
    ownerLabel = String(sessionStatus.transportLabel || sessionStrip.stateLabel || "POLLING").toUpperCase();
    badgeStateLabel = ownerLabel;
    phaseLabel = String(sessionSurface.phaseLabel || sessionStrip.phaseLabel || ownerLabel).toUpperCase();
    pathLabel = phaseLabel;
    source = String(sessionStrip.source || sessionSurface.source || sessionStatus.transport || "polling").toLowerCase();
    reason = String(sessionStatus.transportReason || "polling-fallback");
    clearReason = "none";
  } else if (terminalClear) {
    state = "terminal-idle";
    presentation = "cleared";
    reason = "terminal";
    clearReason = "terminal";
  }

  return {
    state,
    presentation,
    visible,
    owned,
    authoritative,
    ownerLabel,
    badgeStateLabel,
    phaseLabel,
    pathLabel,
    source,
    reason,
    clearReason,
    summaryVisible: visible,
    badgeVisible: false,
    healthyPromotion,
    sessionStatus,
    sessionSurface,
    sessionStrip,
  };
}

export function isSelectedThreadPrimarySessionOwned(currentState, conversation = null, liveRun = null) {
  const authority = deriveSelectedThreadSessionAuthorityModel(currentState, conversation, liveRun);
  return authority.state === "healthy" || authority.state === "provisional";
}

export function deriveSelectedThreadSessionSnapshot(currentState, conversation = null, liveRun = null) {
  const authority = deriveSelectedThreadSessionAuthorityModel(currentState, conversation, liveRun);
  const sessionStatus = authority.sessionStatus;
  const sessionSurface = authority.sessionSurface;
  const sessionStrip = authority.sessionStrip;
  const followControl = deriveSelectedThreadFollowControlModel(currentState);
  const pendingOutgoing = currentState.pendingOutgoing || {};
  const phaseLabel = String(
    authority.phaseLabel || deriveSelectedThreadShellPhaseLabel(currentState, conversation) || sessionSurface.phaseLabel || "IDLE",
  )
    .trim()
    .toUpperCase();
  const transportLabel = String(
    authority.ownerLabel || sessionStatus.transportLabel || sessionStrip.stateLabel || "SNAPSHOT",
  )
    .trim()
    .toUpperCase();
  const owned = Boolean(authority.owned && authority.state === "healthy");
  const handoff = authority.state === "handoff";
  let rowState = "idle";
  let rowUnseenCount = 0;
  if (handoff) {
    rowState = "handoff";
  } else if (owned) {
    rowState = followControl.visible ? followControl.followState : "live";
    rowUnseenCount = followControl.visible ? Math.max(Number(followControl.unseenCount || 0), 0) : 0;
  }
  const conversationTitle = String(sessionStatus.conversationTitle || conversation?.title || "현재 대화").trim() || "현재 대화";
  let composerState = "idle";
  let composerLabel = "IDLE";
  let composerTone = "muted";
  let composerConversationId = "";
  let composerTarget = "NO TARGET";
  let composerCopy = "SELECT";
  let composerBlocked = false;
  let composerBlockedReason = "";

  if (authority.state === "switching" && sessionStatus.targetConversationId) {
    composerState = "switching";
    composerLabel = "SWITCHING";
    composerTone = "warning";
    composerConversationId = String(sessionStatus.targetConversationId || "");
    composerTarget = String(sessionStatus.targetTitle || "선택한 대화").trim() || "선택한 대화";
    composerCopy = "ATTACH";
    composerBlocked = true;
    composerBlockedReason = "ATTACH PENDING";
  } else if (authority.state === "provisional" || authority.state === "restore") {
    const resume = authority.state === "provisional" ? sessionStatus.provisionalResume : sessionStatus.restoreResume;
    composerState = resume ? "resume" : "attach";
    composerLabel = transportLabel || (resume ? "RESUME" : "ATTACH");
    composerTone = String(sessionStatus.transportTone || "neutral");
    composerConversationId = String(sessionStatus.conversationId || "");
    composerTarget = conversationTitle;
    composerCopy = resume ? "RESUME" : "ATTACH";
  } else if (authority.state === "handoff" && sessionStatus.conversationId) {
    composerState = "handoff";
    composerLabel = "HANDOFF";
    composerTone = "neutral";
    composerConversationId = String(sessionStatus.conversationId || "");
    composerTarget = conversationTitle;
    composerCopy = pendingOutgoing.status === "sending-user" ? "SEND" : "FIRST";
  } else if (authority.state === "degraded" && sessionStatus.conversationId) {
    composerState = sessionStatus.transportState === "reconnect" ? "reconnect" : "polling";
    composerLabel = transportLabel || "POLLING";
    composerTone = String(sessionStatus.transportTone || "warning");
    composerConversationId = String(sessionStatus.conversationId || "");
    composerTarget = conversationTitle;
    composerCopy = "WATCH";
  } else if (authority.state === "healthy" && sessionStatus.conversationId) {
    composerState = "ready";
    composerLabel = "READY";
    composerTone = "healthy";
    composerConversationId = String(sessionStatus.conversationId || "");
    composerTarget = conversationTitle;
    composerCopy = "SSE OWNER";
  }

  return {
    conversationId: String(sessionStatus.conversationId || conversation?.conversation_id || ""),
    state: String(authority.state || "cleared"),
    presentation: String(authority.presentation || "cleared"),
    visible: Boolean(authority.visible),
    owned,
    authoritative: Boolean(authority.authoritative),
    transportLabel,
    transportKey: String(sessionStatus.transportState || sessionStatus.transport || "snapshot"),
    transportOwned: owned,
    reason: String(authority.reason || sessionStatus.transportReason || "idle"),
    source: String(authority.source || sessionSurface.source || sessionStatus.transport || "none"),
    phaseLabel: phaseLabel || "IDLE",
    handoff,
    rowState,
    rowOwned: owned || handoff,
    rowSource: owned || handoff ? "sse" : "none",
    rowPhase: owned || handoff ? phaseLabel || "LIVE" : "IDLE",
    rowUnseenCount,
    composerState,
    composerLabel,
    composerTone,
    composerConversationId,
    composerTarget,
    composerCopy,
    composerBlocked,
    composerBlockedReason,
    authority,
    sessionStatus,
    sessionSurface,
    sessionStrip,
  };
}

function canonicalPhaseLabelFromStatus(sessionStatusPayload = {}, fallback = "UNKNOWN") {
  const phase = String(sessionStatusPayload?.phase?.value || fallback).toUpperCase();
  const eventType = String(sessionStatusPayload?.eventType || sessionStatusPayload?.event_type || sessionStatusPayload?.phase?.eventType || sessionStatusPayload?.phase?.event_type || "");
  if (eventType === "goal.proposal.auto_apply.started") {
    return "AUTO APPLY";
  }
  return phase || fallback;
}

function normalizeQuorumEntry(entry) {
  const payload = entry && typeof entry === "object" ? entry : {};
  const approved = Math.max(Number(payload.approved || 0), 0);
  const required = Math.max(Number(payload.required || 0), 0);
  const complete = Boolean(payload.complete) || (required > 0 && approved >= required);
  return {
    approved,
    required,
    complete,
    source: String(payload.source || "none").toLowerCase(),
  };
}

export function deriveSelectedThreadSessionQuorumModel(currentState, conversation = null) {
  const selectedThreadStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, conversation);
  const appendStream = currentState.appendStream || {};
  const sessionStatusPayload = appendStream.sessionStatus || null;
  const conversationId = String(conversation?.conversation_id || selectedThreadStatus.conversationId || "");
  const currentConversationId = String(currentState.currentConversationId || "");
  const payloadConversationId = String(sessionStatusPayload?.conversationId || sessionStatusPayload?.conversation_id || "");
  const selectedPayload =
    Boolean(conversationId) &&
    Boolean(payloadConversationId) &&
    conversationId === currentConversationId &&
    payloadConversationId === conversationId;
  const transportState = String(
    sessionStatusPayload?.transportState || sessionStatusPayload?.transport?.state || "idle",
  ).toLowerCase();
  const selectedThreadOwned =
    Boolean(healthyPromotion.promoted) &&
    selectedPayload &&
    transportState === "sse-live" &&
    selectedThreadStatus.presentation === "owned";
  if (!selectedThreadOwned || !sessionStatusPayload) {
    return {
      visible: false,
      state:
        selectedThreadStatus.transportState === "reconnect" || selectedThreadStatus.transportState === "polling"
          ? "downgraded"
          : "cleared",
      review: { approved: 0, required: 0, complete: false, source: "none" },
      verify: { approved: 0, required: 0, complete: false, source: "none" },
      proposalReady: false,
      proposalStatus: "",
      reviewLabel: "",
      verifyLabel: "",
      readyLabel: "",
      source: "none",
      clearReason: String(selectedThreadStatus.clearReason || selectedThreadStatus.transportReason || "lost-authority"),
    };
  }
  const review = normalizeQuorumEntry(sessionStatusPayload?.reviewQuorum || sessionStatusPayload?.review_quorum);
  const verify = normalizeQuorumEntry(sessionStatusPayload?.verifyQuorum || sessionStatusPayload?.verify_quorum);
  const proposalReady = Boolean(sessionStatusPayload?.proposalReady ?? sessionStatusPayload?.proposal_ready ?? false);
  const proposalStatus = String(sessionStatusPayload?.proposalStatus || sessionStatusPayload?.proposal_status || "").toLowerCase();
  return {
    visible: review.required > 0 || verify.required > 0 || proposalReady || proposalStatus === "ready_to_apply",
    state: "owned",
    review,
    verify,
    proposalReady,
    proposalStatus,
    reviewLabel: review.required > 0 ? `REVIEW ${review.approved}/${review.required}` : "",
    verifyLabel: verify.required > 0 ? `VERIFY ${verify.approved}/${verify.required}` : "",
    readyLabel: proposalReady || proposalStatus === "ready_to_apply" ? "READY" : "",
    source: String(sessionStatusPayload?.source || sessionStatusPayload?.transport?.channel || "append-sse").toLowerCase(),
    clearReason: "none",
  };
}

export function deriveSelectedThreadSessionStripModel(currentState, conversation = null, liveRun = null) {
  const selectedThreadStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, conversation);
  const quorumModel = deriveSelectedThreadSessionQuorumModel(currentState, conversation);
  const appendStream = currentState.appendStream || {};
  const sessionStatusPayload = appendStream.sessionStatus || null;
  const conversationId = String(conversation?.conversation_id || selectedThreadStatus.conversationId || "");
  const currentConversationId = String(currentState.currentConversationId || "");
  const payloadConversationId = String(sessionStatusPayload?.conversationId || sessionStatusPayload?.conversation_id || "");
  const selectedPayload =
    Boolean(conversationId) &&
    Boolean(payloadConversationId) &&
    conversationId === currentConversationId &&
    payloadConversationId === conversationId;
  const terminal = Boolean(liveRun?.terminal);
  const transportState = String(
    sessionStatusPayload?.transportState ||
      sessionStatusPayload?.transport?.state ||
      "idle",
  ).toLowerCase();
  const attachMode = String(
    sessionStatusPayload?.attachMode ||
      sessionStatusPayload?.transport?.attachMode ||
      sessionStatusPayload?.transport?.attach_mode ||
      "idle",
  ).toLowerCase();
  const pathVerdict = String(sessionStatusPayload?.pathVerdict || sessionStatusPayload?.path_verdict || "UNKNOWN").toUpperCase();
  const verifierAcceptability = String(
    sessionStatusPayload?.verifierAcceptability || sessionStatusPayload?.verifier_acceptability || "PENDING",
  ).toUpperCase();
  const blockerReason = String(sessionStatusPayload?.blockerReason || sessionStatusPayload?.blocker_reason || "none").toUpperCase();
  const proposalReady = Boolean(sessionStatusPayload?.proposalReady ?? sessionStatusPayload?.proposal_ready ?? false);
  const proposalStatus = String(sessionStatusPayload?.proposalStatus || sessionStatusPayload?.proposal_status || "").toLowerCase();
  const proposalJobId = String(sessionStatusPayload?.proposalJobId || sessionStatusPayload?.proposal_job_id || "");
  const latestJobId = String(sessionStatusPayload?.latestJobId || sessionStatusPayload?.latest_job_id || "");
  const degradedSignals = Array.isArray(sessionStatusPayload?.degradedSignals || sessionStatusPayload?.degraded_signals)
    ? (sessionStatusPayload.degradedSignals || sessionStatusPayload.degraded_signals)
    : [];

  if (
    !selectedPayload ||
    !conversationId ||
    selectedThreadStatus.switchActive ||
    !sessionStatusPayload ||
    terminal
  ) {
    const clearReason = selectedThreadStatus.switchActive
      ? "thread-switch"
      : terminal
        ? "terminal"
        : !conversationId || !currentConversationId
          ? "deselected"
          : !sessionStatusPayload
            ? "missing-session-status"
            : "lost-authority";
    return {
      visible: false,
      presentation: "cleared",
      conversationId,
      phaseLabel: "",
      stateLabel: "",
      detail: "",
      transportState: "idle",
      attachMode: "idle",
      tone: "muted",
      pathVerdict: "",
      verifierAcceptability: "",
      blockerReason: "",
      proposalReady: false,
      proposalStatus: "",
      proposalJobId: "",
      proposalLabel: "",
      reviewQuorumLabel: "",
      verifyQuorumLabel: "",
      readyLabel: "",
      latestJobId: "",
      degradedSignals: [],
      owned: false,
      source: "none",
      clearReason,
    };
  }

  const phaseLabel = canonicalPhaseLabelFromStatus(sessionStatusPayload, "UNKNOWN");
  const pathStateLabel =
    transportState === "sse-live"
      ? "SSE OWNER"
      : transportState === "reconnecting"
        ? "RECONNECT"
        : transportState === "polling-fallback"
          ? "POLLING"
          : attachMode === "sse-resume"
            ? "RESUME"
            : attachMode === "sse-bootstrap"
              ? "ATTACH"
              : "SESSION";
  const owned = Boolean(healthyPromotion.promoted);
  const degraded = transportState === "reconnecting" || transportState === "polling-fallback";
  const restore = attachMode === "sse-resume" || attachMode === "sse-bootstrap";
  const tone = owned ? "healthy" : degraded ? "warning" : restore ? "neutral" : "muted";
  const presentation = owned ? "healthy" : degraded ? "degraded" : restore ? "restore" : "cleared";
  const proposalLabel =
    proposalReady || proposalStatus === "ready_to_apply"
      ? "APPLY READY"
      : proposalStatus === "applied"
        ? "APPLIED"
        : proposalStatus
          ? proposalStatus.toUpperCase()
          : "";
  const detail = degraded
    ? `selected thread ${pathStateLabel.toLowerCase()} · ${selectedThreadStatus.transportReason || "fallback"}`
    : restore
      ? `selected thread ${pathStateLabel.toLowerCase()} · bootstrap pending`
      : latestJobId
        ? `selected thread ${phaseLabel.toLowerCase()} · job ${latestJobId}`
        : `selected thread ${phaseLabel.toLowerCase()} · live session`;

  return {
    visible: owned || degraded || restore,
    presentation,
    conversationId,
    phaseLabel,
    stateLabel: pathStateLabel,
    detail,
    transportState,
    attachMode,
    tone,
    pathVerdict,
    verifierAcceptability,
    blockerReason,
    proposalReady,
    proposalStatus,
    proposalJobId,
    proposalLabel,
    reviewQuorumLabel: owned ? String(quorumModel.reviewLabel || "") : "",
    verifyQuorumLabel: owned ? String(quorumModel.verifyLabel || "") : "",
    readyLabel: owned ? String(quorumModel.readyLabel || "") : "",
    latestJobId,
    degradedSignals,
    owned,
    source: String(sessionStatusPayload?.source || sessionStatusPayload?.transport?.channel || "append-sse").toLowerCase(),
    clearReason: "none",
  };
}

export function deriveSelectedThreadHealthyLiveRunModel(currentState, conversation = null) {
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, conversation);
  const sessionStatusPayload = currentState.appendStream?.sessionStatus || null;
  const conversationId = String(conversation?.conversation_id || healthyPromotion.conversationId || "");
  const payloadConversationId = String(
    sessionStatusPayload?.conversationId || sessionStatusPayload?.conversation_id || "",
  );
  if (
    !healthyPromotion.promoted ||
    !sessionStatusPayload ||
    !conversationId ||
    payloadConversationId !== conversationId
  ) {
    return {
      visible: false,
      state: "idle",
      phase: "IDLE",
      detail: "",
      source: "none",
      tone: "idle",
      jobId: "",
      terminal: false,
      appendId: 0,
      authoritative: false,
      reason: healthyPromotion.reason,
    };
  }

  const phasePayload = sessionStatusPayload?.phase && typeof sessionStatusPayload.phase === "object"
    ? sessionStatusPayload.phase
    : {};
  const rawPhase = String(phasePayload?.value || "UNKNOWN").toUpperCase();
  const eventType = String(
    sessionStatusPayload?.eventType ||
      sessionStatusPayload?.event_type ||
      phasePayload?.eventType ||
      phasePayload?.event_type ||
      "",
  );
  const proposalReady = Boolean(sessionStatusPayload?.proposalReady ?? sessionStatusPayload?.proposal_ready ?? false);
  const proposalStatus = String(
    sessionStatusPayload?.proposalStatus || sessionStatusPayload?.proposal_status || "",
  ).toLowerCase();
  const pathVerdict = String(
    sessionStatusPayload?.pathVerdict || sessionStatusPayload?.path_verdict || "UNKNOWN",
  ).toUpperCase();
  const blockerReason = String(
    sessionStatusPayload?.blockerReason || sessionStatusPayload?.blocker_reason || "none",
  ).toLowerCase();
  const phaseSource = String(
    phasePayload?.source || sessionStatusPayload?.source || sessionStatusPayload?.transport?.channel || "sse",
  ).toLowerCase();
  const jobId = String(
    phasePayload?.jobId ||
      phasePayload?.job_id ||
      sessionStatusPayload?.latestJobId ||
      sessionStatusPayload?.latest_job_id ||
      "",
  );
  const appendId = Math.max(
    Number(
      phasePayload?.appendId ||
        phasePayload?.append_id ||
        sessionStatusPayload?.appendId ||
        sessionStatusPayload?.append_id ||
        0,
    ),
    0,
  );

  if (rawPhase === "FAILED" || pathVerdict === "DEGRADED" || blockerReason !== "none") {
    return {
      visible: true,
      state: "failed",
      phase: "FAILED",
      detail: "선택된 대화의 authoritative SSE session status가 실패 또는 degraded 상태를 보고했습니다.",
      source: phaseSource,
      tone: "done",
      jobId,
      terminal: true,
      appendId,
      authoritative: true,
      reason: blockerReason || "degraded",
    };
  }
  if (eventType === "goal.proposal.auto_apply.started") {
    return {
      visible: true,
      state: "auto-apply",
      phase: "AUTO APPLY",
      detail: "선택된 대화의 authoritative SSE session status가 자동 적용 단계를 보고했습니다.",
      source: phaseSource,
      tone: "waiting",
      jobId,
      terminal: false,
      appendId,
      authoritative: true,
      reason: "session-status-phase",
    };
  }
  if (rawPhase === "VERIFY") {
    return {
      visible: true,
      state: "verify-phase",
      phase: "VERIFY",
      detail: "선택된 대화의 authoritative SSE session status가 검증 단계를 보고했습니다.",
      source: phaseSource,
      tone: "running",
      jobId,
      terminal: false,
      appendId,
      authoritative: true,
      reason: "session-status-phase",
    };
  }
  if (rawPhase === "REVIEW") {
    return {
      visible: true,
      state: "review-phase",
      phase: "REVIEW",
      detail: "선택된 대화의 authoritative SSE session status가 리뷰 단계를 보고했습니다.",
      source: phaseSource,
      tone: "thinking",
      jobId,
      terminal: false,
      appendId,
      authoritative: true,
      reason: "session-status-phase",
    };
  }
  if (rawPhase === "PROPOSAL") {
    return {
      visible: true,
      state: "proposal-phase",
      phase: "PROPOSAL",
      detail: "선택된 대화의 authoritative SSE session status가 제안 단계를 보고했습니다.",
      source: phaseSource,
      tone: "thinking",
      jobId,
      terminal: false,
      appendId,
      authoritative: true,
      reason: "session-status-phase",
    };
  }
  if (proposalReady || proposalStatus === "ready_to_apply" || rawPhase === "READY") {
    return {
      visible: true,
      state: "proposal-ready",
      phase: "READY",
      detail: "선택된 대화의 authoritative SSE session status가 ready 상태를 보고했습니다.",
      source: phaseSource,
      tone: "waiting",
      jobId,
      terminal: true,
      appendId,
      authoritative: true,
      reason: "session-status-ready",
    };
  }
  if (proposalStatus === "applied" || rawPhase === "APPLIED") {
    return {
      visible: true,
      state: "applied",
      phase: "APPLIED",
      detail: "선택된 대화의 authoritative SSE session status가 applied 상태를 보고했습니다.",
      source: phaseSource,
      tone: "done",
      jobId,
      terminal: true,
      appendId,
      authoritative: true,
      reason: "session-status-applied",
    };
  }
  if (rawPhase === "LIVE") {
    return {
      visible: true,
      state: "live",
      phase: "LIVE",
      detail: "선택된 대화가 authoritative SSE session status에 의해 live session으로 유지되고 있습니다.",
      source: phaseSource,
      tone: "running",
      jobId,
      terminal: false,
      appendId,
      authoritative: true,
      reason: "session-status-live",
    };
  }
  return {
    visible: true,
    state: "unknown",
    phase: rawPhase || "UNKNOWN",
    detail: "선택된 대화의 authoritative SSE session status가 아직 명시적 세션 단계를 확정하지 않았습니다.",
    source: phaseSource,
    tone: "idle",
    jobId,
    terminal: false,
    appendId,
    authoritative: true,
    reason: "session-status-unknown",
  };
}

export function isSelectedThreadSessionOwned(currentState, conversationId = "") {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, { conversation_id: conversationId });
  const targetConversationId = String(conversationId || sessionStatus.conversationId || "");
  const healthyPromotion = deriveSelectedThreadHealthyPromotionModel(currentState, { conversation_id: targetConversationId });
  const provisionalOwned =
    Boolean(sessionStatus.conversationId) &&
    (!targetConversationId || String(sessionStatus.conversationId || "") === targetConversationId) &&
    !sessionStatus.retrying &&
    !sessionStatus.sessionRotationDetected &&
    (
      sessionStatus.selectedThreadProvisional ||
      sessionStatus.selectedThreadRestore ||
      (sessionStatus.pendingHandoff && sessionStatus.selectedThreadSse)
    );
  return Boolean(
    provisionalOwned ||
      (
        healthyPromotion.promoted &&
        (!targetConversationId || String(healthyPromotion.conversationId || "") === targetConversationId)
      ),
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
