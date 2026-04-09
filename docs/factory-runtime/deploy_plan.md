# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, transcript follow behavior, footer dock, center-pane header, and left rail intact, but shortens the footer live-rail detail text into compact action cues without widening transport scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and inspect the footer live rail while a selected thread moves through send and live execution.
4. Confirm the rail renders compact cues such as sending, handoff, proposal, review, verify, ready, applied, failed, and idle without falling back to sentence-level strip explanations.
5. Confirm the cues still follow the existing selected-thread live state, while transcript and footer composer remain continuously accessible and no new status surface appears.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
