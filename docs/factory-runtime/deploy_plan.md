# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, transcript follow behavior, footer dock, and center-pane header intact, but tightens the left conversation rail so cards expose one bounded recent preview line and clearer compact state labels without widening transport scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and inspect the conversation rail before opening a thread.
4. Confirm each card keeps one concise recent preview line and that the selected thread shows the clearest live-state label without implying liveness for other threads.
5. Confirm the selected-thread label follows the existing selected-thread live state, while transcript and footer composer remain continuously accessible and the footer rail remains the richer in-pane live surface.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
