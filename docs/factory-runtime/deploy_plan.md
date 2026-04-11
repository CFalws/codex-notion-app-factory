# Factory Runtime Deploy Plan

## Iteration 104

This deploy plan validates the selected-thread unified footer-follow contract and does not introduce new transport, new polling behavior, or new duplicate healthy follow surfaces.

## Deployment Impact

This iteration changes healthy selected-thread follow presentation only. The bounded expectation is that detached `NEW` or `PAUSED` follow state appears in the composer-adjacent footer strip on the healthy SSE-owned path, while degraded, reconnect, restore, switching, and polling provenance immediately clear or downgrade that footer ownership.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm restore still appears through one transcript-tail `ATTACH` or `RESUME` item before bootstrap settles.
5. Start from one healthy selected-thread conversation, scroll away from the live tail, and let unseen append backlog accumulate.
6. Confirm the composer-adjacent footer strip becomes the only visible detached follow surface with compact `LIVE` or `READY` plus `NEW` or `PAUSED` context and unseen-count metadata.
7. Confirm the footer action jumps back to the live tail and clears detached follow ownership in place.
8. Confirm reconnect, polling fallback, terminal idle, or thread switch immediately clear or downgrade the footer follow surface instead of leaving stale selected-thread ownership.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread unified footer-follow contract succeeds through the intended path.
