# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, transcript follow behavior, footer dock, center-pane header, and left rail intact, but makes stream health explicit in the footer live rail so degraded reconnecting or offline states are visible without widening transport scope.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths and inspect the footer live rail while a selected thread moves between live, reconnecting, and offline stream states.
4. Confirm the rail exposes explicit healthy and degraded transport cues such as `LIVE`, `RECONNECT`, and `OFFLINE` plus compact recovery wording in the same composer-adjacent surface.
5. Confirm the cues still follow the existing selected-thread stream state, while transcript and footer composer remain continuously accessible and no new status surface appears.
6. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
