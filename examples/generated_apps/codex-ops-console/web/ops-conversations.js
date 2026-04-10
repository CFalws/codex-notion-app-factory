export function createConversationController(deps) {
  const {
    dom,
    state,
    selectedAppData,
    fetchJson,
    appConversationsUrl,
    appGoalsUrl,
    conversationUrl,
    setStatus,
    setJobMeta,
    renderConversation,
    buildAutonomySummary,
    renderAutonomySummary,
    clearAutonomySummary,
    clearLearningSummary,
    updateSelectedAppCard,
    updateProposalButton,
    persistSettings,
    syncLatestJob,
    ensurePollingForJob,
    stopPolling,
    normalizeBaseUrl,
    updateHeroState,
    renderWorkspaceSummary,
    restoreDraft,
    syncDraftStatus,
    internalConversationAppendStreamUrl,
    renderSessionStrip,
  } = deps;
  const RECENT_THREAD_LIMIT = 4;

  function clearPendingOutgoing(conversationId = "") {
    if (conversationId && state.pendingOutgoing?.conversationId !== conversationId) {
      return;
    }
    state.pendingOutgoing = {
      conversationId: "",
      body: "",
      createdAt: "",
      assistantCreatedAt: "",
      baselineAppendId: 0,
      status: "idle",
      source: "none",
    };
  }

  function showPendingOutgoing(conversationId, body) {
    if (!conversationId || !body) {
      return;
    }
    state.pendingOutgoing = {
      conversationId,
      body,
      createdAt: new Date().toISOString(),
      assistantCreatedAt: "",
      baselineAppendId: Math.max(Number(state.appendStream?.lastAppendId || 0), 0),
      status: "sending-user",
      source: "local-submit",
    };
    const baseConversation =
      state.conversationCache && state.conversationCache.conversation_id === conversationId
        ? state.conversationCache
        : {
            conversation_id: conversationId,
            title: "현재 대화",
            latest_job_id: state.currentJobId || "",
            messages: [],
            events: [],
          };
    renderConversation(dom, state, baseConversation, persistSettings);
    syncConversationCardState();
  }

  function shouldClearPendingOutgoing(conversation) {
    const pendingOutgoing = state.pendingOutgoing || {};
    if (!conversation?.conversation_id || pendingOutgoing.conversationId !== conversation.conversation_id) {
      return false;
    }
    const baselineAppendId = Number(pendingOutgoing.baselineAppendId || 0);
    const messages = Array.isArray(conversation.messages) ? conversation.messages : [];
    const events = Array.isArray(conversation.events) ? conversation.events : [];
    const hasAssistantResponse = messages.some(
      (message) => message.role === "assistant" && Number(message.append_id || 0) > baselineAppendId,
    );
    if (hasAssistantResponse) {
      return true;
    }
    return events.some((event) => {
      const appendId = Number(event.append_id || 0);
      if (appendId <= baselineAppendId) {
        return false;
      }
      const status = String(event.status || "").toLowerCase();
      const type = String(event.type || "");
      return (
        status === "failed" ||
        status === "completed" ||
        status === "applied" ||
        type === "runtime.exception" ||
        type === "job.completed" ||
        type === "proposal.ready" ||
        type === "codex.exec.applied"
      );
    });
  }

  function showPendingAssistant(conversationId, conversation = null) {
    const pendingOutgoing = state.pendingOutgoing || {};
    if (!conversationId || pendingOutgoing.conversationId !== conversationId) {
      return;
    }
    if (conversation && shouldClearPendingOutgoing(conversation)) {
      clearPendingOutgoing(conversationId);
      return;
    }
    state.pendingOutgoing = {
      ...pendingOutgoing,
      assistantCreatedAt: new Date().toISOString(),
      status: "awaiting-assistant",
      source: "accepted-event",
    };
  }

  function resetAppendStream(conversationId = "") {
    state.appendStream ||= {};
    state.appendStream.conversationId = conversationId;
    state.appendStream.status = "offline";
    state.appendStream.transport = "polling";
    state.appendStream.lastRenderSource = "snapshot";
    state.appendStream.lastLiveAppendId = 0;
    state.appendStream.attachMode = conversationId ? "snapshot-fallback" : "idle";
    state.appendStream.bootstrapVersion = "";
    if (!conversationId) {
      state.appendStream.lastAppendId = 0;
    }
  }

  function closeAppendStream() {
    if (state.appendStream?.source) {
      state.appendStream.source.close();
    }
    state.appendStream.source = null;
    resetAppendStream("");
    renderSessionStrip(dom, state, state.conversationCache);
    syncConversationCardState();
  }

  function syncAppendCursor(conversation) {
    state.appendStream ||= {};
    const messages = Array.isArray(conversation?.messages) ? conversation.messages : [];
    const events = Array.isArray(conversation?.events) ? conversation.events : [];
    const lastAppendId = [...messages, ...events].reduce((maxValue, item) => {
      const appendId = Number(item?.append_id || 0);
      return appendId > maxValue ? appendId : maxValue;
    }, 0);
    state.appendStream.lastAppendId = lastAppendId;
    state.appendStream.lastRenderSource = "snapshot";
    return lastAppendId;
  }

  function appendLiveItem(appendEnvelope) {
    const activeConversationId = state.currentConversationId;
    if (!activeConversationId || !state.conversationCache) {
      return false;
    }
    if (appendEnvelope.conversation_id !== activeConversationId) {
      return false;
    }

    const appendId = Number(appendEnvelope.append_id || 0);
    if (!appendId || appendId <= Number(state.appendStream?.lastAppendId || 0)) {
      return false;
    }

    const payload = appendEnvelope.payload;
    if (!payload || typeof payload !== "object") {
      return false;
    }
    const livePayload = { ...payload, delivery_source: "sse" };
    const liveJobId = String(livePayload.job_id || "").trim();

    const conversation = {
      ...state.conversationCache,
      messages: Array.isArray(state.conversationCache.messages) ? [...state.conversationCache.messages] : [],
      events: Array.isArray(state.conversationCache.events) ? [...state.conversationCache.events] : [],
    };
    const duplicate = [...conversation.messages, ...conversation.events].some(
      (item) => Number(item?.append_id || 0) === appendId,
    );
    if (duplicate) {
      state.appendStream.lastAppendId = Math.max(Number(state.appendStream.lastAppendId || 0), appendId);
      return false;
    }

    if (appendEnvelope.kind === "message") {
      conversation.messages.push(livePayload);
    } else if (appendEnvelope.kind === "event") {
      conversation.events.push(livePayload);
    } else {
      return false;
    }
    if (liveJobId) {
      state.currentJobId = liveJobId;
      conversation.latest_job_id = liveJobId;
    }

    if (appendEnvelope.kind === "message" && livePayload.role === "assistant") {
      clearPendingOutgoing(activeConversationId);
    }
    if (appendEnvelope.kind === "event") {
      const eventStatus = String(livePayload.status || "").toLowerCase();
      const eventType = String(livePayload.type || "");
      if (
        eventStatus === "failed" ||
        eventStatus === "completed" ||
        eventStatus === "applied" ||
        eventType === "runtime.exception" ||
        eventType === "job.completed" ||
        eventType === "proposal.ready" ||
        eventType === "codex.exec.applied"
      ) {
        clearPendingOutgoing(activeConversationId);
      }
    }
    state.appendStream.lastAppendId = appendId;
    state.appendStream.lastLiveAppendId = appendId;
    state.appendStream.transport = "sse";
    state.appendStream.status = "live";
    state.appendStream.lastRenderSource = "sse";
    stopPolling();
    renderConversation(dom, state, conversation, persistSettings);
    syncConversationCardState();
    restoreDraft();
    syncDraftStatus();
    syncSelectedSessionFromLiveAppend(appendEnvelope.kind, livePayload);
    return true;
  }

  function shouldProjectAutonomySummaryFromLiveAppend(kind, payload) {
    if (kind !== "event" || !payload) {
      return false;
    }
    const type = String(payload.type || "");
    const status = String(payload.status || "").toLowerCase();
    return (
      type === "job.running" ||
      type === "proposal.ready" ||
      type.startsWith("goal.proposal.phase.") ||
      type.startsWith("goal.review.phase.") ||
      type.startsWith("goal.verify.phase.") ||
      type === "goal.proposal.auto_apply.started" ||
      type === "runtime.exception" ||
      type === "codex.exec.applied" ||
      status === "failed" ||
      status === "completed" ||
      status === "applied"
    );
  }

  function projectAutonomySummaryFromLiveAppend(kind, payload) {
    if (!shouldProjectAutonomySummaryFromLiveAppend(kind, payload)) {
      return state.autonomySummary;
    }
    const currentSummary = state.autonomySummary || {};
    const type = String(payload?.type || "");
    const status = String(payload?.status || "").toLowerCase();
    const degradedSignals = Array.isArray(currentSummary.degradedSignals)
      ? [...currentSummary.degradedSignals]
      : [];
    let pathVerdict = String(currentSummary.pathVerdict || "EXPECTED").toUpperCase();
    let verifierAcceptability = String(currentSummary.verifierAcceptability || "PENDING").toUpperCase();
    let blockerReason = String(currentSummary.blockerReason || "none");

    if (
      type === "runtime.exception" ||
      status === "failed"
    ) {
      pathVerdict = "DEGRADED";
      verifierAcceptability = "DISQUALIFYING";
      blockerReason = type === "runtime.exception" ? "runtime.exception" : "failed";
      if (!degradedSignals.includes(blockerReason)) {
        degradedSignals.push(blockerReason);
      }
    } else if (
      type === "proposal.ready" ||
      type === "codex.exec.applied" ||
      status === "applied" ||
      status === "completed"
    ) {
      pathVerdict = "EXPECTED";
      verifierAcceptability = "ACCEPTABLE";
      blockerReason = "none";
    } else if (
      type === "job.running" ||
      type.startsWith("goal.proposal.phase.") ||
      type.startsWith("goal.review.phase.") ||
      type.startsWith("goal.verify.phase.") ||
      type === "goal.proposal.auto_apply.started"
    ) {
      pathVerdict = "EXPECTED";
      verifierAcceptability = "PENDING";
      blockerReason = "none";
    }

    const nextSummary = {
      goalTitle: currentSummary.goalTitle || "Autonomy Goal",
      goalStatus: currentSummary.goalStatus || "running",
      iteration: String(currentSummary.iteration || ""),
      pathVerdict,
      verifierAcceptability,
      blockerReason,
      expectedPath: currentSummary.expectedPath || "selected-thread-sse",
      degradedSignals,
      heading:
        currentSummary.heading ||
        `${currentSummary.goalTitle || "Autonomy Goal"} · ${currentSummary.goalStatus || "running"} · iteration ${String(currentSummary.iteration || "")}`,
    };
    return nextSummary;
  }

  function liveJobMetaLabel(kind, payload) {
    if (!payload || kind !== "event") {
      return "";
    }
    const type = String(payload.type || "");
    const status = String(payload.status || "").toLowerCase();
    const jobId = String(payload.job_id || state.currentJobId || "").trim();
    const suffix = jobId ? ` · ${jobId}` : "";
    if (type === "job.running") {
      return `RUNNING${suffix}`;
    }
    if (type.startsWith("goal.proposal.phase.")) {
      return `PROPOSAL${suffix}`;
    }
    if (type.startsWith("goal.review.phase.")) {
      return `REVIEW${suffix}`;
    }
    if (type.startsWith("goal.verify.phase.")) {
      return `VERIFY${suffix}`;
    }
    if (type === "goal.proposal.auto_apply.started") {
      return `AUTO APPLY${suffix}`;
    }
    if (type === "proposal.ready") {
      return `READY${suffix}`;
    }
    if (type === "codex.exec.applied" || status === "applied") {
      return `APPLIED${suffix}`;
    }
    if (type === "runtime.exception" || status === "failed") {
      return `FAILED${suffix}`;
    }
    if (status === "completed") {
      return `DONE${suffix}`;
    }
    return "";
  }

  function syncSelectedSessionFromLiveAppend(kind, payload) {
    if (
      !state.currentConversationId ||
      !state.conversationCache ||
      !state.appendStream ||
      state.appendStream.conversationId !== state.currentConversationId ||
      state.appendStream.transport !== "sse" ||
      state.appendStream.lastRenderSource !== "sse" ||
      state.appendStream.status !== "live"
    ) {
      return;
    }
    const liveJobId = String(payload?.job_id || "").trim();
    if (liveJobId) {
      state.currentJobId = liveJobId;
      state.conversationCache.latest_job_id = liveJobId;
    }
    const immediateMeta = liveJobMetaLabel(kind, payload);
    if (immediateMeta) {
      setJobMeta(dom, immediateMeta);
    }
    const projectedAutonomySummary = projectAutonomySummaryFromLiveAppend(kind, payload);
    if (projectedAutonomySummary !== state.autonomySummary) {
      state.autonomySummary = projectedAutonomySummary;
      if (state.conversationCache) {
        renderConversation(dom, state, state.conversationCache, persistSettings);
      }
    }
  }

  function connectAppendStream(conversationId, options = {}) {
    const { awaitBootstrap = false } = options;
    closeAppendStream();
    if (!conversationId || typeof window === "undefined" || typeof window.EventSource !== "function") {
      state.appendStream.attachMode = "snapshot-fallback";
      return Promise.resolve(null);
    }

    let openedOnce = false;
    let settled = false;
    let bootstrapPayload = null;
    let bootstrapTimeoutId = null;
    const settle = (value) => {
      if (settled) {
        return;
      }
      settled = true;
      if (bootstrapTimeoutId !== null) {
        window.clearTimeout(bootstrapTimeoutId);
      }
      bootstrapResolver(value);
    };
    let bootstrapResolver = () => {};
    const bootstrapPromise = new Promise((resolve) => {
      bootstrapResolver = resolve;
    });
    state.appendStream.source = new window.EventSource(internalConversationAppendStreamUrl(conversationId));
    state.appendStream.conversationId = conversationId;
    state.appendStream.status = "connecting";
    state.appendStream.transport = "sse";
    state.appendStream.lastRenderSource = "snapshot";
    state.appendStream.attachMode = "awaiting-bootstrap";
    state.appendStream.bootstrapVersion = "";
    renderSessionStrip(dom, state, state.conversationCache);
    syncConversationCardState();
    if (awaitBootstrap) {
      bootstrapTimeoutId = window.setTimeout(() => {
        state.appendStream.attachMode = "snapshot-fallback";
        settle(null);
      }, 1500);
    }

    state.appendStream.source.addEventListener("open", () => {
      if (state.appendStream?.conversationId !== conversationId) {
        return;
      }
      openedOnce = true;
      state.appendStream.status = "live";
      stopPolling();
      renderSessionStrip(dom, state, state.conversationCache);
      syncConversationCardState();
    });

    state.appendStream.source.addEventListener("session.bootstrap", (event) => {
      if (state.appendStream?.conversationId !== conversationId) {
        return;
      }
      try {
        const payload = JSON.parse(event.data || "{}");
        if (String(payload.conversation_id || "") !== conversationId) {
          return;
        }
        bootstrapPayload = payload;
        state.appendStream.lastAppendId = Math.max(
          Number(state.appendStream.lastAppendId || 0),
          Number(payload.append_cursor || 0),
        );
        state.appendStream.lastRenderSource = "sse";
        state.appendStream.attachMode = String(payload.attach_mode || "sse-bootstrap");
        state.appendStream.bootstrapVersion = String(payload.version || "");
        renderSessionStrip(dom, state, state.conversationCache);
        syncConversationCardState();
        settle(payload);
      } catch (_) {
        state.appendStream.attachMode = "snapshot-fallback";
        settle(null);
      }
    });

    state.appendStream.source.addEventListener("conversation.append", (event) => {
      if (state.currentConversationId !== conversationId || state.appendStream?.conversationId !== conversationId) {
        return;
      }
      try {
        const payload = JSON.parse(event.data || "{}");
        appendLiveItem(payload);
      } catch (_) {
        // Keep the existing timeline and let the next poll-driven refresh recover if needed.
      }
    });

    state.appendStream.source.addEventListener("error", () => {
      if (state.appendStream?.conversationId !== conversationId) {
        return;
      }
      if (!openedOnce || (awaitBootstrap && !bootstrapPayload)) {
        state.appendStream.attachMode = "snapshot-fallback";
        settle(null);
        closeAppendStream();
        ensurePollingForJob();
        return;
      }
      state.appendStream.status = "reconnecting";
      state.appendStream.attachMode = "snapshot-fallback";
      ensurePollingForJob();
      renderSessionStrip(dom, state, state.conversationCache);
      syncConversationCardState();
    });

    return bootstrapPromise;
  }

  function pickRelevantGoal(goals) {
    const items = Array.isArray(goals) ? goals.slice() : [];
    if (!items.length) {
      return null;
    }
    items.sort((left, right) => {
      const leftStamp = left.updated_at || left.completed_at || left.created_at || "";
      const rightStamp = right.updated_at || right.completed_at || right.created_at || "";
      return leftStamp < rightStamp ? 1 : -1;
    });
    return (
      items.find((goal) => goal.status === "running") ||
      items.find((goal) => goal.status === "paused") ||
      items[0]
    );
  }

  function simplifyPreviewText(value) {
    return String(value || "")
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1")
      .replace(/`([^`]+)`/g, "$1")
      .replace(/\*\*/g, "")
      .replace(/^#{1,3}\s+/gm, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function escapeHtml(value) {
    return String(value || "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function snapshotThreadState(conversation) {
    const events = Array.isArray(conversation?.events) ? conversation.events : [];
    const latestEvent = events.length ? events[events.length - 1] : null;
    const latestType = String(latestEvent?.type || "");
    const latestStatus = String(latestEvent?.status || "").toLowerCase();
    if (latestStatus === "failed" || latestType === "runtime.exception") {
      return "failed";
    }
    if (latestType === "proposal.ready") {
      return "ready";
    }
    if (latestType === "goal.verify.phase.started") {
      return "verify";
    }
    if (latestType === "goal.review.phase.started") {
      return "review";
    }
    if (latestType === "goal.proposal.phase.started" || latestType === "goal.proposal.auto_apply.started") {
      return "proposal";
    }
    if (latestType === "message.accepted" || latestType === "job.queued") {
      return "waiting";
    }
    if (latestType === "job.running" || latestType === "codex.exec.started") {
      return "running-tool";
    }
    if (
      latestType === "job.completed" ||
      latestType === "codex.exec.applied" ||
      latestStatus === "completed" ||
      latestStatus === "applied"
    ) {
      return "done";
    }
    return "idle";
  }

  function snapshotThreadLabel(threadState) {
    if (threadState === "failed") {
      return "FAILED";
    }
    if (threadState === "ready") {
      return "READY";
    }
    if (threadState === "verify") {
      return "VERIFY";
    }
    if (threadState === "review") {
      return "REVIEW";
    }
    if (threadState === "proposal") {
      return "PROPOSAL";
    }
    if (threadState === "waiting") {
      return "WAITING";
    }
    if (threadState === "running-tool") {
      return "ACTIVE";
    }
    if (threadState === "done") {
      return "DONE";
    }
    return "IDLE";
  }

  function compactConversationLabel({ presentation = "", liveRunState = "", liveRunPhase = "", pendingStage = "", isSelected = false } = {}) {
    if (!isSelected) {
      return snapshotThreadLabel(liveRunState);
    }
    if (pendingStage === "pending-user" || pendingStage === "pending-assistant") {
      return "HANDOFF";
    }
    if (presentation === "connecting") {
      return "CONNECT";
    }
    if (presentation === "reconnecting") {
      return "RESUME";
    }
    if (presentation === "terminal") {
      if (liveRunState === "failed" || liveRunPhase === "FAILED") {
        return "FAILED";
      }
      return liveRunPhase || "DONE";
    }
    if (presentation === "live") {
      if (liveRunPhase) {
        return liveRunPhase;
      }
      if (liveRunState === "sending" || liveRunState === "generating") {
        return "LIVE";
      }
      if (liveRunState === "running-tool" || liveRunState === "running tool") {
        return "RUN";
      }
      return "LIVE";
    }
    return "ACTIVE";
  }

  function liveOwnerLabel(liveLabel = "") {
    if (liveLabel) {
      return "OWNER";
    }
    return "LIVE";
  }

  function liveOwnerDetail({ pendingStage = "", presentation = "", liveRunState = "", liveRunPhase = "" } = {}) {
    if (pendingStage === "pending-user") {
      return "HANDOFF";
    }
    if (pendingStage === "pending-assistant") {
      return "HANDOFF";
    }
    if (presentation === "connecting") {
      return "PAUSED";
    }
    if (presentation === "reconnecting") {
      return "PAUSED";
    }
    if (liveRunState || liveRunPhase) {
      return "LIVE";
    }
    return "LIVE";
  }

  function liveOwnerFollowLabel({ pendingStage = "", isFollowing = false, jumpVisible = false, presentation = "" } = {}) {
    if (pendingStage === "pending-user" || pendingStage === "pending-assistant") {
      return "HANDOFF";
    }
    if (presentation === "reconnecting") {
      return "PAUSED";
    }
    if (jumpVisible) {
      return "NEW";
    }
    if (isFollowing) {
      return "LIVE";
    }
    return "PAUSED";
  }

  function liveOwnerState({ pendingStage = "", presentation = "", isFollowing = false, jumpVisible = false } = {}) {
    if (pendingStage === "pending-user" || pendingStage === "pending-assistant") {
      return "handoff";
    }
    if (jumpVisible) {
      return "new";
    }
    if (presentation === "reconnecting" || !isFollowing) {
      return "paused";
    }
    return "live";
  }

  function liveOwnerMarkerLabel(liveState = "") {
    if (liveState === "handoff") {
      return "HANDOFF";
    }
    if (liveState === "new") {
      return "NEW";
    }
    if (liveState === "paused") {
      return "PAUSED";
    }
    return "LIVE";
  }

  function syncActiveSessionRow({
    selectedConversationId = "",
    liveConversationId = "",
    presentation = "cleared",
    liveRunState = "done",
    liveRunPhase = "",
    pendingStage = "idle",
    jumpVisible = false,
    isFollowing = false,
    unseenCount = 0,
    sessionTerminal = false,
    renderSource = "snapshot",
  } = {}) {
    if (
      !dom.activeSessionRow ||
      !dom.activeSessionOwner ||
      !dom.activeSessionState ||
      !dom.activeSessionFollow ||
      !dom.activeSessionTitle ||
      !dom.activeSessionMeta
    ) {
      return;
    }

    const threadTransition = state.threadTransition || {};
    const summaryLiveOwned = String(dom.sessionSummaryRow?.dataset.liveSessionOwned || "false") === "true";
    const summaryLiveSource = String(dom.sessionSummaryRow?.dataset.liveSessionSource || "none");
    const summaryLiveState = String(dom.sessionSummaryRow?.dataset.liveSessionState || "idle");
    const summaryLiveReason = String(dom.sessionSummaryRow?.dataset.liveSessionReason || "idle");
    const summaryStateLabel = String(dom.sessionSummaryState?.textContent || "").trim().toUpperCase();
    const sessionIndicatorLabel = String(dom.sessionLiveIndicator?.textContent || "").trim().toUpperCase();
    const healthySelectedSessionMirror =
      Boolean(selectedConversationId) &&
      !sessionTerminal &&
      !threadTransition.active &&
      summaryLiveOwned &&
      summaryLiveSource === "sse" &&
      sessionIndicatorLabel === "SSE OWNER";

    let visible = false;
    let conversationId = "";
    let rowState = "idle";
    let ownerLabel = "OWNER";
    let stateLabel = summaryStateLabel || "LIVE";
    let followLabel = "LIVE";
    let title = "";
    let meta = "";
    let rowOwned = false;
    let rowSource = "none";
    let rowPhase = "IDLE";
    let rowUnseenCount = 0;

    if (healthySelectedSessionMirror) {
      visible = true;
      conversationId = selectedConversationId;
      rowState = summaryLiveState === "paused" ? "paused" : "live";
      stateLabel = summaryStateLabel || liveRunPhase || "LIVE";
      followLabel = jumpVisible ? "NEW" : summaryLiveState === "paused" ? "PAUSED" : "LIVE";
      rowOwned = true;
      rowSource = summaryLiveSource;
      rowPhase = stateLabel;
      rowUnseenCount = jumpVisible ? Math.max(Number(unseenCount || 0), 0) : 0;
      title =
        threadTitleForConversation(selectedConversationId) ||
        String(dom.threadTitle?.textContent || "").trim() ||
        "현재 대화";
      meta =
        jumpVisible && rowUnseenCount > 0
          ? `selected thread · ${stateLabel.toLowerCase()} · ${rowUnseenCount} new`
          : summaryLiveReason === "selected-thread-follow-paused"
            ? `selected thread · ${stateLabel.toLowerCase()} · follow paused`
            : `selected thread · ${stateLabel.toLowerCase()} · sse owner`;
    }

    dom.activeSessionRow.hidden = !visible;
    dom.activeSessionRow.dataset.activeSessionState = visible ? rowState : "idle";
    dom.activeSessionRow.dataset.activeSessionConversationId = visible ? conversationId : "";
    dom.activeSessionRow.dataset.activeSessionPresentation = visible ? presentation : "cleared";
    dom.activeSessionRow.dataset.activeSessionFollow = visible ? followLabel.toLowerCase() : "idle";
    dom.activeSessionRow.dataset.activeSessionOwned = visible ? String(rowOwned) : "false";
    dom.activeSessionRow.dataset.activeSessionSource = visible ? rowSource : "none";
    dom.activeSessionRow.dataset.activeSessionPhase = visible ? rowPhase : "IDLE";
    dom.activeSessionRow.dataset.activeSessionUnseenCount = String(visible ? rowUnseenCount : 0);
    dom.activeSessionOwner.textContent = ownerLabel;
    dom.activeSessionState.textContent = stateLabel;
    dom.activeSessionFollow.textContent = followLabel;
    dom.activeSessionTitle.textContent = visible ? title : "선택된 대화";
    dom.activeSessionMeta.textContent = visible ? meta : "selected thread";
  }

  function clearThreadTransition() {
    state.threadTransition = {
      active: false,
      targetConversationId: "",
      targetTitle: "",
      sourceConversationId: "",
      startedAt: "",
    };
  }

  function syncSelectedAppSession({ detectRotation }) {
    const app = selectedAppData(dom);
    if (!app?.appId) {
      state.appSession = {
        appId: "",
        sessionId: "",
        previousSessionId: "",
        rotationDetected: false,
        rotationDetectedAt: "",
      };
      return;
    }

    const previous = state.appSession || {};
    const previousSessionId = previous.appId === app.appId ? String(previous.sessionId || "") : "";
    const nextSessionId = String(app.sessionId || "");
    const rotationDetected =
      Boolean(detectRotation) &&
      Boolean(previousSessionId) &&
      Boolean(nextSessionId) &&
      previousSessionId !== nextSessionId;
    state.appSession = {
      appId: app.appId,
      sessionId: nextSessionId,
      previousSessionId: rotationDetected ? previousSessionId : "",
      rotationDetected,
      rotationDetectedAt: rotationDetected ? new Date().toISOString() : "",
    };
  }

  function threadTitleForConversation(conversationId = "") {
    if (!conversationId || !dom.conversationList) {
      return "";
    }
    const card = dom.conversationList.querySelector(`[data-conversation-id="${conversationId}"]`);
    const title = card?.querySelector(".conversation-card-title")?.textContent || "";
    return String(title).trim();
  }

  function startThreadTransition(conversationId) {
    state.threadTransition = {
      active: Boolean(conversationId),
      targetConversationId: conversationId || "",
      targetTitle: threadTitleForConversation(conversationId) || "대화",
      sourceConversationId: state.currentConversationId || "",
      startedAt: new Date().toISOString(),
    };
  }

  function truncatePreview(value, maxLength = 72) {
    const text = simplifyPreviewText(value);
    if (text.length <= maxLength) {
      return text;
    }
    return `${text.slice(0, maxLength - 1).trimEnd()}…`;
  }

  function compactRailTitle(value) {
    return truncatePreview(value || "대화", 22) || "대화";
  }

  function latestMessagePreview(conversation) {
    const messages = Array.isArray(conversation?.messages) ? conversation.messages : [];
    if (!messages.length) {
      return "";
    }
    const latestMessage = messages.slice().sort((left, right) => {
      const leftAppend = Number(left?.append_id || 0);
      const rightAppend = Number(right?.append_id || 0);
      if (leftAppend !== rightAppend) {
        return rightAppend - leftAppend;
      }
      const leftCreated = String(left?.created_at || "");
      const rightCreated = String(right?.created_at || "");
      return rightCreated.localeCompare(leftCreated);
    })[0];
    const body = truncatePreview(latestMessage?.body || "");
    if (latestMessage?.role === "assistant") {
      return body || "최근 assistant 응답이 있습니다.";
    }
    if (latestMessage?.role === "user") {
      return `사용자: ${body || "최근 요청이 있습니다."}`;
    }
    return body;
  }

  function eventPreview(item) {
    const body = truncatePreview(item?.body || "");
    const type = String(item?.type || "");
    if (type === "message.accepted") {
      return "메시지가 접수되어 첫 응답을 기다리는 중입니다.";
    }
    if (type === "job.queued") {
      return "작업이 대기열에 올라 있습니다.";
    }
    if (type === "job.running" || type === "codex.exec.started") {
      return "최근 작업이 현재 진행 중입니다.";
    }
    if (type === "goal.proposal.phase.started") {
      return "제안 단계가 진행 중입니다.";
    }
    if (type === "goal.review.phase.started") {
      return "리뷰 단계가 진행 중입니다.";
    }
    if (type === "goal.verify.phase.started") {
      return "검증 단계가 진행 중입니다.";
    }
    if (type === "goal.proposal.auto_apply.started") {
      return "자동 적용 단계가 진행 중입니다.";
    }
    if (type === "proposal.ready") {
      return "제안이 준비되었습니다.";
    }
    if (type === "codex.exec.applied") {
      return "제안이 적용되었습니다.";
    }
    if (type === "job.completed") {
      return "최근 작업이 완료되었습니다.";
    }
    if (type === "runtime.exception") {
      return "최근 실행에서 예외가 기록되었습니다.";
    }
    return body || "최근 이벤트가 기록되었습니다.";
  }

  function conversationPreview(conversation) {
    const messagePreview = latestMessagePreview(conversation);
    if (messagePreview) {
      return messagePreview;
    }
    const events = Array.isArray(conversation?.events) ? conversation.events : [];
    if (!events.length) {
      return "아직 메시지나 이벤트가 없습니다.";
    }
    return eventPreview(events[events.length - 1]);
  }

  function renderRecentThreadRail(conversations, selectedConversationId = "") {
    if (!dom.recentThreadRail || !dom.recentThreadRailList || !dom.recentThreadRailCopy) {
      return;
    }

    const recentConversations = Array.isArray(conversations) ? conversations.slice(0, RECENT_THREAD_LIMIT) : [];
    state.recentConversations = recentConversations.map((conversation) => ({
      conversation_id: conversation.conversation_id,
      title: conversation.title || "대화",
      updated_at: conversation.updated_at || "",
      snapshotState: snapshotThreadState(conversation),
    }));

    if (!recentConversations.length) {
      dom.recentThreadRail.hidden = true;
      dom.recentThreadRail.dataset.recentThreadCount = "0";
      dom.recentThreadRailList.innerHTML = "";
      dom.recentThreadRailCopy.textContent = "현재 대화와 최근 대화를 여기에서 바로 전환합니다.";
      return;
    }

    dom.recentThreadRail.hidden = false;
    dom.recentThreadRail.dataset.recentThreadCount = String(recentConversations.length);
    dom.recentThreadRailCopy.textContent = "현재 대화와 최근 대화를 여기에서 바로 전환합니다.";
    dom.recentThreadRailList.innerHTML = recentConversations
      .map((conversation) => {
        const isSelected = conversation.conversation_id === selectedConversationId;
        const snapshotState = snapshotThreadState(conversation);
        const snapshotLabel = snapshotThreadLabel(snapshotState);
        return `
          <button
            type="button"
            class="recent-thread-chip${isSelected ? " active" : ""}"
            data-recent-thread-chip="true"
            data-conversation-id="${conversation.conversation_id}"
            data-selected="${isSelected ? "true" : "false"}"
            data-thread-state="${snapshotState}"
            data-live-owner="false"
            data-live-owner-state="idle"
            data-snapshot-thread-state="${snapshotState}"
            data-snapshot-state-label="${snapshotLabel}"
          >
            <span class="recent-thread-chip-title">${escapeHtml(compactRailTitle(conversation.title))}</span>
            <span class="recent-thread-chip-row">
              <span class="recent-thread-token" data-recent-thread-marker ${isSelected ? "" : "hidden"}>NOW</span>
              <span class="recent-thread-token" data-recent-thread-owner hidden>OWNER</span>
              <span class="recent-thread-token" data-recent-thread-state>${snapshotLabel}</span>
              <span class="recent-thread-token" data-recent-thread-follow hidden></span>
            </span>
          </button>
        `;
      })
      .join("");
  }

  function syncConversationCardState() {
    const selectedConversationId = state.currentConversationId || state.savedConversationId || "";
    const liveConversationId = String(dom.threadScroller?.dataset.liveConversationId || "");
    const presentation = String(dom.threadScroller?.dataset.sessionPresentation || "cleared");
    const liveRunState = String(dom.threadScroller?.dataset.liveRunState || "done");
    const liveRunPhase = String(dom.threadScroller?.dataset.liveRunPhase || "");
    const renderSource = String(dom.threadScroller?.dataset.renderSource || "snapshot");
    const pendingStage = String(dom.threadScroller?.dataset.pendingHandoffStage || "idle");
    const sessionTerminal = String(dom.threadScroller?.dataset.sessionTerminal || "false") === "true";
    const liveFollow = state.liveFollow || {};
    const threadTransition = state.threadTransition || {};
    const jumpVisible = Boolean(liveFollow.jumpVisible);
    const isFollowing = Boolean(liveFollow.isFollowing);

    let liveLabel = "";
    let liveThreadState = "";
    let liveDetail = "";
    let liveFollowLabel = "";
    let liveOwnerStateLabel = "";
    let showLiveMirror = false;
    const selectedThreadSseOwned = selectedConversationId && selectedConversationId === liveConversationId && renderSource === "sse";
    const hasSelectedThreadState =
      selectedConversationId &&
      !sessionTerminal &&
      (pendingStage === "pending-user" || pendingStage === "pending-assistant" || selectedThreadSseOwned);
    if (hasSelectedThreadState) {
      liveThreadState =
        pendingStage === "pending-user" || pendingStage === "pending-assistant"
          ? "active"
          : presentation === "live"
            ? (liveRunState || "active")
            : presentation || "active";
      liveLabel = compactConversationLabel({
        presentation,
        liveRunState,
        liveRunPhase,
        pendingStage,
        isSelected: true,
      });
      liveDetail = liveOwnerDetail({ pendingStage, presentation, liveRunState, liveRunPhase });
      liveFollowLabel = liveOwnerFollowLabel({ pendingStage, isFollowing, jumpVisible, presentation });
      liveOwnerStateLabel = liveOwnerState({ pendingStage, presentation, isFollowing, jumpVisible });
      showLiveMirror = true;
    }

    for (const card of dom.conversationList.querySelectorAll("[data-conversation-id]")) {
      const isSelected = card.dataset.conversationId === selectedConversationId;
      const marker = card.querySelector("[data-conversation-marker]");
      const sessionMarker = card.querySelector("[data-conversation-session]");
      const liveState = card.querySelector("[data-conversation-live-state]");
      const liveDetailRow = card.querySelector("[data-conversation-live-owner-row]");
      const liveDetailText = card.querySelector("[data-conversation-live-detail]");
      const liveFollowText = card.querySelector("[data-conversation-live-follow]");
      const snapshotLabel = String(card.dataset.snapshotStateLabel || "IDLE");
      const snapshotState = String(card.dataset.snapshotThreadState || "idle");
      card.classList.toggle("active", isSelected);
      card.dataset.selected = isSelected ? "true" : "false";
      card.dataset.threadState = isSelected ? (liveThreadState || "active") : snapshotState;
      card.dataset.liveOwner = isSelected && showLiveMirror ? "true" : "false";
      card.dataset.liveOwnerState = isSelected && showLiveMirror ? liveOwnerStateLabel : "idle";
      if (marker) {
        marker.hidden = !isSelected;
        marker.textContent = isSelected && showLiveMirror ? liveOwnerMarkerLabel(liveOwnerStateLabel) : "NOW";
      }
      if (sessionMarker) {
        sessionMarker.hidden = !isSelected;
        sessionMarker.textContent = isSelected ? (showLiveMirror ? liveOwnerLabel(liveLabel) : snapshotLabel) : "";
      }
      if (liveState) {
        liveState.hidden = isSelected;
        liveState.textContent = snapshotLabel;
      }
      if (liveDetailRow) {
        liveDetailRow.hidden = !(isSelected && showLiveMirror);
        liveDetailRow.dataset.liveOwnerState = isSelected && showLiveMirror ? liveOwnerStateLabel : "idle";
      }
      if (liveDetailText) {
        liveDetailText.textContent = isSelected && showLiveMirror ? liveDetail : "";
      }
      if (liveFollowText) {
        liveFollowText.textContent = isSelected && showLiveMirror ? liveFollowLabel : "";
        liveFollowText.dataset.liveOwnerState = isSelected && showLiveMirror ? liveOwnerStateLabel : "idle";
      }
    }

    for (const chip of dom.recentThreadRailList?.querySelectorAll("[data-conversation-id]") || []) {
      const isSelected = chip.dataset.conversationId === selectedConversationId;
      const marker = chip.querySelector("[data-recent-thread-marker]");
      const owner = chip.querySelector("[data-recent-thread-owner]");
      const stateLabel = chip.querySelector("[data-recent-thread-state]");
      const follow = chip.querySelector("[data-recent-thread-follow]");
      const snapshotLabel = String(chip.dataset.snapshotStateLabel || "IDLE");
      const snapshotState = String(chip.dataset.snapshotThreadState || "idle");
      const isSwitching =
        isSelected &&
        Boolean(threadTransition.active) &&
        String(threadTransition.targetConversationId || "") === selectedConversationId;

      chip.classList.toggle("active", isSelected);
      chip.dataset.selected = isSelected ? "true" : "false";
      chip.dataset.threadState = isSwitching ? "switching" : isSelected ? (liveThreadState || "active") : snapshotState;
      chip.dataset.liveOwner = isSelected && showLiveMirror ? "true" : "false";
      chip.dataset.liveOwnerState = isSelected && showLiveMirror ? liveOwnerStateLabel : "idle";

      if (marker) {
        marker.hidden = !isSelected;
        marker.textContent = "NOW";
      }
      if (owner) {
        owner.hidden = !(isSelected && showLiveMirror);
        owner.textContent = "OWNER";
      }
      if (stateLabel) {
        stateLabel.textContent = isSwitching
          ? "SWITCHING"
          : isSelected
            ? (showLiveMirror
              ? compactConversationLabel({ presentation, liveRunState, liveRunPhase, pendingStage, isSelected: true })
              : snapshotLabel)
            : snapshotLabel;
      }
      if (follow) {
        follow.hidden = !(isSelected && (showLiveMirror || isSwitching));
        follow.textContent = isSwitching ? "ATTACH" : isSelected && showLiveMirror ? liveFollowLabel : "";
        follow.dataset.liveOwnerState = isSelected && showLiveMirror ? liveOwnerStateLabel : isSwitching ? "handoff" : "idle";
      }
    }

    syncActiveSessionRow({
      selectedConversationId,
      liveConversationId,
      presentation,
      liveRunState,
      liveRunPhase,
      pendingStage,
      jumpVisible,
      isFollowing,
      unseenCount: Number(liveFollow.pendingAppendCount || 0),
      sessionTerminal,
      renderSource,
    });
  }

  async function refreshGoalSummary() {
    const app = selectedAppData(dom);
    if (!app) {
      state.autonomySummary = null;
      clearAutonomySummary(dom, "앱을 선택하면 최근 autonomous iteration blocker가 여기에 표시됩니다.");
      if (state.conversationCache) {
        renderConversation(dom, state, state.conversationCache, persistSettings);
      }
      return;
    }
    try {
      const goals = await fetchJson(dom, appGoalsUrl(app.appId));
      const goal = pickRelevantGoal(goals);
      if (!goal) {
        state.autonomySummary = null;
        clearAutonomySummary(dom, "이 앱에는 아직 autonomous goal 기록이 없습니다.");
        if (state.conversationCache) {
          renderConversation(dom, state, state.conversationCache, persistSettings);
        }
        return;
      }
      state.autonomySummary = buildAutonomySummary(goal);
      renderAutonomySummary(dom, goal);
      if (state.conversationCache) {
        renderConversation(dom, state, state.conversationCache, persistSettings);
      }
    } catch (error) {
      state.autonomySummary = null;
      clearAutonomySummary(dom, `Autonomy summary를 불러오지 못했습니다: ${error.message}`);
      if (state.conversationCache) {
        renderConversation(dom, state, state.conversationCache, persistSettings);
      }
    }
  }

  function renderConversationList(conversations, selectedConversationId = "") {
    if (!conversations.length) {
      dom.conversationList.innerHTML = '<p class="conversation-list-empty">아직 대화가 없습니다.</p>';
      renderRecentThreadRail([], "");
      syncConversationCardState();
      return;
    }

    dom.conversationList.innerHTML = conversations
      .map((conversation) => {
        const isActive = conversation.conversation_id === selectedConversationId;
        const snapshotState = snapshotThreadState(conversation);
        return `
          <button
            type="button"
            class="conversation-card${isActive ? " active" : ""}"
            data-conversation-id="${conversation.conversation_id}"
            data-selected="${isActive ? "true" : "false"}"
            data-thread-state="${snapshotState}"
            data-snapshot-thread-state="${snapshotState}"
            data-snapshot-state-label="${snapshotThreadLabel(snapshotState)}"
          >
            <span class="conversation-card-head">
              <span class="conversation-card-title">${conversation.title}</span>
              <span class="conversation-card-tags">
                <span class="conversation-card-marker" data-conversation-marker ${isActive ? "" : "hidden"}>NOW</span>
                <span class="conversation-card-session" data-conversation-session ${isActive ? "" : "hidden"}>${isActive ? snapshotThreadLabel(snapshotState) : ""}</span>
              </span>
            </span>
            <span class="conversation-card-preview" data-preview-lines="1">${escapeHtml(conversationPreview(conversation))}</span>
            <span class="conversation-card-live-owner-row" data-conversation-live-owner-row hidden>
              <span class="conversation-card-live-detail" data-conversation-live-detail></span>
              <span class="conversation-card-live-follow" data-conversation-live-follow></span>
            </span>
            <span class="conversation-card-meta-row">
              <span class="conversation-card-meta">${new Date(conversation.updated_at).toLocaleString()}</span>
              <span class="conversation-card-live" data-conversation-live-state ${isActive ? "hidden" : ""}>${snapshotThreadLabel(snapshotState)}</span>
            </span>
          </button>
        `;
      })
      .join("");
    renderRecentThreadRail(conversations, selectedConversationId);
    syncConversationCardState();
  }

  async function loadConversations() {
    const app = selectedAppData(dom);
    const preferredConversationId = state.currentConversationId || state.savedConversationId || "";
    state.conversationCache = null;
    clearThreadTransition();
    closeAppendStream();

    if (!app) {
      clearPendingOutgoing();
      state.currentConversationId = "";
      state.savedConversationId = "";
      dom.conversationList.innerHTML = '<p class="conversation-list-empty">앱을 먼저 고르세요.</p>';
      renderRecentThreadRail([], "");
      clearAutonomySummary(dom, "앱을 선택하면 최근 autonomous iteration blocker가 여기에 표시됩니다.");
      updateHeroState(dom, {
        threadTitle: "앱을 먼저 고르세요",
        threadKicker: "작업 공간",
        conversationState: "대화 준비 전",
      });
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
      restoreDraft();
      return;
    }

    try {
      const conversations = await fetchJson(dom, appConversationsUrl(app.appId));
      await refreshGoalSummary();
      const fallbackConversationId =
        preferredConversationId ||
        (conversations.length ? conversations[0].conversation_id : "");

      renderConversationList(conversations, fallbackConversationId);

      if (fallbackConversationId) {
        state.savedConversationId = fallbackConversationId;
        await fetchConversation(fallbackConversationId);
        return;
      }

      state.currentConversationId = "";
      state.savedConversationId = "";
      state.currentJobId = "";
      clearThreadTransition();
      clearPendingOutgoing();
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
      updateHeroState(dom, {
        threadTitle: "새 대화를 시작하세요",
        threadKicker: "선택된 대화",
        conversationState: "이 앱에는 아직 대화가 없습니다.",
      });
      renderWorkspaceSummary(dom, `${app.title}에는 아직 대화가 없습니다. 메시지를 보내면 현재 앱 레인에서 새 세션이 시작됩니다.`);
      renderConversationList([], "");
      restoreDraft();
    } catch (error) {
      clearPendingOutgoing();
      state.currentConversationId = "";
      state.currentJobId = "";
      clearThreadTransition();
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
      updateHeroState(dom, {
        threadTitle: "대화를 불러오지 못했습니다",
        threadKicker: "선택된 대화",
        conversationState: `대화를 불러오지 못했습니다: ${error.message}`,
      });
      dom.conversationList.innerHTML = '<p class="conversation-list-empty">대화를 불러오지 못했습니다.</p>';
      renderRecentThreadRail([], "");
      clearAutonomySummary(dom, "대화를 불러오지 못해 autonomy summary도 갱신하지 못했습니다.");
      restoreDraft();
    }
  }

  async function fetchConversation(conversationId, options = {}) {
    const { syncJob = true } = options;
    if (!conversationId) {
      clearThreadTransition();
      clearPendingOutgoing();
      closeAppendStream();
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
      return;
    }

    if (state.currentConversationId && state.currentConversationId !== conversationId) {
      if (dom.threadScroller) {
        dom.threadScroller.dataset.pendingConversationId = conversationId;
      }
      state.savedConversationId = conversationId;
      startThreadTransition(conversationId);
      clearPendingOutgoing();
      closeAppendStream();
      state.currentConversationId = "";
      state.currentJobId = "";
      state.conversationCache = null;
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
    }

    let conversation;
    let bootstrap = null;
    try {
      bootstrap = await connectAppendStream(conversationId, { awaitBootstrap: true });
      if (
        bootstrap &&
        String(bootstrap.attach_mode || "") === "sse-bootstrap" &&
        bootstrap.conversation &&
        String(bootstrap.conversation.conversation_id || "") === conversationId
      ) {
        conversation = bootstrap.conversation;
      } else {
        conversation = await fetchJson(dom, conversationUrl(conversationId));
        connectAppendStream(conversationId);
      }
    } catch (error) {
      clearThreadTransition();
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
      restoreDraft();
      syncDraftStatus();
      throw error;
    }
    clearThreadTransition();
    if (shouldClearPendingOutgoing(conversation)) {
      clearPendingOutgoing(conversation.conversation_id);
    }
    state.currentConversationId = conversation.conversation_id;
    state.savedConversationId = state.currentConversationId;
    for (const card of dom.conversationList.querySelectorAll("[data-conversation-id]")) {
      card.classList.toggle("active", card.dataset.conversationId === state.currentConversationId);
    }
    renderConversation(dom, state, conversation, persistSettings);
    syncConversationCardState();
    syncAppendCursor(conversation);
    state.appendStream.attachMode =
      bootstrap && String(bootstrap.attach_mode || "") === "sse-bootstrap"
        ? "sse-bootstrap"
        : state.appendStream.attachMode || "snapshot-fallback";
    state.appendStream.bootstrapVersion =
      bootstrap && bootstrap.version !== undefined
        ? String(bootstrap.version)
        : state.appendStream.bootstrapVersion || "";
    restoreDraft();
    syncDraftStatus();

    if (!syncJob) {
      return;
    }

    if (conversation.latest_job_id) {
      state.currentJobId = conversation.latest_job_id;
      const payload = await syncLatestJob();
      if (payload && payload.status !== "completed" && payload.status !== "failed") {
        ensurePollingForJob();
        return;
      }
    }

    state.currentJobId = "";
    state.latestProposalJobId = "";
    updateProposalButton(dom, state.latestProposalJobId);
  }

  async function ensureConversation() {
    if (state.currentConversationId) {
      return state.currentConversationId;
    }

    const app = selectedAppData(dom);
    if (!app) {
      throw new Error("대상 앱을 먼저 선택하세요.");
    }

    const payload = await fetchJson(dom, `${normalizeBaseUrl()}/api/conversations`, {
      method: "POST",
      body: JSON.stringify({
        app_id: app.appId,
        source: "mobile-ops-console",
      }),
    });
    await loadConversations();
    state.currentConversationId = payload.conversation_id;
    state.savedConversationId = state.currentConversationId;
    await fetchConversation(state.currentConversationId);
    return state.currentConversationId;
  }

  async function createConversation() {
    try {
      await ensureConversation();
      setStatus(dom, "새 대화 세션을 만들었습니다.");
      setJobMeta(dom, `CONVERSATION · ${state.currentConversationId}`);
    } catch (error) {
      setStatus(dom, `새 대화 생성에 실패했습니다.\n\n${error.message}`);
    }
  }

  async function loadApps() {
    setStatus(dom, "앱 목록을 불러오는 중...");

    try {
      const apps = await fetchJson(dom, deps.appsUrl());
      const previousAppId = dom.appSelect.value || state.savedAppId || "";
      dom.appSelect.innerHTML = "";

      for (const app of apps) {
        const option = document.createElement("option");
        option.value = app.app_id;
        option.textContent = `${app.title} (${app.app_id})`;
        option.dataset.deploymentUrl = app.deployment_url || "";
        option.dataset.sessionId = app.session_id || "";
        option.dataset.title = app.title || app.app_id;
        dom.appSelect.append(option);
      }

      if (!apps.length) {
        updateSelectedAppCard(dom, null);
        clearAutonomySummary(dom, "등록된 앱이 없어서 autonomy summary를 표시할 수 없습니다.");
        setStatus(dom, "등록된 앱이 없습니다. 서버의 state/registry/apps를 확인하세요.");
        setJobMeta(dom, "앱이 등록되면 여기에서 작업 상태를 추적합니다.");
        dom.conversationList.innerHTML = '<p class="conversation-list-empty">등록된 앱이 없습니다.</p>';
        renderRecentThreadRail([], "");
        renderConversation(dom, state, null, persistSettings);
        syncConversationCardState();
        clearLearningSummary(dom);
        return;
      }

      if (previousAppId) {
        dom.appSelect.value = previousAppId;
      }
      if (!dom.appSelect.value) {
        dom.appSelect.selectedIndex = 0;
      }

      syncSelectedAppSession({ detectRotation: true });
      updateSelectedAppCard(dom, selectedAppData(dom));
      persistSettings();
      setStatus(dom, `앱 ${apps.length}개를 불러왔습니다.`);
      setJobMeta(dom, "앱과 대화를 선택하고 에이전트와 계속 대화할 수 있습니다.");
      await loadConversations();
    } catch (error) {
      setStatus(dom, `앱 목록을 불러오지 못했습니다.\n\n${error.message}`);
    }
  }

  async function handleAppChange() {
    syncSelectedAppSession({ detectRotation: false });
    updateSelectedAppCard(dom, selectedAppData(dom));
    state.savedConversationId = "";
    stopPolling();
    await loadConversations();
    persistSettings();
    restoreDraft();
  }

  async function handleConversationChange() {
    if (state.savedConversationId) {
      await fetchConversation(state.savedConversationId);
    } else {
      restoreDraft();
    }
    persistSettings();
  }

  return {
    createConversation,
    clearPendingOutgoing,
    ensureConversation,
    fetchConversation,
    handleAppChange,
    handleConversationChange,
    loadApps,
    loadConversations,
    refreshGoalSummary,
    showPendingAssistant,
    showPendingOutgoing,
  };
}
