# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on a sticky active-session mirror in the left rail. The bounded expectation is that the navigation column exposes one compact selected-thread session row for live, reconnecting, handoff, switching, and unseen-live states without introducing new transport or control behavior.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the left navigation shows exactly one compact active-session row above the conversation list while the selected thread is live, reconnecting, in handoff, or switching.
5. Confirm the row mirrors the same selected-thread conversation id, state chips, and follow or unseen pressure as the center workspace.
6. Confirm the row clears immediately on terminal resolution, reconnect downgrade, polling fallback, or thread switch so stale ownership never survives.
7. Confirm non-selected conversation rows remain snapshot-only while the sticky active-session row is visible.
8. Confirm desktop and phone widths keep the row visible without opening the secondary panel and without displacing the conversation-first shell.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the sticky active-session row proof still passes without degraded-path signals.
