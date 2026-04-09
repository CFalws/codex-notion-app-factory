# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It keeps the selected-conversation SSE path, transcript follow behavior, footer dock, compact composer state row, and left-rail session markers intact, but removes stale header-only autonomy and status chrome so the desktop active pane stays minimal.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open an active conversation on desktop and phone widths and trigger sending, live, review, verify, proposal-ready, done, and failed states through the healthy selected-thread SSE path.
4. At desktop width, verify the active-pane header shows only conversation identity, navigation affordances, and the existing secondary-panel toggle.
5. Confirm the first readable content below the header is the transcript, with the compact composer row remaining the only in-pane live-status surface above the bottom composer.
6. Confirm richer autonomy and operator detail remains reachable only through the existing secondary panel, and opening that panel does not create a third primary workspace column.
7. Confirm polling only appears as degraded fallback when the append stream is absent or interrupted.
