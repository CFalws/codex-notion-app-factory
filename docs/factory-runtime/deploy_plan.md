# Factory Runtime Deploy Plan

## Iteration 169

This deploy plan validates the compact selected-thread session summary row above the transcript in the center pane.

## Deployment Impact

This iteration keeps transport and transcript-tail live ownership unchanged while reducing the healthy selected-thread header to one compact session summary row and suppressing duplicate live-owner chrome above the transcript.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the center header shows exactly one compact summary row while the transcript-tail live activity remains the only primary live session item.
5. Confirm the header phase chip is hidden on that healthy path and does not reintroduce a second live-owner surface above the transcript.
6. Switch to a different conversation and confirm the compact summary row clears immediately while the switch placeholder and transcript continuity behave as before.
7. Confirm reconnect downgrade, polling fallback, deselection, terminal completion, and lost authority clear the summary row and leave only degraded or cleared header treatment.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible compact row is selected-thread-only, healthy-path-only, and never competes with the transcript-tail live activity for primary session authority.
