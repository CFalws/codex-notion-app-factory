# Factory Runtime Deploy Plan

## Iteration 113

This deploy plan validates the selected-thread switch continuity contract and does not introduce new transport, polling behavior, or a backend switch protocol.

## Deployment Impact

This iteration changes selected-thread switch presentation only. The bounded expectation is that intentional switches stay on one compact workspace placeholder with explicit summary and scroller datasets until the new snapshot or SSE session attaches, while true no-selection idle keeps the generic empty workspace path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation and one additional conversation for switching.
4. Start from a healthy selected-thread conversation and intentionally switch to another thread.
5. Confirm the center workspace never flashes the generic empty timeline during that transition.
6. Confirm exactly one compact switching placeholder appears, the thread scroller reports switching placeholder datasets, and the workspace summary copy describes selected-thread attach pending.
7. Confirm the bottom-fixed composer stays mounted throughout the transition and resolves in place when the target snapshot or SSE session attaches.
8. Confirm restore, reconnect, polling fallback, terminal, and true no-selection idle still use their own explicit downgrade or empty paths and do not inherit switching treatment.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread switch continuity contract succeeds through the intended path.
