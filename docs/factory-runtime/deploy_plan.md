# Factory Runtime Deploy Plan

## Iteration 173

This deploy plan validates healthy selected-thread autonomy authority from the canonical `session_status` stream.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while moving healthy selected-thread autonomy visibility onto the canonical `session_status` SSE seam instead of goals polling fallback.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation with internal append SSE enabled and confirm proposal, review, verify, blocker, intended-path, and verifier acceptability state update from the live session seam without waiting for goals polling.
5. Confirm the active workspace stays SSE-owned on that healthy path and that autonomy treatment does not silently fall back to goals polling.
6. Confirm reconnect downgrade, polling fallback, deselection, restore gap, terminal completion, and true non-authoritative paths clear or degrade that autonomy treatment immediately.
7. Confirm stale autonomy ownership never survives onto a non-selected, deselected, or polling-owned path.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible autonomy surfaces are driven by selected-thread `session_status` on the healthy path and explicitly non-authoritative elsewhere.
