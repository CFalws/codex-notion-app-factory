# Factory Runtime Deploy Plan

## Iteration 95

This deploy plan validates the single selected-thread center-lane session-surface contract and does not introduce new transport, new polling gates, or new status surfaces beyond that bounded frontend presentation change.

## Deployment Impact

This iteration changes selected-thread surface presentation only. The bounded expectation is that healthy selected-thread SSE handoff or active progress appears through exactly one live-owned center-lane session block, while the header and composer remain compact supporting context, degraded reconnect or polling paths stay visibly downgraded, and existing polling behavior remains unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Submit a new request and confirm the selected-thread center workspace shows exactly one live-owned session block during handoff or healthy SSE progress, rather than duplicating live-owned status in the header or composer strip.
5. Confirm the center session block still exposes explicit `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, `APPLIED`, or failure progression directly from selected-thread SSE append events.
6. Confirm the header remains visible as compact selected-thread context and the composer strip remains compact target context, while degraded reconnect or polling fallback still renders explicit downgraded markers.
7. Switch threads and confirm the old thread live ownership clears immediately while the mounted shell and fixed composer continuity still hold.
8. Confirm no new `/api/jobs` or `/api/goals` suppression was introduced in this iteration beyond the existing intended-path behavior.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread unified session-surface contract succeeds through the intended path.
