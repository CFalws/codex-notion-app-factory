# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-conversation SSE path. The bounded expectation is that the rail reads as conversation-first, with thread history first, a compact always-visible selected-app summary, and heavier operator controls collapsed by default, without changing live-strip ownership or secondary-panel scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the conversation list is the first visible rail section on desktop and phone widths, with app or operator controls no longer ranked above it.
5. Confirm the compact selected-app summary remains visible near the rail header so the current app is still identifiable without opening the heavier controls section.
6. Open the collapsed app or operator section and confirm refresh, app selection, and deploy link remain reachable on touch and keyboard.
7. Confirm the app or operator section starts collapsed by default and re-collapses when the nav sheet opens on phone widths.
8. Confirm session strip, bottom follow control, and selected-row live-owner cues remain unchanged.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals or a rail that reverts to operator-first ordering.
