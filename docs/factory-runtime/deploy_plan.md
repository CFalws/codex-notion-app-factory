# Factory Runtime Deploy Plan

## Iteration 227

This deploy plan validates one authoritative selected-thread SSE session source in the deployed workspace gate.

## Deployment Impact

This iteration keeps runtime behavior unchanged and tightens only deployed verification. The gate should pass only when the healthy selected-thread append SSE path remains the sole live authority, the composer-adjacent strip stays passive with matching `sse` provenance, polling remains fallback-only, and session rotation or stale-state revival fails verification.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation with an active autonomy run and confirm the append SSE path is attached.
5. Confirm the center timeline is the only healthy live-owned session surface.
6. Confirm the composer-adjacent strip stays visible but passive, with matching phase and `sse` provenance and no owned transport or footer-dock authority.
7. Confirm job polling and goals refresh do not become visible owners on the healthy path.
8. Confirm reconnect downgrade or offline fallback clears healthy ownership and does not revive stale live-owned phase or proposal state.
9. Confirm unexpected session rotation fails the gate.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread SSE session remains the sole healthy authority and fallback remains explicit and degraded-only.
