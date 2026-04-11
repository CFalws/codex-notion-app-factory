# Factory Runtime Deploy Plan

## Iteration 103

This deploy plan validates the selected-thread unified timeline progression contract and does not introduce new transport, new polling behavior, or new non-timeline healthy status surfaces.

## Deployment Impact

This iteration changes healthy selected-thread autonomy progression presentation only. The bounded expectation is that proposal, review, verify, ready, and applied state appears in one transcript live surface on the healthy SSE-owned path, while degraded, reconnect, restore, and polling provenance remains explicit and non-healthy.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Start from one healthy selected-thread conversation and drive proposal, review, verify, ready, and applied progress through the intended SSE path.
6. Confirm the transcript live activity item shows milestone progression for those states without requiring the sidecar autonomy card or `/api/goals` owned success.
7. Confirm the sidecar autonomy surface stays hidden only while the selected-thread session is healthy-owned, and degraded, reconnect, restore, or polling states return explicit non-healthy provenance.
8. Confirm the fixed composer remains bound to the same conversation and the compact header stays contextual rather than becoming a second healthy autonomy surface.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread unified timeline progression contract succeeds through the intended path.
