# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It repositions the autonomy summary into a compact header-adjacent rail while leaving the selected-conversation live workspace path intact. Broader polling, transport, and proposal behavior stay unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open one active conversation and confirm message history is immediately visible without a large autonomy card above it.
4. Confirm the autonomy blocker, path verdict, and verifier state are still visible in the compact rail below the header.
5. Verify the rail still exposes machine-readable autonomy attributes and that the selected thread keeps the inline live-run row and append provenance markers.
6. Check mobile width and confirm the thread plus composer remain easier to reach because the autonomy summary no longer occupies the top of the scrollable body.
