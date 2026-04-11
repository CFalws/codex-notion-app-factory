# Factory Runtime Deploy Plan

## Iteration 181

This deploy plan validates the selected-thread switch continuity path as one continuous conversation workspace.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while validating that intentional switches stay inside the existing workspace shell, clear stale old-thread ownership immediately, and use one compact transition placeholder until attach completes.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled, then intentionally switch to a different conversation.
5. Confirm the center transcript shell stays mounted, the composer dock stays visible, old-thread live ownership clears immediately, and exactly one compact switching placeholder is shown while the incoming snapshot attaches.
6. Confirm the generic empty workspace does not flash during the switch and that the incoming thread becomes authoritative as soon as its snapshot or live session attaches.
7. Confirm reconnect downgrade, polling fallback, restore-gap, deselection, switch cancellation ambiguity, and terminal idle still clear or neutralize session-owned UI immediately.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch path stays on the compact transition placeholder, never flashes the generic empty workspace, and keeps the composer target pinned to the incoming thread.
