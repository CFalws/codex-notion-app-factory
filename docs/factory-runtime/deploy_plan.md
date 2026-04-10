# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the selected-thread submit handoff, polling boundary, and verification layers. The bounded expectation is that healthy session startup now remains on the existing local handoff plus append-SSE path without an eager snapshot poll, while degraded paths still activate polling explicitly when SSE authority is unavailable or lost.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Submit a request in the selected thread and confirm the workspace stays continuous through local send, accepted handoff, and `SSE OWNER` without an eager snapshot refresh on the healthy path.
5. Confirm the transcript-tail live item, header chip, rail mirror, and composer strip all reflect the same selected-thread ownership while SSE is connecting or live.
6. Trigger unavailable EventSource, reconnect, or polling fallback and confirm polling activates only after the downgrade while healthy live ownership clears immediately.
7. Switch intentionally to another thread and confirm old selected-thread ownership does not survive the switch and the startup path does not rotate sessions unexpectedly.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible workspace proves startup followed the intended selected-thread SSE path rather than a hidden eager poll.
