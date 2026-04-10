# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, center-pane inline session block, and non-selected thread rendering intact, but mirrors the selected-thread handoff and live session state into the selected conversation card through compact chips and detail labels.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Submit a new message in the selected thread and confirm the selected conversation card immediately reflects pending handoff without making any non-selected row look live.
5. After request acceptance and during the active SSE-owned phase progression, confirm the selected card shows compact live detail and follow or unread chips that mirror the center-pane session state.
6. Confirm the selected-card live markers clear on terminal resolution or thread switch without leaving stale live state in the rail.
7. Confirm transcript plus composer reachability and the existing jump-to-latest behavior do not regress on phone or desktop widths.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals.
