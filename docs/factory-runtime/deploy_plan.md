# Factory Runtime Deploy Plan

## Iteration 105

This deploy plan validates the selected-thread footer session-dock contract and does not introduce new transport, new polling behavior, or new duplicate healthy live-status surfaces.

## Deployment Impact

This iteration changes healthy selected-thread footer presentation only. The bounded expectation is that current phase and milestone progression appear in the composer-adjacent footer strip on the healthy SSE-owned path, while degraded, reconnect, restore, switching, and polling provenance immediately clear or downgrade that footer ownership.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Start from one healthy selected-thread conversation and confirm the composer-adjacent footer strip becomes the visible live session dock with current phase and milestone chips.
6. Scroll away from the live tail and let unseen append backlog accumulate, then confirm the same footer dock also carries `NEW` or `PAUSED` follow context and unseen-count metadata.
7. Confirm the footer action jumps back to the live tail and clears detached follow ownership in place.
8. Confirm reconnect, polling fallback, restore, terminal idle, or thread switch immediately clear or downgrade the footer session dock instead of leaving stale selected-thread ownership.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread footer session-dock contract succeeds through the intended path.
