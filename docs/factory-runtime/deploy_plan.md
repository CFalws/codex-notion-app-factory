# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It adds a temporary assistant placeholder to the existing active conversation handoff while leaving the selected-conversation live path, pending outbound user bubble, thread-header context strip, composer-adjacent activity bar, desktop secondary panel, mobile drawer behavior, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and submit a request in an active conversation.
4. Verify the pending user bubble appears immediately, then an assistant placeholder appears in the transcript before the first real assistant content arrives.
5. Confirm the assistant placeholder is replaced without duplication when the first assistant append lands and that it clears on terminal failure, idle reset, or thread switch.
6. Open the secondary panel and confirm deeper operator detail remains there rather than reappearing in the center pane.
7. On phone width, confirm the same assistant-side handoff behavior works without breaking the existing mobile drawer or sticky footer dock.
