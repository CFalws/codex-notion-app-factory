# Factory Runtime Deploy Plan

## Iteration 241

This deploy plan validates that the footer dock becomes the sole selected-thread follow owner while the existing session-status bootstrap plus SSE authority path remains unchanged.

## Deployment Impact

This iteration keeps transport and authority behavior intact and removes the detached follow surface. The gate should pass only when healthy selected-thread follow state appears only in the footer dock, the floating jump-to-latest control is absent, and degraded or switched paths clear footer follow ownership immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and a switch or restore path on desktop and phone widths.
5. Confirm the floating jump-to-latest control is absent on desktop and phone widths.
6. Confirm NEW or PAUSED follow state and unseen-count metadata appear only on the footer-dock action affordance.
7. Confirm the transcript inline session block remains the only in-timeline live progress surface.
8. Confirm the unified header capsule, footer dock, and left-rail cues remain coherent on the same selected-thread authority path.
9. Confirm thread switch, reconnect downgrade, polling fallback, terminal resolution, and deselection visibly downgrade or clear footer follow ownership with no stale retention.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, compact, and free of detached follow controls.
