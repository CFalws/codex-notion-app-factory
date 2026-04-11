# Factory Runtime Deploy Plan

## Iteration 109

This deploy plan validates the selected-thread switch continuity contract and does not introduce new transport, new polling behavior, or a new switch state model.

## Deployment Impact

This iteration changes the intentional selected-thread switch presentation only. The bounded expectation is that the center pane keeps one compact `SWITCHING` placeholder and the composer shell mirrors the same target state until the new snapshot attaches, while reconnect, polling fallback, restore, terminal, and true no-selection paths do not retain switching treatment.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Start from one healthy selected-thread conversation and intentionally switch to another conversation from the left rail.
6. Confirm the center pane never flashes the generic empty-state view and instead shows exactly one compact `SWITCHING` placeholder until the new snapshot attaches.
7. Confirm the composer shell reports the same switching target state from the existing selected-thread ownership contract while the old thread no longer appears live-owned.
8. Confirm reconnect, polling fallback, restore, terminal, and true no-selection paths do not retain the switching placeholder or switching datasets.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread switch continuity contract succeeds through the intended path.
