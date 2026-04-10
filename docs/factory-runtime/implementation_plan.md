# Factory Runtime Implementation Plan

1. Keep the existing selected-thread session summary surface, transcript timeline, composer dock, recent-thread rail, and side-panel behavior unchanged.
2. Reuse the current `selectedThreadLiveSessionIndicator` mapping as the single header ownership source for healthy SSE, reconnect, and polling fallback states.
3. Change the healthy selected-thread header chip to an explicit `SSE OWNER` marker while preserving degraded `RECONNECT` and `POLLING` states.
4. Publish machine-readable source, ownership, and reason datasets directly on the header ownership chip so browser verification can prove intended-path transport in the main workspace.
5. Update the selected-thread session summary copy and durable verifier/doc artifacts to match the explicit ownership-chip contract.
