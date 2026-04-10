# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the center conversation workspace now exposes one compact recent-thread quick-switch rail beneath the header, so the operator can move between the selected thread and nearby recent threads without reopening the left navigation drawer.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path and at least two additional recent threads available.
4. Confirm the center pane shows exactly one bounded recent-thread chip rail beneath the conversation header and that it remains reachable without opening the nav drawer.
5. Confirm the selected thread and recent threads can be switched directly from that rail while transcript history and the composer stay mounted.
6. Confirm the rail mirrors selected, live, follow, and switching cues from the existing selected-thread state selectors, and that non-selected threads never retain live-owned treatment.
7. Confirm stale live ownership clears immediately on thread switch, reconnect downgrade, polling fallback, and terminal completion.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the recent-thread rail proof passes without unexpected degraded-path signals or stale live ownership.
