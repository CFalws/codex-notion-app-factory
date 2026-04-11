# Factory Runtime Deploy Plan

## Iteration 81

This deploy plan validates the bounded composer-adjacent strip phase contract and does not introduce any new transport or layout behavior beyond that contract.

## Deployment Impact

This iteration changes only the composer-adjacent selected-thread session strip in the existing conversation-first workspace. The bounded expectation is that the strip shows one authoritative phase chip on the healthy selected-thread SSE path, relabels immediately to degraded transport states when ownership drops, and clears stale healthy phase on switch or idle.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two existing conversations.
4. Select a conversation on the healthy SSE-owned path and confirm the session strip shows exactly one phase chip that tracks `LIVE`, `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, or `APPLIED`.
5. Confirm the strip detail remains compact and no longer relies on multi-chip owner or transport state to communicate the healthy selected-thread phase.
6. Force a reconnect or polling fallback path and confirm the same strip state row relabels immediately to `RECONNECT` or `POLLING`.
7. Click a different conversation and confirm the strip clears stale healthy phase immediately by moving to transition state for the pending target.
8. Confirm true idle clears the strip and that no healthy `/api/goals` fetch appears after submit.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible strip path succeeds through the intended selected-thread SSE-owned phase contract.
