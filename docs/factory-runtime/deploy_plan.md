# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the selected-thread header now exposes exactly one compact live-session ownership chip, showing healthy `SSE OWNER` only on the intended path and downgrading immediately to `RECONNECT` or `POLLING` when retry, fallback, or session rotation breaks that path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the selected-thread header shows exactly one compact `SSE OWNER` live-session chip while the selected conversation is healthy and SSE-owned.
5. Confirm that same chip downgrades immediately to `RECONNECT` on append-stream retry and to `POLLING` on retry fallback or detected session rotation.
6. Confirm the chip clears on thread switch and terminal completion without leaving stale live-owned state in the header.
7. Confirm transcript history, selected-thread live strip, composer access, and the secondary panel remain continuous while the header indicator changes state.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread header ownership proof passes without unexpected `codex.exec.retrying`, `runtime.exception`, or session rotation on the healthy path.
