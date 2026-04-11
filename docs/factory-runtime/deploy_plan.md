# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes the selected-thread active-run job ownership boundary in the existing conversation-first workspace. The bounded expectation is that healthy selected-thread attach, resume, and send flows stay on the existing SSE-owned session path without routine `/api/jobs/{id}` polling, while degraded conditions explicitly reopen the fallback path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Open an existing selected thread with healthy append-stream SSE ownership and confirm attach performs no `/api/jobs/{id}` fetch after the selected-thread attach mark.
5. Submit a message from the fixed composer and confirm the session remains in the existing SSE-owned handoff and active-run path without routine `/api/jobs/{id}` polling.
6. Confirm proposal, review, verify, ready, and applied visibility still update immediately through the selected-thread session strip and timeline.
7. Confirm reconnect downgrade, ownership loss, stale-or-missing freshness, or off-thread tracking visibly downgrades the selected-thread path before polling is re-enabled.
8. Confirm forced degraded paths can still reopen polling after the downgrade is visible and explicit.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread active run works through the intended SSE-owned session contract.
