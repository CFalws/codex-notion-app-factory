# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It merges the selected-conversation session strip and composer into one phone-width footer dock while leaving desktop hierarchy, mobile drawer behavior, and the existing live append path intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on a phone-width viewport and confirm the selected conversation is visible before app and thread controls.
4. Open the mobile drawer with one tap, switch app or conversation, and confirm the drawer closes back to the active workspace.
5. Verify the phone-width footer dock keeps the session strip and composer in one persistent region at the bottom of the active conversation.
6. Confirm the session strip still updates through connecting, live, reconnecting, idle collapse, and terminal collapse using the selected-conversation live path.
7. Switch conversations and confirm stale strip state clears immediately before the new thread loads.
8. Confirm desktop width remains unchanged and the autonomy rail plus composer remain easy to access.
