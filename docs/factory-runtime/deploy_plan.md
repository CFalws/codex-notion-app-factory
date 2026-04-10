# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the bottom follow control now becomes the single explicit detached-tail indicator for healthy selected-thread SSE sessions, showing `PAUSED` immediately and upgrading to `NEW` when unseen append backlog appears.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an active selected conversation.
4. Start a healthy selected-thread SSE session, scroll away from the live tail before new backlog appears, and confirm the bottom control shows `PAUSED` immediately.
5. Let unseen selected-thread live appends arrive and confirm the same control upgrades in place to `NEW` with the correct unseen count metadata.
6. Confirm jump-to-latest, reconnect downgrade, polling fallback, terminal idle, thread switch, and ownership loss clear the control immediately.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm detached-tail visibility now follows the intended selected-thread SSE path without stale paused or new state on degraded paths.
