# Factory Runtime Deploy Plan

## Iteration 228

This deploy plan validates intentional selected-thread switch continuity in the deployed workspace gate.

## Deployment Impact

This iteration keeps runtime behavior unchanged and records the intended switch path. The gate should pass only when intentional selected-thread switches preserve the mounted shell and composer, clear old-thread ownership immediately, avoid empty-state flash, and limit the transition state to one compact placeholder until the new snapshot attaches.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation, then intentionally switch to another thread and back again.
5. Confirm the center conversation shell stays mounted and never flashes the generic empty workspace during the switch.
6. Confirm the bottom-fixed composer stays visible and attached through the full switch path.
7. Confirm old-thread live, phase, proposal, and follow ownership clear immediately at switch start.
8. Confirm exactly one compact selected-thread transition placeholder is visible until the target snapshot attaches.
9. Confirm only the newly selected thread can own the temporary transition state and no degraded or stale live owner revives during the handoff.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when intentional selected-thread switches preserve one continuous workspace surface with no empty-state flash and no duplicate transition ownership.
