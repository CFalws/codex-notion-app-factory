# Factory Runtime Implementation Plan

## Iteration 100

Keep the transcript-tail live activity item as the only healthy selected-thread SSE-owned session surface without changing transport or polling behavior.

1. Reuse the existing selected-thread store-owned session, restore, autonomy, and phase helpers.
2. Hide the composer-adjacent session strip on the healthy selected-thread SSE path so the center pane reads as one live session timeline.
3. Preserve the strip for restore, handoff, switching, reconnect, polling fallback, and other non-healthy states where explicit context is still needed.
4. Keep the compact header summary and fixed composer bound to the same conversation while removing duplicate healthy live-owned presentation.
5. Extend the focused verifier layer and proposal artifacts so the healthy path proves one session-owned center-pane live surface while degraded paths remain explicit.
