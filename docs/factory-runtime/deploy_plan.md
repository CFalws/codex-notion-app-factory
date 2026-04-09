# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It adds compact left-rail thread status markers while leaving the selected-conversation live path, desktop secondary panel, mobile drawer behavior, and phone footer dock intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on desktop width and confirm the left rail still remains continuously visible while the transcript and composer dominate the center pane.
4. Verify the selected conversation shows an `ACTIVE` marker in the left rail and that the selected thread gains compact live-state markers such as connecting, reconnecting, running, or done directly in navigation.
5. Confirm those left-rail live markers clear when the session returns to idle or when a different conversation is selected.
6. Open and close the secondary panel from the thread header and confirm the center conversation view remains intact.
7. On phone width, confirm the existing mobile drawer and sticky footer dock still behave unchanged.
