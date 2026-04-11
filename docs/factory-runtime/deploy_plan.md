# Factory Runtime Deploy Plan

## Iteration 110

This deploy plan validates the selected-thread transcript session-event lane contract and does not introduce new transport, new polling behavior, or a new transcript state model.

## Deployment Impact

This iteration changes healthy selected-thread transcript presentation only. The bounded expectation is that the center timeline shows one compact healthy session event lane with explicit milestone datasets, while reconnect, polling fallback, restore-only, switch, terminal, and true empty paths clear or downgrade that lane immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Start from one healthy selected-thread conversation and drive proposal, review, verify, ready, and applied progression through the intended SSE path.
6. Confirm the center timeline shows exactly one compact live session event lane with explicit phase and milestone datasets for the selected thread.
7. Confirm healthy transcript session-event cards for those same authority events do not append beside that lane.
8. Confirm reconnect, polling fallback, restore-only, terminal idle, switch, and true empty paths clear or downgrade the lane immediately instead of resembling healthy ownership.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread transcript session-event lane contract succeeds through the intended path.
