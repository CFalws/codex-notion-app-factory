export function createConversationController(deps) {
  const {
    dom,
    state,
    selectedAppData,
    fetchJson,
    appConversationsUrl,
    conversationUrl,
    setStatus,
    setJobMeta,
    renderConversation,
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
  } = deps;

  async function loadConversations() {
    const app = selectedAppData(dom);
    const preferredConversationId =
      state.currentConversationId ||
      dom.conversationSelect.value ||
      dom.conversationSelect.dataset.savedConversationId ||
      "";

    dom.conversationSelect.innerHTML = "";
    state.conversationCache = null;

    if (!app) {
      state.currentConversationId = "";
      updateHeroState(dom, {
        appName: "앱 미선택",
        conversationState: "대화 준비 전",
        jobState: "IDLE",
      });
      renderConversation(dom, state, null, persistSettings);
      restoreDraft();
      return;
    }

    try {
      const conversations = await fetchJson(dom, appConversationsUrl(app.appId));
      for (const conversation of conversations) {
        const option = document.createElement("option");
        option.value = conversation.conversation_id;
        option.textContent = `${conversation.title} (${new Date(conversation.updated_at).toLocaleString()})`;
        dom.conversationSelect.append(option);
      }

      if (preferredConversationId) {
        dom.conversationSelect.value = preferredConversationId;
      }
      if (!dom.conversationSelect.value && conversations.length) {
        dom.conversationSelect.selectedIndex = 0;
      }

      if (dom.conversationSelect.value) {
        dom.conversationSelect.dataset.savedConversationId = dom.conversationSelect.value;
        await fetchConversation(dom.conversationSelect.value);
        return;
      }

      state.currentConversationId = "";
      state.currentJobId = "";
      renderConversation(dom, state, null, persistSettings);
      dom.conversationMeta.textContent = "이 앱에는 아직 대화가 없습니다.";
      updateHeroState(dom, {
        appName: app.title,
        conversationState: "새 대화 필요",
      });
      renderWorkspaceSummary(dom, `${app.title}에는 아직 대화가 없습니다. 메시지를 보내면 현재 앱 레인에서 새 세션이 시작됩니다.`);
      restoreDraft();
    } catch (error) {
      state.currentConversationId = "";
      state.currentJobId = "";
      renderConversation(dom, state, null, persistSettings);
      dom.conversationMeta.textContent = `대화를 불러오지 못했습니다: ${error.message}`;
      restoreDraft();
    }
  }

  async function fetchConversation(conversationId, options = {}) {
    const { syncJob = true } = options;
    if (!conversationId) {
      renderConversation(dom, state, null, persistSettings);
      return;
    }

    const conversation = await fetchJson(dom, conversationUrl(conversationId));
    state.currentConversationId = conversation.conversation_id;
    dom.conversationSelect.value = state.currentConversationId;
    dom.conversationSelect.dataset.savedConversationId = state.currentConversationId;
    renderConversation(dom, state, conversation, persistSettings);
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
    dom.conversationSelect.value = state.currentConversationId;
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
      const previousAppId = dom.appSelect.value || dom.appSelect.dataset.savedAppId || "";
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
        setStatus(dom, "등록된 앱이 없습니다. 서버의 state/registry/apps를 확인하세요.");
        setJobMeta(dom, "앱이 등록되면 여기에서 작업 상태를 추적합니다.");
        renderConversation(dom, state, null, persistSettings);
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
    dom.conversationSelect.dataset.savedConversationId = "";
    stopPolling();
    await loadConversations();
    persistSettings();
    restoreDraft();
  }

  async function handleConversationChange() {
    if (dom.conversationSelect.value) {
      await fetchConversation(dom.conversationSelect.value);
    } else {
      restoreDraft();
    }
    persistSettings();
  }

  return {
    createConversation,
    ensureConversation,
    fetchConversation,
    handleAppChange,
    handleConversationChange,
    loadApps,
    loadConversations,
  };
}
