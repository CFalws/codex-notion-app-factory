# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on finite left-rail session chips. The bounded expectation is that the selected conversation exposes only compact owner and follow chips in the rail, while non-selected rows remain snapshot-only.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the selected row alone renders compact owner and follow chips from the finite `HANDOFF`, `LIVE`, `NEW`, and `PAUSED` vocabulary.
5. Confirm the selected row no longer shows helper-style live detail text in the rail.
6. Confirm non-selected rows remain snapshot-only with one compact label and one bounded preview line.
7. Confirm thread switch, terminal resolution, reconnect downgrade, and polling-only fallback each clear the selected-row live chips immediately.
8. Confirm desktop and phone widths keep the rail readable without changing the conversation-first shell.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the finite selected-row chip proof still passes without degraded-path signals.
