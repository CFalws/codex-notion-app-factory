# Factory Runtime Deploy Plan

## Iteration 236

This deploy plan validates that thread navigation is owned by the left rail or mobile nav sheet while the center pane remains transcript-first.

## Deployment Impact

This iteration keeps runtime behavior otherwise intact and removes center-pane recent-thread navigation chrome. The gate should pass only when the center pane stays transcript-first, selected-thread switch and restore still use one inline transition item, the composer shell remains mounted, and degraded fallback still clears healthy ownership immediately instead of looking like live continuity.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger an intentional thread switch and a saved restore or resume path from the left rail or mobile nav sheet.
5. Confirm the center conversation shell stays mounted and the bottom composer remains fixed through each transition.
6. Confirm exactly one inline `timeline-transition` item represents attach or restore progress inside the canonical conversation timeline.
7. Confirm the center pane no longer renders recent-thread navigation chrome and remains focused on transcript, live session surfaces, and the composer.
8. Confirm the composer target row and session strip stay synchronized with the same transition state.
9. Confirm reconnect downgrade, polling fallback, switch, deselection, restore failure, and terminal transitions clear healthy ownership immediately with no stale revival.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, and free of center-pane navigation duplication.
