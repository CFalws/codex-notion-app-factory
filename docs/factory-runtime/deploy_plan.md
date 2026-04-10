# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-thread composer-adjacent live rail. The bounded expectation is that the selected conversation exposes one compact chip-first session rail that distinguishes healthy `LIVE` SSE transport from `RECONNECT`, `OPEN`, or `OFFLINE` degradation without promoting polling fallback as live ownership.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the selected-thread session rail shows `LIVE` when the selected conversation is healthy on the intended SSE path.
5. Force reconnect or temporary disconnect conditions and confirm the same rail degrades to `RECONNECT`, `OPEN`, or `OFFLINE` instead of continuing to present healthy live ownership.
6. Confirm polling-only fallback clears the selected-thread rail rather than leaving stale live-owned transport visible.
7. Switch threads on desktop and phone widths and confirm the old thread loses rail ownership immediately.
8. Confirm no second selected-thread status surface or stale old-thread transport cue appears while the current rail state changes.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread transport-health proof still passes without degraded-path signals or polling-only live presentation.
