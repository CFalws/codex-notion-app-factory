# Factory Runtime Deploy Plan

## Iteration 216

This deploy plan validates selected-thread restore or resume continuity across the center workspace and composer handoff.

## Deployment Impact

This iteration keeps transport and ownership unchanged while tightening restore or resume continuity. Saved-session restore or resume should keep the mounted center workspace and composer visible, clear stale ownership immediately, and show exactly one compact restore or attach placeholder until authoritative SSE ownership returns.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a saved selected-thread conversation and trigger restore or resume by reopening or reselecting that conversation.
5. Confirm the center conversation shell and bottom-fixed composer stay mounted for the full restore or resume path.
6. Confirm exactly one compact restore or attach placeholder appears until authoritative SSE ownership returns.
7. Confirm stale live ownership clears before any degraded or fallback rendering appears.
8. Confirm no generic empty workspace flashes during restore or resume.
9. Confirm reconnect downgrade, polling fallback, deselection, and terminal resolution still clear live-owned restore surfaces immediately.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the restore or resume flow keeps the mounted shell and composer, avoids empty-state flash, limits the placeholder to one compact block, and clears stale ownership immediately before fallback state appears.
