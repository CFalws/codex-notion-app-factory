# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the selected conversation now exposes exactly one compact composer-adjacent live strip on the healthy selected-thread SSE path, and that the strip clears immediately instead of persisting through degraded or terminal states.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the active conversation shows exactly one compact live strip directly above the composer while the selected thread is healthy and SSE-owned.
5. Confirm the strip stays chip-first and selected-thread scoped, with no duplicate live surface in the active pane.
6. Confirm the strip clears immediately on reconnect downgrade, polling fallback, thread switch, and terminal completion without leaving stale live-owned state near the composer.
7. Confirm transcript history, composer access, and the secondary panel remain continuously reachable on phone-sized layouts while the strip appears and clears.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the healthy-path live strip proof passes without unexpected degraded-path signals.
