# Factory Runtime Deploy Plan

## Iteration 122

This deploy plan validates the selected-thread switch continuity contract and does not introduce new transport, polling behavior, or a backend switch protocol.

## Deployment Impact

This iteration changes switch-path presentation only. The bounded expectation is that intentional thread switches keep the center shell and fixed composer mounted, show exactly one compact transition placeholder, clear prior-thread ownership in the same render cycle, and avoid the true empty-state path until the new selected thread attaches.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and intentionally switch threads. Confirm the center shell stays mounted, the fixed composer remains visible, and exactly one `SWITCHING` placeholder appears until the target thread attaches.
5. Confirm the transition placeholder and mounted shell publish ownership-cleared datasets while the old-thread header, rail, and footer ownership surfaces clear in the same render cycle.
6. Trigger rapid thread switching, reconnect downgrade, and polling fallback around the selected thread and confirm the workspace still avoids the true empty-state path during intentional switches.
7. Confirm genuine no-selection idle still renders the generic empty placeholder only when there is no selected thread at all.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread switch continuity contract succeeds through the intended path.
