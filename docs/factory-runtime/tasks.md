# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, session strip ownership, bottom follow control, footer composer, and non-selected snapshot rows unchanged.
- [x] Mirror selected-thread live-owner state only in the currently selected conversation row.
- [x] Reuse compact `HANDOFF`, `LIVE`, `NEW`, and `PAUSED` selected-row cues plus the existing follow or unread detail.
- [x] Keep all non-selected rows snapshot-only.
- [x] Clear selected-row live-owner treatment immediately on thread switch, reconnect downgrade, polling fallback, or terminal resolution.
- [x] Align focused verification and iteration artifacts with the selected-row-only live-owner contract.
