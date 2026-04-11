# Factory Runtime Deploy Plan

## Iteration 94

This deploy plan validates the canonical selected-thread live-autonomy and phase-progression contract and does not introduce new transport, new polling gates, or new status surfaces beyond that bounded frontend projection.

## Deployment Impact

This iteration changes frontend state derivation and selected-thread surface rendering only. The bounded expectation is that healthy selected-thread SSE append events immediately drive explicit proposal, review, verify, auto-apply, ready, applied, and failure progression in the center-lane session surfaces, while reconnect and polling fallback stay visibly degraded and existing polling behavior remains unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Submit a new request and confirm the selected-thread transcript live card, inline live block, and composer-adjacent strip show `HANDOFF`, then explicit `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, `APPLIED`, or failure progression directly from selected-thread SSE append events.
5. Confirm the same healthy selected-thread surfaces mark autonomy state as SSE-sourced, fresh, and non-fallback instead of preserving stale fallback metadata.
6. Force reconnect or polling fallback and confirm the selected-thread live autonomy surfaces remain visible but explicitly downgraded to `RECONNECT` or `POLLING` instead of looking healthy or silently clearing.
7. Switch threads and confirm the old thread phase projection and live-owned autonomy clear immediately while the mounted shell and fixed composer continuity still hold.
8. Confirm no new `/api/jobs` or `/api/goals` suppression was introduced in this iteration beyond the existing intended-path behavior.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread phase progression and live-autonomy contract succeeds through the intended path.
