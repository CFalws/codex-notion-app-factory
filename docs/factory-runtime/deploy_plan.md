# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It keeps the selected-conversation SSE path, transcript follow behavior, footer dock, compact composer state row, and left-rail session markers intact, but shortens the selected-thread live rail so the active workspace reads through chips and compact cues instead of sentence-level strip text.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open an active conversation on desktop and phone widths and trigger sending, live, review, verify, proposal-ready, done, and failed states through the healthy selected-thread SSE path.
4. At desktop width, confirm the transcript remains the first readable content below the minimal header and above the bottom composer.
5. Confirm the selected-thread live rail exposes compact transport, phase, proposal, provenance, and action cues without reverting to sentence-level status text.
6. Confirm richer autonomy and operator detail remains reachable only through the existing secondary panel, and opening that panel does not create a third primary workspace column.
7. Confirm polling only appears as degraded fallback when the append stream is absent or interrupted.
