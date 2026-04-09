# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, transcript follow behavior, footer dock, center-pane header, and stream-health rail intact, but adds a compact selected-thread session marker to the left rail without widening transport scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and inspect the conversation rail while a selected thread moves through live or in-flight states.
4. Confirm the selected row exposes one compact session marker that follows the existing selected-thread phase or stream state, while non-selected rows remain snapshot-only.
5. Confirm the rail makes the active or generating thread recognizable without reducing transcript and footer composer accessibility or introducing broader rail prose.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
