# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It tightens the selected-conversation live rail so active states stay expanded while idle or terminal states collapse into a one-line latest-result summary with an in-rail re-expand affordance. The selected-conversation SSE path, transcript follow behavior, navigation structure, desktop secondary panel, phone footer dock, and thread rail markers remain intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console with an active generating conversation and confirm the live rail stays expanded while selected-thread SSE events update it.
4. Wait for a terminal or idle state and confirm the rail collapses into a one-line latest-result summary instead of disappearing.
5. Use the in-rail toggle and confirm the user can re-expand terminal or idle detail without opening any secondary panel.
6. Confirm the rail remains expanded during reconnecting or renewed live execution and does not hide the latest active state.
7. Confirm the composer-adjacent rail remains the only visible live-status surface inside the conversation pane.
