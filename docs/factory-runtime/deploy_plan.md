# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It adds a temporary pending outbound message and a short sending handoff state to the existing active conversation flow while leaving the selected-conversation live path, thread-header context strip, composer-adjacent activity bar, desktop secondary panel, mobile drawer behavior, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and submit a request in an active conversation.
4. Verify a temporary pending user message appears in the transcript immediately and the composer-adjacent activity bar shows a sending handoff state before the first accepted or live signal arrives.
5. Confirm the pending item clears or is replaced when the accepted response or first live append lands, and that no duplicate or stale pending item remains on failure, idle, or thread switch.
6. Open the secondary panel and confirm deeper operator detail remains there rather than reappearing in the center pane.
7. On phone width, confirm the same send handoff behavior works without breaking the existing mobile drawer or sticky footer dock.
