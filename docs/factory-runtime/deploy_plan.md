# Factory Runtime Deploy Plan

## Iteration 118

This deploy plan validates the selected-thread transcript-bottom follow-control contract and does not introduce new transport, polling behavior, or a backend switch protocol.

## Deployment Impact

This iteration changes transcript-bottom follow ownership only. The bounded expectation is that the healthy selected-thread SSE path exposes one compact bottom follow control with explicit `NEW` or `PAUSED` plus unseen-count metadata, while degraded and non-selected paths clear that control immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run, scroll away from the live tail, and confirm the transcript-bottom control becomes visible with `NEW` or `PAUSED`, selected-thread ownership, and unseen-count metadata.
5. Click the bottom follow control and confirm it clears immediately while scrolling back to the live tail.
6. Confirm reconnect downgrade, polling fallback, switching, terminal idle, and deselection clear the control immediately and do not leave stale selected-thread ownership behind.
7. Confirm no composer-adjacent or secondary follow surface reappears.
8. Confirm the rail, center live session lane, and composer strip contracts from earlier iterations remain unchanged.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread detached follow contract succeeds through the intended path.
