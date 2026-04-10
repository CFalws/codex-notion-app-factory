# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside selected-thread footer rendering and verification layers. The bounded expectation is that one composer-adjacent activity bar now carries ownership, transport, phase, and proposal progress without a duplicate footer live-status row underneath it.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and the composer dock visible.
4. Start a healthy selected-thread SSE-owned run and confirm the composer-adjacent `session-strip` shows owner, transport, phase, and proposal chips while the separate owner row stays hidden.
5. Confirm attach, handoff, reconnect, and polling fallback states reuse that same `session-strip` instead of surfacing a second live footer row.
6. Confirm the fixed composer remains visually dominant on desktop and phone widths while degraded, ownership-loss, terminal idle, and switched-away states clear live-owned treatment immediately.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible footer shows exactly one composer-adjacent selected-thread activity bar with no duplicate owner row while the intended path remains healthy.
