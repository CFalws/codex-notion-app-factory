# Factory Runtime Deploy Plan

## Iteration 232

This deploy plan validates streamed autonomy identity through selected-thread `session_status` in the deployed workspace gate.

## Deployment Impact

This iteration extends the existing selected-thread SSE contract so autonomy identity travels inside append/bootstrap `session_status`. The gate should pass only when healthy goal identity, iteration, phase, proposal, review, verify, ready, and applied progression remain attributable to streamed `session_status`, the transcript-tail session block stays canonical, and goals polling stays explicit degraded fallback instead of becoming a healthy visible owner.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation that is receiving append SSE updates.
5. Confirm append/bootstrap `session_status` provides goal title, goal status, iteration, heading, freshness, and fallback metadata to the selected-thread workspace.
6. Confirm the transcript-tail session block remains the only healthy live-owned surface while header, rail, and composer-adjacent mirrors stay passive.
7. Confirm healthy autonomy identity and phase/proposal progression remain attributable to streamed `session_status` with no healthy `/api/apps/{appId}/goals` takeover.
8. Confirm goals polling appears only on explicit degraded or non-authoritative states.
9. Confirm reconnect downgrade, polling fallback, switch, deselection, restore, and terminal transitions clear streamed authority immediately with no stale autonomy identity revival.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains SSE-scoped, single-owner, and free of healthy polling-owned autonomy identity.
