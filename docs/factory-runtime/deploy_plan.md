# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside selected-thread center-pane rendering and verification layers. The bounded expectation is that one inline selected-thread session block now carries handoff, healthy live, and degraded progress without a duplicate transcript-tail live activity item.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and the center inline session block visible.
4. Start a healthy selected-thread SSE-owned run and confirm the inline session block shows active live phase progress while no transcript-tail live activity item remains.
5. Confirm accepted handoff and degraded reconnect or polling states reuse that same inline session block instead of splitting across a second center live surface.
6. Confirm reconnect, polling fallback, ownership loss, terminal idle, or thread switch clear the healthy inline block immediately instead of leaving stale owned cues.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible workspace shows exactly one selected-thread center session block for handoff, healthy live, or degraded progress with no duplicate transcript-tail live activity.
