# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It adds a narrow-screen navigation drawer while leaving desktop hierarchy and the selected-conversation live workspace path intact. Broader polling, transport, and proposal behavior stay unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console on a phone-width viewport and confirm the selected conversation is visible before app and thread controls.
4. Open the mobile drawer with one tap, switch app or conversation, and confirm the drawer closes back to the active workspace.
5. Verify the main pane still shows the autonomy rail, live run row, append stream strip, and composer in the active conversation path.
6. Confirm desktop width remains unchanged and that machine-readable live-state markers are still present for browser verification.
