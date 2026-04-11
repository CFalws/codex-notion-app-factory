# Factory Runtime Deploy Plan

## Iteration 90

This deploy plan validates the bounded selected-thread switch continuity contract and does not introduce any new transport or layout behavior beyond that contract.

## Deployment Impact

This iteration changes only the selected-thread switch continuity evidence in the existing conversation-first workspace. The bounded expectation is that intentional thread switches keep the center shell and composer mounted, show exactly one compact attach placeholder, clear stale live ownership immediately, and avoid `/api/jobs` and `/api/goals` fallback on the intended path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two existing conversations.
4. Select a healthy selected-thread conversation, then click a different conversation and confirm the center shell stays mounted with exactly one compact transition placeholder.
5. Confirm the composer remains fixed and reachable throughout the switch and that previous-thread healthy or degraded live markers clear immediately.
6. Confirm no generic timeline empty-state flash appears during that switch and that the new snapshot attaches through the transition placeholder path.
7. Before the first switch resolves, click another conversation and confirm the placeholder retargets cleanly to the latest selection without duplicate switch surfaces.
8. Confirm `/api/jobs` and `/api/goals` do not reappear during the intended switch path.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch path succeeds through the intended selected-thread continuity contract.
