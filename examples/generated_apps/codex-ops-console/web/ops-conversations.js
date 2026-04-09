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

  function clearPendingOutgoing(conversationId = "") {
    if (conversationId && state.pendingOutgoing?.conversationId !== conversationId) {
      return;
    }
    state.pendingOutgoing = {
      conversationId: "",
      body: "",
      createdAt: "",
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
      status: "sending",
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

  function resetAppendStream(conversationId = "") {
    state.appendStream ||= {};
    state.appendStream.conversationId = conversationId;
    state.appendStream.status = "offline";
    state.appendStream.transport = "polling";
    state.appendStream.lastRenderSource = "snapshot";
    state.appendStream.lastLiveAppendId = 0;
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

    clearPendingOutgoing(activeConversationId);
    state.appendStream.lastAppendId = appendId;
    state.appendStream.lastLiveAppendId = appendId;
    state.appendStream.transport = "sse";
    state.appendStream.status = "live";
    state.appendStream.lastRenderSource = "sse";
    renderConversation(dom, state, conversation, persistSettings);
    syncConversationCardState();
    restoreDraft();
    syncDraftStatus();
    return true;
  }

  function connectAppendStream(conversationId) {
    closeAppendStream();
    if (!conversationId || typeof window === "undefined" || typeof window.EventSource !== "function") {
      return;
    }

    let openedOnce = false;
    state.appendStream.source = new window.EventSource(internalConversationAppendStreamUrl(conversationId));
    state.appendStream.conversationId = conversationId;
    state.appendStream.status = "connecting";
    state.appendStream.transport = "sse";
    state.appendStream.lastRenderSource = "snapshot";
    renderSessionStrip(dom, state, state.conversationCache);
    syncConversationCardState();

    state.appendStream.source.addEventListener("open", () => {
      if (state.currentConversationId !== conversationId || state.appendStream?.conversationId !== conversationId) {
        return;
      }
      openedOnce = true;
      state.appendStream.status = "live";
      renderSessionStrip(dom, state, state.conversationCache);
      syncConversationCardState();
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
      if (state.currentConversationId !== conversationId || state.appendStream?.conversationId !== conversationId) {
        return;
      }
      if (!openedOnce) {
        closeAppendStream();
        return;
      }
      state.appendStream.status = "reconnecting";
      renderSessionStrip(dom, state, state.conversationCache);
      syncConversationCardState();
    });
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

  function syncConversationCardState() {
    const selectedConversationId = state.currentConversationId || state.savedConversationId || "";
    const liveConversationId = String(dom.threadScroller?.dataset.liveConversationId || "");
    const presentation = String(dom.threadScroller?.dataset.sessionPresentation || "cleared");
    const liveRunState = String(dom.threadScroller?.dataset.liveRunState || "done");

    let liveLabel = "";
    if (selectedConversationId && selectedConversationId === liveConversationId) {
      if (presentation === "connecting") {
        liveLabel = "CONNECTING";
      } else if (presentation === "live") {
        liveLabel = liveRunState.replaceAll("-", " ").toUpperCase();
      } else if (presentation === "reconnecting") {
        liveLabel = "RECONNECTING";
      } else if (presentation === "terminal") {
        liveLabel = "DONE";
      }
    }

    for (const card of dom.conversationList.querySelectorAll("[data-conversation-id]")) {
      const isSelected = card.dataset.conversationId === selectedConversationId;
      const marker = card.querySelector("[data-conversation-marker]");
      const liveState = card.querySelector("[data-conversation-live-state]");
      card.classList.toggle("active", isSelected);
      card.dataset.selected = isSelected ? "true" : "false";
      card.dataset.threadState = isSelected ? (liveLabel ? liveLabel.toLowerCase() : "idle") : "idle";
      if (marker) {
        marker.hidden = !isSelected;
        marker.textContent = "ACTIVE";
      }
      if (liveState) {
        liveState.hidden = !isSelected || !liveLabel;
        liveState.textContent = liveLabel;
      }
    }
  }

  async function refreshGoalSummary() {
    const app = selectedAppData(dom);
    if (!app) {
      clearAutonomySummary(dom, "앱을 선택하면 최근 autonomous iteration blocker가 여기에 표시됩니다.");
      return;
    }
    try {
      const goals = await fetchJson(dom, appGoalsUrl(app.appId));
      const goal = pickRelevantGoal(goals);
      if (!goal) {
        clearAutonomySummary(dom, "이 앱에는 아직 autonomous goal 기록이 없습니다.");
        return;
      }
      renderAutonomySummary(dom, goal);
    } catch (error) {
      clearAutonomySummary(dom, `Autonomy summary를 불러오지 못했습니다: ${error.message}`);
    }
  }

  function renderConversationList(conversations, selectedConversationId = "") {
    if (!conversations.length) {
      dom.conversationList.innerHTML = '<p class="conversation-list-empty">아직 대화가 없습니다.</p>';
      return;
    }

    dom.conversationList.innerHTML = conversations
      .map((conversation) => {
        const isActive = conversation.conversation_id === selectedConversationId;
        return `
          <button
            type="button"
            class="conversation-card${isActive ? " active" : ""}"
            data-conversation-id="${conversation.conversation_id}"
            data-selected="${isActive ? "true" : "false"}"
            data-thread-state="idle"
          >
            <span class="conversation-card-head">
              <span class="conversation-card-title">${conversation.title}</span>
              <span class="conversation-card-marker" data-conversation-marker ${isActive ? "" : "hidden"}>ACTIVE</span>
            </span>
            <span class="conversation-card-meta-row">
              <span class="conversation-card-meta">${new Date(conversation.updated_at).toLocaleString()}</span>
              <span class="conversation-card-live" data-conversation-live-state hidden></span>
            </span>
          </button>
        `;
      })
      .join("");
    syncConversationCardState();
  }

  async function loadConversations() {
    const app = selectedAppData(dom);
    const preferredConversationId = state.currentConversationId || state.savedConversationId || "";
    state.conversationCache = null;
    closeAppendStream();

    if (!app) {
      clearPendingOutgoing();
      state.currentConversationId = "";
      state.savedConversationId = "";
      dom.conversationList.innerHTML = '<p class="conversation-list-empty">앱을 먼저 고르세요.</p>';
      clearAutonomySummary(dom, "앱을 선택하면 최근 autonomous iteration blocker가 여기에 표시됩니다.");
      updateHeroState(dom, {
        appName: "앱 미선택",
        conversationState: "대화 준비 전",
        jobState: "IDLE",
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
      clearPendingOutgoing();
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
      dom.conversationMeta.textContent = "이 앱에는 아직 대화가 없습니다.";
      updateHeroState(dom, {
        appName: app.title,
        conversationState: "새 대화 필요",
      });
      renderWorkspaceSummary(dom, `${app.title}에는 아직 대화가 없습니다. 메시지를 보내면 현재 앱 레인에서 새 세션이 시작됩니다.`);
      renderConversationList([], "");
      restoreDraft();
    } catch (error) {
      clearPendingOutgoing();
      state.currentConversationId = "";
      state.currentJobId = "";
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
      dom.conversationMeta.textContent = `대화를 불러오지 못했습니다: ${error.message}`;
      dom.conversationList.innerHTML = '<p class="conversation-list-empty">대화를 불러오지 못했습니다.</p>';
      clearAutonomySummary(dom, "대화를 불러오지 못해 autonomy summary도 갱신하지 못했습니다.");
      restoreDraft();
    }
  }

  async function fetchConversation(conversationId, options = {}) {
    const { syncJob = true } = options;
    if (!conversationId) {
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
      clearPendingOutgoing();
      closeAppendStream();
      state.currentConversationId = "";
      state.currentJobId = "";
      state.conversationCache = null;
      renderConversation(dom, state, null, persistSettings);
      syncConversationCardState();
    }

    const conversation = await fetchJson(dom, conversationUrl(conversationId));
    clearPendingOutgoing(conversation.conversation_id);
    state.currentConversationId = conversation.conversation_id;
    state.savedConversationId = state.currentConversationId;
    for (const card of dom.conversationList.querySelectorAll("[data-conversation-id]")) {
      card.classList.toggle("active", card.dataset.conversationId === state.currentConversationId);
    }
    renderConversation(dom, state, conversation, persistSettings);
    syncConversationCardState();
    syncAppendCursor(conversation);
    connectAppendStream(conversation.conversation_id);
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
        option.dataset.title = app.title || app.app_id;
        dom.appSelect.append(option);
      }

      if (!apps.length) {
        updateSelectedAppCard(dom, null);
        clearAutonomySummary(dom, "등록된 앱이 없어서 autonomy summary를 표시할 수 없습니다.");
        setStatus(dom, "등록된 앱이 없습니다. 서버의 state/registry/apps를 확인하세요.");
        setJobMeta(dom, "앱이 등록되면 여기에서 작업 상태를 추적합니다.");
        dom.conversationList.innerHTML = '<p class="conversation-list-empty">등록된 앱이 없습니다.</p>';
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
    showPendingOutgoing,
  };
}
