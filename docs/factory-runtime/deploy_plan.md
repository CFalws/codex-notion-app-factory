# Factory Runtime Deploy Plan

## Iteration 242

This deploy plan validates that the left-rail active-session row is an explicit canonical mirror of the selected-thread session-status plus SSE path.

## Deployment Impact

This iteration keeps transport and authority behavior intact and corrects the left-rail ownership contract. The gate should pass only when the sticky active-session row is visibly canonical and owned on the healthy selected-thread SSE path, while degraded or switched paths clear that row immediately and non-selected rows remain snapshot-only.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and a switch or restore path on desktop and phone widths.
5. Confirm the sticky active-session row is visible for the healthy selected thread and reports owned plus canonical state from the selected-thread SSE path.
6. Confirm the transcript inline session block remains the only in-timeline live progress surface.
7. Confirm the unified header capsule, footer dock, and left-rail cues remain coherent on the same selected-thread authority path.
8. Confirm non-selected rows remain snapshot-only and do not appear live-owned.
9. Confirm thread switch, reconnect downgrade, polling fallback, terminal resolution, and deselection visibly downgrade or clear active-session ownership with no stale retention.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, and the active-session row is canonical only on the intended selected-thread SSE path.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
