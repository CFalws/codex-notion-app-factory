# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside selected-thread header rendering and verification layers. The bounded expectation is that the title remains, but the separate phase chip and compact session summary row no longer compete with the transcript during active or switching selected-thread states.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Start a healthy selected-thread SSE-owned run and confirm the center header shows only the title and meta while the separate phase chip and session summary row stay hidden.
5. Confirm attach, handoff, reconnect, and polling fallback states do not reintroduce stale visible header-owned session chrome above the transcript.
6. Confirm the inline session block, left-rail row, and composer-adjacent strip still provide the visible session state while the transcript remains the first dominant center surface.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible center workspace shows no duplicate header live-status chrome on the intended path.
