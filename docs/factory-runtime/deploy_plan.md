# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It removes duplicated active-pane header status surfaces while leaving the selected-conversation live path, transcript handoff states, composer-adjacent activity bar, desktop secondary panel, mobile drawer behavior, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and confirm the transcript begins immediately below the active-thread header.
4. Verify the header now shows only conversation identity and navigation controls, with no duplicated live-status chips or in-pane autonomy strip above the timeline.
5. Confirm the composer-adjacent activity bar remains the only visible live-status surface inside the conversation pane.
6. Open the secondary panel and confirm deeper operator and autonomy detail remain reachable there.
7. On phone width, confirm the same conversation-first reading flow works without breaking the existing mobile drawer or sticky footer dock.
