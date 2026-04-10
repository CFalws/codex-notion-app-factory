# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, dock behavior, transcript-tail live item, and non-selected snapshot rows unchanged.
2. Strengthen the selected row as the sole rail live-owner surface by giving it one explicit owner-state contract for handoff, live, new, and paused conditions.
3. Derive that owner-state contract from the existing pending handoff state, selected-thread SSE ownership, and live-follow state, and clear it immediately when render ownership degrades to snapshot or the user switches threads.
4. Preserve phone and desktop scanability by keeping non-selected rows limited to their fixed snapshot labels and bounded preview lines.
5. Extend the focused verifier and docs so future sessions can prove selected-row live ownership, state-specific cues, and immediate clearing on reconnect fallback, terminal resolution, or thread switch.
