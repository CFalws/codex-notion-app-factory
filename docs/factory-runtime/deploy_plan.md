# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside selected-thread switch verification and durable iteration artifacts. The bounded expectation is that intentional thread switches preserve the mounted conversation shell and composer while clearing old-thread live ownership immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Start from a healthy selected-thread SSE-owned run, then intentionally switch to a different thread.
5. Confirm the center shell stays mounted with exactly one compact transition placeholder and no generic empty-state flash.
6. Confirm the prior-thread healthy inline session block is gone, follow ownership is cleared, and the composer strip remains in switching attach state for the target thread.
7. Confirm reconnect, polling fallback, ownership loss, and terminal idle do not leave stale selected-thread live ownership cues during or after switch.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch path passes the tightened no-stale-inline-block and no-stale-follow-ownership assertions on the intended path.
