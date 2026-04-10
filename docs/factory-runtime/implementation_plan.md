# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, center-pane inline session block, and live-follow behavior unchanged.
2. Mirror the selected-thread handoff and live session state into the left conversation card only, keeping non-selected rows snapshot-only.
3. Render compact selected-card detail and follow chips that cover pending handoff, active live progress, and fresh assistant-append completion, then clear on terminal resolution or thread switch.
4. Preserve transcript plus composer primacy on desktop and phone widths while making the selected rail row more informative without adding a new panel.
5. Extend the focused verifier and docs so future sessions can prove the selected card alone mirrors the selected-thread live path.
