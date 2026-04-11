# Factory Runtime Deploy Plan

## Iteration 211

This deploy plan validates selected-thread switch continuity in the center workspace and composer handoff.

## Deployment Impact

This iteration keeps transport and ownership unchanged while tightening switch continuity. Intentional selected-thread switches should keep the mounted center workspace and composer visible, clear old-thread ownership immediately, and show at most one compact switching placeholder until the new snapshot attaches.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Start from a healthy selected-thread conversation and intentionally switch to another conversation from the rail.
6. Confirm the center conversation shell and bottom-fixed composer stay mounted for the full switch path.
7. Confirm old-thread live ownership clears immediately when the switch starts.
8. Confirm the center timeline shows at most one compact switching placeholder and never flashes the generic empty workspace during the switch path.
9. Confirm true no-selection idle still renders the generic empty workspace.
10. Confirm reconnect downgrade, polling fallback, deselection, restore-gap loss, and terminal resolution still clear live-owned switch surfaces immediately.
11. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the switch keeps the mounted shell and composer, avoids the empty-state flash, limits the placeholder to one compact block, and clears stale ownership immediately.
