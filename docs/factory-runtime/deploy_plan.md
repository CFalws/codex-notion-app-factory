# Factory Runtime Deploy Plan

## Iteration 92

This deploy plan validates the canonical selected-thread session-status contract and does not introduce new transport, new polling gates, or new status surfaces beyond that boundary cleanup.

## Deployment Impact

This iteration changes frontend state derivation only. The bounded expectation is that the selected-thread center header, composer strip, inline live block, and left-rail active-session row all reflect one canonical selected-thread session-status model, while existing polling and fallback behavior remains unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Confirm the center header, composer strip, inline live block, and left active-session row all show the same selected-thread ownership or downgrade state during healthy SSE ownership.
5. Force reconnect or polling fallback and confirm those same surfaces relabel consistently to `RECONNECT` or `POLLING` instead of leaving stale healthy ownership behind.
6. Submit a new request and confirm handoff state appears consistently through the canonical selected-thread status boundary without changing the fixed composer behavior.
7. Switch threads and confirm the existing switch continuity still clears stale ownership immediately while the canonical session-status model exposes the attach or clear reason consistently.
8. Confirm no new `/api/jobs` or `/api/goals` suppression was introduced in this iteration beyond the existing intended-path behavior.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread ownership contract succeeds through the intended path.
