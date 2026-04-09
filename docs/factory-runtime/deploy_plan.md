# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It keeps the selected-conversation SSE path, transcript follow behavior, footer dock, and live phase model intact, but compresses the composer-adjacent status surface into a compact state row with fixed chips and short affordance text.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open an active conversation on desktop and phone widths and trigger sending, live, review, verify, proposal-ready, done, and failed states through the healthy selected-thread SSE path.
4. Verify the composer dock shows a compact row of transport, phase, and proposal chips rather than long explanatory strip copy.
5. Confirm the short affordance line and send or apply button copy adapt to the selected-thread state only and never imply live state for non-selected conversations.
6. Confirm the transcript-plus-bottom-composer layout remains unchanged and the compact state row remains the only visible in-pane live-status surface inside the conversation pane.
7. Confirm polling only appears as degraded fallback when the append stream is absent or interrupted.
