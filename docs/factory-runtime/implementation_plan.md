# Factory Runtime Implementation Plan

1. Keep the existing conversation-first shell, transcript timeline, bottom-fixed composer, composer owner row, and selected-thread inline session block unchanged as the primary workspace structure.
2. Reuse the selected-thread SSE ownership, pending handoff, live phase, and terminal-retention selectors through one shared inline-session visibility helper.
3. Use that helper to keep the inline session block as the only healthy selected-thread live-progress surface in the center timeline.
4. Suppress the composer-adjacent live strip whenever the inline session block is active, while preserving selected-thread ownership datasets on the thread scroller for follow-state behavior.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the single-surface healthy live-progress contract.
