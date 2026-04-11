# Factory Runtime Deploy Plan

## Iteration 207

This deploy plan validates healthy selected-thread suppression of duplicate secondary execution and autonomy cards.

## Deployment Impact

This iteration keeps transport and ownership unchanged while tightening presentation convergence. On the healthy selected-thread path, the center timeline and session strip should remain authoritative and the secondary execution and autonomy cards should stay hidden until authority is lost.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm the healthy selected-thread path exposes phase, verifier, blocker, and apply readiness through the center timeline and session strip without requiring the secondary execution or autonomy cards.
6. Confirm the secondary execution and autonomy cards are hidden and marked `suppressed` only while healthy selected-thread authority is active.
7. Confirm reconnect downgrade, polling fallback, switch, deselection, restore-gap loss, and terminal completion immediately restore or downgrade those secondary-detail cards through the existing fail-open path.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path passes only when the secondary execution and autonomy cards stay suppressed on the healthy path and reappear or downgrade immediately on authority loss.
