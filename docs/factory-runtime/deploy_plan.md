# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It turns the footer into a more compact chat-style session composer while leaving the selected-conversation live path, transcript handoff states, composer-adjacent activity bar, desktop secondary panel, mobile drawer behavior, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and confirm the footer reads like a chat composer with the textarea as the dominant surface.
4. Verify send is the primary action, while proposal apply and auto-open remain accessible without competing with normal message entry.
5. Confirm the composer-adjacent activity bar remains the only visible live-status surface inside the conversation pane.
6. Open the secondary panel and confirm deeper operator and autonomy detail remain reachable there.
7. On phone width, confirm the same conversation-first reading flow works without breaking the existing mobile drawer or sticky footer dock.
