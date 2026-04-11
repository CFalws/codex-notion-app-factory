# Factory Runtime Deploy Plan

## Iteration 210

This deploy plan validates the healthy-path sticky active-session row in the left rail and its non-authoritative mirroring of the selected live session.

## Deployment Impact

This iteration keeps transport and ownership unchanged while tightening left-rail mirroring. The healthy selected-thread path should show exactly one sticky active-session row for the selected live thread while the center timeline and composer strip remain the authoritative live session surfaces.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm the left rail shows exactly one sticky active-session row for the selected thread when the selected-thread path is healthy live, handoff, switching, new, or paused.
6. Confirm the sticky row mirrors owner, phase, and follow or unseen cues from the same selected-thread datasets as the center workspace, but remains non-authoritative and chip-first.
7. Confirm no selected-card live-owner row or non-selected row becomes live-owned while the sticky row is present.
8. Confirm reconnect downgrade, polling fallback, deselection, terminal idle, and terminal resolution clear the sticky row immediately.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path passes only when exactly one sticky rail row appears for the selected thread and no stale or duplicate rail ownership survives authority loss.
