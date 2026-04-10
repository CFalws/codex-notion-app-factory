# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, dock behavior, transcript-tail live surface, and selected-row live-owner cues intact, but moves primary selected-thread context into a compact center-header summary and leaves deeper operator detail behind a collapsed-by-default secondary panel.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the center header exposes a compact selected-thread summary row with explicit scope, path, and state cues while the transcript, live strip, and composer remain the dominant workspace surfaces.
5. Confirm the secondary panel starts collapsed on desktop and phone widths and is no longer required to understand the current selected-thread state.
6. Submit a new message in the selected thread and confirm the selected row still flips to `HANDOFF`, then to `LIVE`, and surfaces `NEW` or `PAUSED` only for the selected thread as the session state changes.
7. Confirm non-selected rows continue to show only snapshot labels and bounded preview lines even while the selected thread is active.
8. Confirm degraded fallback or reconnect downgrade clears compact center summary cues back toward snapshot context without leaving stale live markers in the rail or center pane.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals, stale live leakage, or side-panel-dependent interpretation.
