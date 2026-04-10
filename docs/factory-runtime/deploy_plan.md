# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-conversation SSE path. The bounded expectation is that the currently selected row alone mirrors selected-thread live ownership with compact `HANDOFF`, `LIVE`, `NEW`, or `PAUSED` cues, while non-selected rows remain snapshot-only and no new center-pane status surface is introduced.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the selected conversation row alone shows compact `HANDOFF`, `LIVE`, `NEW`, or `PAUSED` owner cues plus the existing follow or unread detail.
5. Confirm non-selected rows stay snapshot-only and never inherit selected-thread live-owner treatment.
6. Confirm thread switch, reconnect downgrade, polling fallback, and terminal resolution clear the selected-row live-owner marker immediately.
7. Confirm the center-pane session strip, bottom follow control, and footer composer remain otherwise unchanged.
8. Confirm the rail still reads as conversation-first on desktop and phone widths.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals or duplicate live ownership elsewhere in the rail.
