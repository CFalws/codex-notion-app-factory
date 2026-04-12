# Factory Runtime Deploy Plan

## Iteration 225

This deploy plan validates selected-thread session-stream ownership across the append SSE path and conversation-first workspace.

## Deployment Impact

This iteration keeps the existing append SSE transport and selected-thread ownership model, but records the intended path as one session-scoped live stream. Healthy phase, proposal, verifier, and apply state should arrive through the selected-thread append SSE path, while polling remains explicit fallback-only behavior.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation with an active autonomy run and confirm the append SSE path is attached.
5. Confirm phase, proposal, verifier, and apply-related changes appear through the selected-thread session timeline and inline milestone strip without polling-owned takeover.
6. Confirm the header, composer-adjacent context, transcript timeline, and rail markers all reflect the same selected-thread session provenance.
7. Confirm `ops-jobs` remains fallback-only and does not reclaim ownership while the selected thread is SSE-owned.
8. Confirm reconnect downgrade, offline fallback, switch, deselection, and restore paths explicitly downgrade or clear ownership with no stale healthy revival.
9. Confirm the composer-adjacent strip stays passive on the healthy selected-thread path.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when healthy selected-thread live status is attributable to the append SSE session stream and fallback remains degraded-only.
