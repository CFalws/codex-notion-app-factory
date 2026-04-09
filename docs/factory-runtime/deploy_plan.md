# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It moves autonomy context out of the center-pane reading flow into a compact thread-header strip plus secondary-panel detail while leaving the selected-conversation live path, desktop secondary panel, mobile drawer behavior, phone footer dock, and thread rail markers intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and confirm the transcript is the first visible content below the active thread header.
4. Verify the compact autonomy context strip appears inside the thread header and only shows the latest blocker, verifier acceptability, and iteration status without pushing the transcript down with a standalone summary block.
5. Open the secondary panel and confirm the fuller autonomy detail remains reachable there.
6. Switch conversations and confirm the active-thread context strip clears stale state correctly.
7. On phone width, confirm the existing mobile drawer, sticky footer dock, and live session strip behavior remain unchanged.
