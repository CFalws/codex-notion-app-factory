# Factory Runtime Deploy Plan

## Iteration 238

This deploy plan validates the unified selected-thread header capsule as the only visible live-session surface in the center header.

## Deployment Impact

This iteration keeps runtime behavior otherwise intact and collapses the center header into one compact session capsule. The gate should pass only when that capsule remains strictly derived from selected-thread `conversation.session_status`, the legacy phase badge stays non-visible, and degraded or terminal transitions clear or downgrade the header immediately without affecting the existing transcript inline session block.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and a switch or restore path on desktop and phone widths.
5. Confirm the center header shows one compact chip-first session capsule carrying scope, path, owner, and phase together.
6. Confirm the legacy phase badge does not remain visible as a second center-header live-status surface.
7. Confirm the transcript inline session block, footer dock, left-rail cues, and switch or restore continuity remain unchanged.
8. Confirm the header capsule reflects selected-thread `conversation.session_status` state without append-coupled lag.
9. Confirm switch, terminal resolution, reconnect downgrade, polling fallback, and deselection clear or downgrade the header capsule immediately with no stale retention.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, and free of split center-header status ownership.
