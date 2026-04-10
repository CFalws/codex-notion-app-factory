# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer dock, sticky active-session row, and side-panel behavior unchanged.
2. Reuse the existing conversation message and event history instead of introducing another preview or state source.
3. Expand the non-selected snapshot label vocabulary so waiting, active, ready, done, failed, and idle states remain distinguishable without making any non-selected row live-owned.
4. Keep one bounded preview line per row and prefer recent assistant or user message text over event prose whenever message content exists.
5. Keep the focused verifier and durable docs aligned with the compact snapshot-label and preview contract.
