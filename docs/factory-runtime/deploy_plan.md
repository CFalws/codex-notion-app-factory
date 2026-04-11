# Factory Runtime Deploy Plan

## Iteration 120

This deploy plan validates the selected-thread active-session rail contract and does not introduce new transport, polling behavior, or a backend switch protocol.

## Deployment Impact

This iteration changes left-rail presentation only. The bounded expectation is that the sticky active-session row appears only for the healthy selected-thread SSE session, mirrors owner plus current phase plus detached follow state from the same canonical datasets as the center and footer, and clears immediately on degraded or non-selected paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the sticky active-session row appears above the thread list with `SSE OWNER`, the current phase, and either `LIVE` or detached `NEW` or `PAUSED` state from the selected-thread datasets.
5. Scroll away from the live tail and confirm the row updates to detached follow state with unseen-count metadata while non-selected rows remain snapshot-only.
6. Re-engage follow and confirm the row returns to the healthy live phase view; switch threads or trigger reconnect or polling fallback and confirm the row clears immediately.
7. Confirm the row never persists on switching, terminal idle, deselection, or degraded paths.
8. Confirm the center live lane and unified footer session bar contracts from earlier iterations remain unchanged.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread active-session rail contract succeeds through the intended path.
