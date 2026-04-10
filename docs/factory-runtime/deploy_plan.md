# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the conversation-first surface now exposes explicit FOLLOWING versus FOLLOW PAUSED state for the healthy selected-thread live tail, so the operator can tell at a glance whether they are still attached while reading history.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path and enough history to scroll away from the live tail.
4. Confirm the selected-thread header summary and composer-adjacent session strip show FOLLOWING while healthy SSE ownership is attached.
5. Scroll away from the live tail and confirm the workspace flips to FOLLOW PAUSED without opening another panel and that the jump-to-latest affordance remains reachable on phone widths.
6. Restore follow and confirm the paused signal clears immediately, then confirm reconnect downgrade, polling fallback, thread switch, and terminal completion also clear paused or following chips without leaving stale live-owned state behind.
7. Confirm the recent-thread rail, transcript history, composer access, and secondary panel remain continuously reachable on phone-sized layouts while follow pauses and resumes.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the explicit live-follow proof passes without unexpected degraded-path signals or stale paused chips.
