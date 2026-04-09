# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, transcript follow behavior, footer dock, compact composer state row, and left-rail session markers intact, but makes the active center header conversation-first by promoting selected-thread identity and a compact live phase badge while demoting app identity out of the primary reading path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and select a live thread.
4. Confirm the first readable center-pane surface is the selected conversation title plus compact phase badge, not the selected app shell.
5. Confirm the header badge follows the existing selected-thread live state, while transcript and footer composer remain continuously accessible and the footer rail remains the only richer in-pane live surface.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
