# Factory Runtime Deploy Plan

## Iteration 146

This deploy plan validates the selected-thread switch-continuity contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread switch presentation and verification only. The bounded expectation is that an intentional thread switch keeps the conversation shell and fixed composer in place, shows one compact switching placeholder, and never flashes the generic empty-state until the new selected-thread snapshot or live session attaches.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open one selected-thread conversation, then intentionally switch to a different thread while the workspace is active.
5. Confirm the previous thread's live-owned cues clear immediately, the generic empty-state never flashes, and at most one compact `SWITCHING` placeholder appears while the new selected-thread snapshot or live session is attaching.
6. Confirm the bottom-fixed composer dock and center conversation shell remain mounted throughout the switch window on desktop and phone widths.
7. Confirm the switching placeholder clears as soon as the new selected-thread snapshot or live session arrives, and that true idle with no selected conversation still renders the normal empty-state.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch-continuity contract succeeds through the intended selected-thread session path.
