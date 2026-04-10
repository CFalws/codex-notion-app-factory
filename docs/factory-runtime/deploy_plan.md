# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the selected-thread switch-continuity verification and documentation layers. The bounded expectation is that intentional thread switches keep the conversation-first shell mounted, clear old ownership immediately, and route the gap through the dedicated transition placeholder instead of a generic empty-state flash.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Start from a healthy selected-thread SSE-owned session, then intentionally switch to another thread from the left rail.
5. Confirm the center pane keeps one transition placeholder, does not flash `.timeline-empty`, and clears old selected-thread live ownership immediately in the header and transcript.
6. Confirm the composer stays bottom-fixed with `SWITCHING` owner state, target copy for the new thread, and `ATTACH` transport while the new snapshot attaches.
7. Confirm degraded reconnect or polling fallback still remain explicit and do not appear as healthy ownership continuity during or after the switch.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible workspace proves intentional thread switches follow the dedicated transition path instead of a generic empty-state reset.
