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
  const selectedThreadRestore =
    Boolean(savedConversationId) &&
    conversationId === savedConversationId &&
    !threadTransition.active &&
    (
      (!selectedThreadStream && transport === "sse" && (attachMode === "awaiting-bootstrap" || attachMode === "sse-resume")) ||
      (selectedThreadStream && renderSource !== "sse" && streamStatus === "connecting")
    );
  const restoreResume =
    selectedThreadRestore &&
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
    selectedThreadRestore,
    restoreResume,
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
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const followControl = deriveSelectedThreadFollowControlModel(currentState);
  const phaseLabel = String(deriveSelectedThreadShellPhaseLabel(currentState, conversation) || "").trim().toUpperCase();
  const conversationTitle = sessionStatus.conversationTitle || "현재 대화";
  if (sessionStatus.switchActive) {
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
      rowSource: "none",
      rowPhase: "IDLE",
      rowUnseenCount: 0,
    };
  }
  if (sessionStatus.pendingHandoff && sessionStatus.selectedThreadSse) {
    return {
      visible: true,
      conversationId: String(sessionStatus.conversationId || ""),
      presentation: "handoff",
      rowState: "handoff",
      ownerLabel: sessionStatus.transportLabel || "SSE OWNER",
      stateLabel: "HANDOFF",
      followLabel: "LIVE",
      title: conversationTitle,
      meta: "selected thread · handoff · awaiting first append",
      rowOwned: true,
      rowSource: "sse",
      rowPhase: "HANDOFF",
      rowUnseenCount: 0,
    };
  }
  if (sessionStatus.liveOwned) {
    const rowState = followControl.visible ? followControl.followState : "live";
    const followLabel = followControl.visible ? followControl.stateLabel : "LIVE";
    const rowPhase = phaseLabel || "LIVE";
    const rowUnseenCount = followControl.visible ? Math.max(Number(followControl.unseenCount || 0), 0) : 0;
    const meta =
      followControl.followState === "new" && rowUnseenCount > 0
        ? `selected thread · ${rowPhase.toLowerCase()} · ${rowUnseenCount} new`
        : followControl.followState === "paused"
          ? `selected thread · ${rowPhase.toLowerCase()} · ${followControl.detailLabel}`
          : `selected thread · ${rowPhase.toLowerCase()} · sse owner`;
    return {
      visible: true,
      conversationId: String(sessionStatus.conversationId || ""),
      presentation: "owned",
      rowState,
      ownerLabel: sessionStatus.transportLabel || "SSE OWNER",
      stateLabel: rowPhase,
      followLabel,
      title: conversationTitle,
      meta,
      rowOwned: true,
      rowSource: "sse",
      rowPhase,
      rowUnseenCount,
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
    rowSource: "none",
    rowPhase: "IDLE",
    rowUnseenCount: 0,
  };
}

export function deriveSelectedThreadLiveAutonomy(currentState, conversation = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const autonomySummary = currentState.autonomySummary;
  if (sessionStatus.presentation === "restore") {
    return {
      visible: true,
      owned: false,
      presentation: "restore",
      label: sessionStatus.transportLabel || "ATTACH",
      reason: sessionStatus.transportReason,
      source: sessionStatus.transport || "sse",
      freshnessState: String(autonomySummary?.freshnessState || "stale-or-missing").toLowerCase(),
      fallbackAllowed: false,
      summary: autonomySummary || null,
    };
  }
  if (!autonomySummary || typeof autonomySummary !== "object") {
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
      freshnessState: String(autonomySummary.freshnessState || "stale-or-missing").toLowerCase(),
      fallbackAllowed: Boolean(autonomySummary.fallbackAllowed ?? true),
      summary: autonomySummary,
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
      freshnessState: String(autonomySummary.freshnessState || "stale-or-missing").toLowerCase(),
      fallbackAllowed: Boolean(autonomySummary.fallbackAllowed ?? true),
      summary: autonomySummary,
    };
  }
  if (sessionStatus.liveOwned) {
    return {
      visible: true,
      owned: true,
      presentation: "owned",
      label: sessionStatus.transportLabel || "SSE OWNER",
      reason: sessionStatus.transportReason,
      source: String(autonomySummary.source || "sse").toLowerCase(),
      freshnessState: String(autonomySummary.freshnessState || "fresh").toLowerCase(),
      fallbackAllowed: Boolean(autonomySummary.fallbackAllowed ?? false),
      summary: autonomySummary,
    };
  }
  return {
    visible: false,
    owned: false,
    presentation: "cleared",
    label: "",
    reason: sessionStatus.clearReason,
    source: "none",
    freshnessState: String(autonomySummary.freshnessState || "stale-or-missing").toLowerCase(),
    fallbackAllowed: Boolean(autonomySummary.fallbackAllowed ?? true),
    summary: autonomySummary,
  };
}

export function deriveSelectedThreadPhaseProgression(currentState, conversation = null) {
  const sessionStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
  const appendStream = currentState.appendStream || {};
  const sessionPhase = appendStream.sessionPhase || {};
  const phaseValue = String(sessionPhase.value || "UNKNOWN").toUpperCase();
  const eventType = String(sessionPhase.eventType || sessionPhase.event_type || "");
  const phaseSource = String(sessionPhase.source || "none").toLowerCase();

  if (sessionStatus.presentation === "restore") {
    return {
      visible: true,
      label: sessionStatus.restoreResume ? "RESUME" : "ATTACH",
      state: sessionStatus.restoreResume ? "resume" : "attach",
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
    owned: sessionStatus.liveOwned,
    reason: sessionStatus.transportReason,
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
    { key: "ready", label: "READY", state: phaseRank > 4 ? "complete" : currentPhase === "AUTO APPLY" || currentPhase === "READY" ? "active" : "pending" },
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
  const liveAutonomy = deriveSelectedThreadLiveAutonomy(currentState, conversation);
  const phaseProgression = deriveSelectedThreadPhaseProgression(currentState, conversation);
  const milestoneModel = deriveSelectedThreadTimelineMilestones(currentState, conversation);
  const shellPhaseLabel = deriveSelectedThreadShellPhaseLabel(currentState, conversation);
  const liveOwned = Boolean(sessionStatus.liveOwned && liveAutonomy.owned && phaseProgression.visible);
  const degradedVisible = sessionStatus.transportState === "reconnect" || sessionStatus.transportState === "polling";
  const handoffVisible = Boolean(sessionStatus.pendingHandoff && sessionStatus.selectedThreadSse);
  const restoreVisible = Boolean(sessionStatus.presentation === "restore" && liveAutonomy.visible && phaseProgression.visible);
  const phaseLabel = degradedVisible
    ? String(sessionStatus.transportLabel || "POLLING").toUpperCase()
    : handoffVisible
      ? "HANDOFF"
      : String(shellPhaseLabel || phaseProgression.label || "").toUpperCase();
  const summary = liveAutonomy.summary || null;
  return {
    sessionStatus,
    liveAutonomy,
    phaseProgression,
    milestoneModel,
    liveOwned,
    degradedVisible,
    handoffVisible,
    restoreVisible,
    phaseLabel,
    pathVerdict: liveOwned ? String(summary?.pathVerdict || "UNKNOWN").toUpperCase() : "",
    verifierAcceptability: liveOwned ? String(summary?.verifierAcceptability || "PENDING").toUpperCase() : "",
    blockerReason: liveOwned ? String(summary?.blockerReason || "none").toUpperCase() : "",
    source: String(
      degradedVisible
        ? sessionStatus.transport || "polling"
        : restoreVisible
          ? phaseProgression.source || liveAutonomy.source || "sse"
          : phaseProgression.source || liveAutonomy.source || "none",
    ).toLowerCase(),
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

export function deriveSelectedThreadSessionStripModel(currentState, conversation = null, liveRun = null) {
  const selectedThreadStatus = deriveSelectedThreadSessionStatus(currentState, conversation);
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
  const owned = transportState === "sse-live";
  const degraded = transportState === "reconnecting" || transportState === "polling-fallback";
  const restore = attachMode === "sse-resume" || attachMode === "sse-bootstrap";
  const tone = owned ? "healthy" : degraded ? "warning" : restore ? "neutral" : "muted";
  const presentation = owned ? "healthy" : degraded ? "degraded" : restore ? "restore" : "cleared";
  const detail = degraded
    ? `selected thread ${pathStateLabel.toLowerCase()} · ${selectedThreadStatus.transportReason || "fallback"}`
    : restore
      ? `selected thread ${pathStateLabel.toLowerCase()} · bootstrap pending`
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
    degradedSignals,
    owned,
    source: String(sessionStatusPayload?.source || sessionStatusPayload?.transport?.channel || "append-sse").toLowerCase(),
    clearReason: "none",
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
