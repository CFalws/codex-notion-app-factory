# Factory Runtime Deploy Plan

## Iteration 143

This deploy plan validates the center-timeline authority contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread render composition and verification only. The bounded expectation is that the center timeline live-session item becomes the sole authority-looking selected-thread session surface in the center lane, while summary and status prose are demoted behind machine-readable datasets.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the timeline live-session item stays authoritative while the header summary row, autonomy detail, and execution status cards stay hidden or demoted in the same render pass.
5. Trigger reconnect downgrade, polling fallback, restore, and handoff and confirm the same timeline item remains the authority surface while the demoted datasets switch from `healthy` to the correct downgraded presentation.
6. Trigger switching, deselection, and terminal resolution and confirm the healthy authority datasets clear immediately and no duplicate selected-thread center-lane prose survives.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible center-timeline authority contract succeeds through the intended path.
