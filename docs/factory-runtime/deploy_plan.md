# Factory Runtime Deploy Plan

## Iteration 99

This deploy plan validates the machine-readable selected-thread restore-stage contract and does not introduce new transport, new polling gates, or new status surfaces beyond that bounded frontend presentation change.

## Deployment Impact

This iteration changes selected-thread restore continuity and verification surface only. The bounded expectation is that reload or re-entry with a saved selected conversation immediately shows exactly one transcript-tail restore item, the header and composer expose the same machine-readable restore stage without flashing generic snapshot-ready state, degraded reconnect or polling paths stay visibly downgraded, and existing polling behavior remains unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation and one additional conversation for switching.
4. Reload the workspace or re-enter with a saved selected conversation and confirm the transcript tail immediately shows exactly one restore `ATTACH` or `RESUME` item for that conversation.
5. Confirm the compact header summary, composer ownership row, session strip, and thread scroller all expose matching restore stage, path, and provenance datasets while restore is pending.
6. Confirm no snapshot `READY` or `ATTACHED` label appears before authoritative selected-thread SSE bootstrap succeeds.
7. Confirm the same selected thread transitions in place to healthy SSE ownership, with no conversation refetch and no `/api/jobs` or `/api/goals` owned success on the healthy path.
8. Switch threads and confirm the old restore owner clears immediately while the mounted shell and fixed composer continuity still hold.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread restore contract succeeds through the intended authoritative SSE path.
