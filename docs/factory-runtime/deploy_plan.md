# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It fuses the selected-thread live session strip and footer status into one compact composer-adjacent activity bar while leaving the selected-conversation live path, thread-header context strip, desktop secondary panel, mobile drawer behavior, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and confirm the transcript remains the dominant reading surface in the center pane.
4. Verify the selected-thread live activity now appears as one compact bar immediately above the composer rather than as a separate strip plus footer status.
5. Confirm the unified activity bar clears on idle, terminal completion, and thread switch.
6. Open the secondary panel and confirm deeper operator detail remains there rather than reappearing in the center pane.
7. On phone width, confirm the existing mobile drawer and sticky footer dock still behave correctly with the unified activity bar.
