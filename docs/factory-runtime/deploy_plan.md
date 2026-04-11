# Factory Runtime Deploy Plan

## Iteration 199

This deploy plan validates selected-thread switch continuity as one continuous session workspace transition.

## Deployment Impact

This iteration keeps transport and selected-thread ownership unchanged while validating that an intentional selected-thread switch keeps the center conversation shell and composer dock mounted, clears old ownership immediately, and uses one compact switching placeholder instead of the generic empty workspace.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled.
5. Intentionally switch to another thread and confirm the center conversation shell and composer dock stay mounted.
6. Confirm the outgoing thread clears live-owned markers immediately, exactly one compact switching placeholder appears, and the generic empty workspace never flashes.
7. Confirm the incoming thread snapshot attaches into the same mounted workspace and that reconnect, restore-gap, deselection, and terminal idle still fail closed when they should.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch path passes only when there is one compact placeholder, no empty-state flash, no hidden composer dock, and no stale selected-thread live ownership.
