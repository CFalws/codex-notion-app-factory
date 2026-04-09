# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It makes the phone-width nav sheet conversation-first while leaving the selected-conversation live path, transcript handoff states, composer-adjacent activity bar, desktop secondary panel, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on phone width and confirm the nav sheet opens with the conversation list as the first actionable surface.
4. Verify the selected or generating thread remains identifiable from the first-visible conversation list and that switching threads still takes one tap.
5. Confirm app selector, refresh, deployment link, and related operator controls remain reachable through the collapsed operator section without displacing the thread list.
6. Open the same console on desktop width and confirm the sidebar still behaves like the existing left rail.
7. Confirm the composer-adjacent activity bar remains the only visible live-status surface inside the conversation pane.
