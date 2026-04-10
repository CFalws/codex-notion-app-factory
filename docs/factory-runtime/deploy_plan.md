# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, dock behavior, and transcript-tail live surface intact, but strengthens the selected rail row as the sole live-owner row through compact owner-state cues.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Submit a new message in the selected thread and confirm the selected row flips to `HANDOFF`, then to `LIVE`, and surfaces `NEW` or `PAUSED` only for the selected thread as the session state changes.
5. Confirm non-selected rows continue to show only snapshot labels and bounded preview lines even while the selected thread is active.
6. Confirm selected-row live-owner cues clear immediately on terminal resolution, polling-only fallback, reconnect downgrade, or thread switch.
7. Confirm transcript plus composer reachability do not regress on phone or desktop widths and that the selected-row live mirror does not become a second detailed live-status surface.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals or non-selected live leakage.
