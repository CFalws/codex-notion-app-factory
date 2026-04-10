# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, session strip ownership, bottom follow control, footer composer, and non-selected snapshot rows unchanged.
2. Let only the currently selected row mirror selected-thread handoff or live-owner state in the left rail.
3. Reuse the existing selected-thread `HANDOFF`, `LIVE`, `NEW`, and `PAUSED` state derivation instead of adding a second navigation-specific status source.
4. Clear selected-row live-owner treatment immediately on thread switch, reconnect downgrade, polling fallback, or terminal resolution.
5. Keep the focused verifier and durable docs aligned with the selected-row-only live-owner contract.
