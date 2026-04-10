# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
2. Reuse the existing selected-thread handoff, SSE-live, and live-follow datasets instead of introducing another rail ownership source.
3. Replace the selected-row live-owner prose detail with finite compact chips that only expose current owner state and follow state.
4. Keep non-selected rows snapshot-only with one stable state label and one bounded preview line.
5. Keep the focused verifier and durable docs aligned with the finite selected-row chip contract.
