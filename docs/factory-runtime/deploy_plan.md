# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It keeps the selected-conversation SSE path, transcript follow behavior, footer dock, and compact composer state row intact, but tightens desktop layout into a conversation-first two-pane shell with a narrower left rail and an overlay secondary panel.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open an active conversation on desktop and phone widths and trigger sending, live, review, verify, proposal-ready, done, and failed states through the healthy selected-thread SSE path.
4. At desktop width, verify the shell reads as a narrow left rail plus dominant center conversation workspace before the secondary panel is opened.
5. Confirm the secondary panel opens as an overlay instead of becoming a third primary column, and that closing it returns to the same two-pane workspace.
6. Confirm the transcript-plus-bottom-composer layout remains unchanged and the compact state row remains the only visible in-pane live-status surface inside the conversation pane.
7. Confirm polling only appears as degraded fallback when the append stream is absent or interrupted.
