# Factory Runtime Deploy Plan

## Iteration 86

This deploy plan validates the bounded selected-thread center-header ownership contract and does not introduce any new transport or layout behavior beyond that contract.

## Deployment Impact

This iteration changes only the selected-thread center-header session contract in the existing conversation-first workspace. The bounded expectation is that the summary row stays visible for selected-thread and switching contexts, the ownership chip shows `SSE OWNER` only on healthy selected-thread SSE authority, degraded paths relabel it to `RECONNECT` or `POLLING`, and switch or terminal idle clears the ownership chip immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two existing conversations.
4. Select a conversation on the healthy selected-thread path and confirm the center header summary row is visible with one adjacent `SSE OWNER` indicator.
5. Confirm the healthy header row reflects the selected target and canonical selected-thread state without reopening any prose-heavy side status surface.
6. Trigger reconnect or polling fallback and confirm the same ownership chip relabels to `RECONNECT` or `POLLING` instead of pretending the session is still healthy.
7. Click a different conversation and confirm the summary row stays visible for the switching target while the ownership chip clears immediately.
8. Confirm terminal idle and true no-selection idle do not leave stale healthy ownership in the center header.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible header state succeeds through the intended selected-thread SSE ownership path with no healthy `/api/goals` fallback after submit.
