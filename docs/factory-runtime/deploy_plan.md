# Factory Runtime Deploy Plan

## Iteration 102

This deploy plan validates the selected-thread switch continuity contract and does not introduce new transport, new polling behavior, or additional center-pane live surfaces.

## Deployment Impact

This iteration changes intentional thread-switch presentation only. The bounded expectation is that the center pane keeps one switching placeholder, the fixed composer keeps one explicit switching target state, stale old-thread ownership clears immediately, and no generic empty-state or polling-owned success presentation appears during a healthy switch.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Start from one healthy selected-thread conversation and switch intentionally to another existing conversation.
6. Confirm the center pane keeps exactly one switching placeholder and never flashes the generic timeline empty-state during the attach.
7. Confirm the composer strip shows `SWITCHING` for the target conversation until the new thread resolves to restore, handoff, ready, or live ownership.
8. Confirm the previous thread's live or polling-owned markers clear immediately and the recent-thread rail does not present its own switching mirror.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread switch continuity contract succeeds through the intended path.
