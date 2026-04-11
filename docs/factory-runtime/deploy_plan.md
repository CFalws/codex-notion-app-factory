# Factory Runtime Deploy Plan

## Iteration 212

This deploy plan validates the selected-thread inline session block in the center transcript and its ownership boundary against adjacent live surfaces.

## Deployment Impact

This iteration keeps transport and ownership unchanged while tightening the center transcript ownership seam. The healthy selected-thread path should show one compact inline session block for live SSE-owned progress or pending handoff, while degraded, switch, restore, and terminal paths continue to clear or fail open immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through live proposal, review, verify, auto-apply, ready, and applied states.
6. Confirm the center transcript shows exactly one compact inline session block for the selected thread and that the older healthy live-activity row is absent while the block is present.
7. Confirm the inline block carries phase, transport, verifier or blocker, and milestone cues directly in the transcript.
8. Confirm pending assistant handoff uses the same inline block path instead of a duplicate live-owner surface.
9. Confirm reconnect downgrade, polling fallback, switch, deselection, and terminal completion clear the inline block immediately.
10. Confirm degraded fallback, switch placeholders, and restore paths still avoid stale inline live ownership.
11. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the transcript owns the selected healthy session through one inline block and no duplicate healthy live-activity row remains.
