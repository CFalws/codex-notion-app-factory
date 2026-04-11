# Factory Runtime Deploy Plan

## Iteration 89

This deploy plan validates the bounded finite-state selected-thread active-session rail contract and does not introduce any new transport or layout behavior beyond that contract.

## Deployment Impact

This iteration changes only the sticky left-rail active-session row in the existing conversation-first workspace. The bounded expectation is that the row appears only for canonical selected-thread handoff and healthy live state, uses only `HANDOFF`, `LIVE`, `NEW`, or `PAUSED`, and clears immediately on reconnect downgrade, polling fallback, terminal idle, or thread switch.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread handoff and one healthy selected-thread live session available.
4. Submit on the healthy selected-thread path and confirm the left rail shows exactly one sticky active-session row labeled `HANDOFF` until the first assistant append or ownership handoff completes.
5. Confirm the same row shows `LIVE` while the selected thread is healthy and followed, `NEW` when selected-thread backlog exists, and `PAUSED` when follow is detached without backlog.
6. Trigger reconnect downgrade or polling fallback and confirm the row clears immediately instead of preserving stale live ownership.
7. Click a different conversation and confirm the row clears immediately on thread switch instead of showing a switch target row.
8. Confirm terminal idle also clears the row and that non-selected conversation cards remain snapshot-only.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the rail-state transitions succeed through canonical selected-thread state with no healthy `/api/goals` fallback after submit.
