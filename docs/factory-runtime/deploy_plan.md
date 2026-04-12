# Factory Runtime Deploy Plan

## Iteration 233

This deploy plan validates inline selected-thread transition continuity in the deployed workspace gate.

## Deployment Impact

This iteration keeps runtime behavior otherwise intact and removes placeholder-mode ownership during selected-thread switch and restore. The gate should pass only when the center pane stays in conversation mode, one inline transition item represents attach or restore progress, the composer shell remains mounted, and degraded fallback still clears healthy ownership immediately instead of looking like live continuity.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger an intentional thread switch and a saved restore or resume path.
5. Confirm the center conversation shell stays mounted and the bottom composer remains fixed through each transition.
6. Confirm exactly one inline `timeline-transition` item represents attach or restore progress inside the canonical conversation timeline.
7. Confirm the conversation timeline stays in conversation mode rather than switching into placeholder ownership semantics.
8. Confirm the composer target row and session strip stay synchronized with the same transition state.
9. Confirm reconnect downgrade, polling fallback, switch, deselection, restore failure, and terminal transitions clear healthy ownership immediately with no stale revival.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, and free of placeholder-mode transition ownership.
