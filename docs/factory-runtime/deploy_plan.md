# Factory Runtime Deploy Plan

## Iteration 85

This deploy plan validates the bounded selected-thread switch continuity contract and does not introduce any new transport or layout behavior beyond that contract.

## Deployment Impact

This iteration changes only selected-thread switch continuity evidence in the existing conversation-first workspace. The bounded expectation is that intentional switches keep the center shell and composer mounted, show exactly one transition placeholder, clear stale old-thread ownership immediately, and mirror the same switching target in the active-session rail row.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two existing conversations.
4. Select a conversation on the healthy selected-thread path and confirm the active-session row is visible with selected-thread ownership.
5. Click a different conversation and confirm the center shell stays mounted with exactly one transition placeholder and no generic empty-state flash.
6. Confirm the composer remains docked, the active-session row retargets immediately to the pending conversation as non-owned `SWITCHING`, and stale old-thread live ownership is gone.
7. Before that switch resolves, click another conversation and confirm the placeholder and rail row retarget to the latest selection without duplicate switch surfaces.
8. Confirm degraded reconnect, polling fallback, terminal idle, and true no-selection idle still clear or relabel through the canonical selected-thread state.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch path succeeds through the intended selected-thread continuity contract.
