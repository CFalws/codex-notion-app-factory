# Factory Runtime Deploy Plan

## Iteration 116

This deploy plan validates the selected-thread active-session rail mirroring contract and does not introduce new transport, polling behavior, or a backend switch protocol.

## Deployment Impact

This iteration changes left-rail selected-thread session mirroring only. The bounded expectation is that the sticky active-session row mirrors switching or attach, handoff, and healthy live follow states for the selected thread only, while degraded, polling, reconnect, terminal, and non-selected paths clear that mirror immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation and one additional conversation for switching.
4. Start from a healthy selected-thread conversation and confirm the sticky active-session row shows one selected-thread mirror above the list with `SSE OWNER` plus `LIVE`, `PAUSED`, or `NEW`.
5. Scroll off tail if needed and confirm the row mirrors unseen-count state only for the selected thread.
6. Intentionally switch to another thread and confirm the active-session row stays visible as a non-owned `SWITCHING` and `ATTACH` mirror for the target conversation instead of clearing to idle.
7. Confirm reconnect downgrade, polling fallback, terminal completion, and deselection clear the active-session row immediately.
8. Confirm non-selected conversation rows remain snapshot-only and the center workspace and composer contracts from earlier iterations remain unchanged.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread active-session rail contract succeeds through the intended path.
