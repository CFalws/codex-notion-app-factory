# Factory Runtime Deploy Plan

## Iteration 106

This deploy plan validates the healthy selected-thread transcript-collapse contract and does not introduce new transport, new polling behavior, or new transcript event schema.

## Deployment Impact

This iteration changes healthy selected-thread transcript presentation only. The bounded expectation is that healthy selected-thread SSE authority events no longer append duplicate session-status cards while the current run is already represented by the live session surfaces, and degraded, reconnect, restore, switching, and polling provenance remain explicit.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Start from one healthy selected-thread conversation and confirm the composer-adjacent footer strip remains the live session dock with current phase and milestone chips.
6. Let proposal, review, verify, ready, and applied progression occur on the healthy SSE-owned path and confirm the transcript does not append duplicate healthy selected-thread session-event cards for those transitions.
7. Confirm degraded, reconnect, restore, switching, or failure paths still surface explicit transcript evidence instead of silently collapsing.
8. Confirm detached follow state still works through the same footer dock and clears in place when returning to the live tail.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread transcript-collapse contract succeeds through the intended path.
