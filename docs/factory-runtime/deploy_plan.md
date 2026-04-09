# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, footer dock, center-pane header, and non-selected snapshot cues intact, but strengthens the selected conversation row so it reads as the live session owner in the left rail.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths while a selected conversation is healthy, reconnecting, proposal-ready, or terminal.
4. Confirm the selected row reads as the unmistakable live session owner from the rail itself, with the selected marker and session chip carrying the ownership treatment.
5. Confirm non-selected rows remain snapshot-only and transcript plus composer accessibility do not regress on phone or desktop widths.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
