# Factory Runtime Deploy Plan

## Iteration 230

This deploy plan validates selected-thread session-status authority in the deployed workspace gate.

## Deployment Impact

This iteration keeps runtime behavior unchanged and records the intended selected-thread session-status authority path. The gate should pass only when healthy live phase and proposal progression are attributable to append SSE session status, the transcript-centered surface remains the only live-owned authority, and polling stays explicit degraded fallback instead of becoming a healthy visible owner.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation that is receiving append SSE updates.
5. Confirm phase and proposal progression appear through the selected-thread session timeline and inline block without polling-owned takeover.
6. Confirm the center conversation surface remains the only live-owned authority while header and composer-adjacent mirrors stay passive.
7. Confirm healthy `/api/jobs/{id}` and `/api/apps/{appId}/goals` fetches do not become visible owners in the selected-thread workspace.
8. Confirm reconnect downgrade or polling fallback remains explicit degraded presentation and clears live ownership immediately.
9. Confirm switch, deselection, restore, and terminal transitions do not revive stale live-owned phase or proposal state.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread session-status authority remains SSE-scoped, single-owner, and free of healthy polling takeover.
