# Factory Runtime Deploy Plan

## Iteration 214

This deploy plan validates the sticky left-rail active-session row as a strict mirror of the selected-thread transcript and composer session authority.

## Deployment Impact

This iteration keeps transport and ownership unchanged while tightening rail mirroring. The healthy selected-thread path should show one compact sticky rail row that matches the same selected-thread conversation id, phase, and follow state already driving the transcript and composer, while degraded, switch, restore, and terminal paths continue to clear or fail open immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through live proposal, review, verify, auto-apply, ready, and applied states.
5. Confirm the left rail shows exactly one sticky active-session row for the selected thread.
6. Confirm that row matches the same conversation id, phase, and follow state already shown by the selected transcript inline block and composer dock.
7. Confirm the row remains non-authoritative and chip-first, and that no selected-card or non-selected row gains a second live-owned marker while it is present.
8. Confirm reconnect downgrade, polling fallback, deselection, and terminal completion clear or downgrade the sticky rail row immediately.
9. Confirm switch and restore paths still use the existing fail-open transition behavior without stale rail ownership.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the sticky rail row mirrors the selected live session without conflicting with transcript or composer datasets and without creating duplicate rail ownership surfaces.
