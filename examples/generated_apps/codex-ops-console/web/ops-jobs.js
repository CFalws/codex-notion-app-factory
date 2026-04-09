export function createJobController(deps) {
  const {
    dom,
    state,
    fetchJson,
    jobUrl,
    setStatus,
    setJobMeta,
    updateProposalButton,
    renderLearningSummary,
    renderJobActivity,
    fetchConversation,
    refreshGoalSummary,
    describeJob,
    isAppendStreamConnected,
  } = deps;

  async function syncLatestJob() {
    if (!state.currentJobId) {
      return null;
    }

    const payload = await fetchJson(dom, jobUrl(state.currentJobId));
    setStatus(dom, describeJob(payload));
    setJobMeta(dom, `${payload.status.toUpperCase()} · ${payload.job_id}`);
    state.latestProposalJobId = payload.proposal ? payload.proposal.job_id : "";
    updateProposalButton(dom, state.latestProposalJobId);

    if (payload.decision_summary) {
      renderLearningSummary(
        dom,
        payload.decision_summary,
        payload.title || "이번 작업에서 배운 점",
        payload.status || "RECORDED",
      );
    }

    renderJobActivity(dom, state.conversationCache, state.currentJobId, payload);

    return payload;
  }

  function ensurePollingForJob() {
    if (!state.currentJobId || state.pollingTimer) {
      return;
    }
    state.pollingTimer = setInterval(() => {
      pollCurrentState();
    }, 3000);
  }

  function stopPolling() {
    if (!state.pollingTimer) {
      return;
    }
    clearInterval(state.pollingTimer);
    state.pollingTimer = null;
  }

  async function pollCurrentState() {
    try {
      const payload = await syncLatestJob();

      if (state.currentConversationId && !isAppendStreamConnected(state, state.currentConversationId)) {
        try {
          await fetchConversation(state.currentConversationId, { syncJob: false });
        } catch (_) {
          // Keep the last rendered conversation and let the job panel carry the visible error if needed.
        }
      }
      await refreshGoalSummary();

      if (!payload) {
        return;
      }

      if (payload.status === "completed" || payload.status === "failed") {
        if (payload.status === "completed" && dom.autoOpenInput.checked) {
          dom.openAppButton.focus();
        }
        state.currentJobId = "";
        stopPolling();
        if (state.currentConversationId && !isAppendStreamConnected(state, state.currentConversationId)) {
          await fetchConversation(state.currentConversationId, { syncJob: false });
        }
        await refreshGoalSummary();
      }
    } catch (error) {
      setStatus(dom, `작업 상태를 가져오지 못했습니다.\n\n${error.message}`);
      setJobMeta(dom, "작업 상태 조회 실패");
    }
  }

  return {
    ensurePollingForJob,
    pollCurrentState,
    stopPolling,
    syncLatestJob,
  };
}
