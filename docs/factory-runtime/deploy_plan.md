# Factory Runtime Deploy Plan

## Iteration 231

This deploy plan validates the unified selected-thread transcript-tail session block in the deployed workspace gate.

## Deployment Impact

This iteration keeps runtime behavior unchanged and records the intended unified selected-thread session surface. The gate should pass only when healthy live handoff and autonomy progression remain concentrated in one transcript-tail session block, header and rail mirrors stay compact and passive, the composer remains chat-first, and polling stays explicit degraded fallback instead of becoming a healthy visible owner.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation that is receiving append SSE updates.
5. Confirm the transcript-tail session block becomes the only live-owned surface for handoff and active session progression.
6. Confirm the bottom-fixed composer remains mounted, chat-first, and free of duplicate live-detail ownership.
7. Confirm header and rail cues remain compact passive mirrors rather than separate live-detail panels.
8. Confirm healthy phase and proposal progression remain attributable to selected-thread SSE data with no healthy polling takeover.
9. Confirm reconnect downgrade, polling fallback, switch, deselection, restore, and terminal transitions clear canonical live ownership immediately.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains SSE-scoped, single-owner, and free of duplicate or stale live session surfaces.
