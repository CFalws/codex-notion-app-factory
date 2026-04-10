# Factory Runtime Implementation Plan

1. Keep the current selected-thread SSE path, conversation shell, footer composer dock, recent-thread rail, and side-panel behavior unchanged.
2. Reuse existing selected-thread append-stream, pending handoff, and live-run selectors to derive one inline transcript-tail session block without introducing a second live state source.
3. Show HANDOFF while the selected thread is awaiting the first assistant append, and show LIVE only while healthy SSE ownership remains active for that same selected thread.
4. Append the block at the transcript tail so the conversation stream stays the dominant surface, and clear it immediately on first real assistant append, terminal completion, reconnect downgrade, polling fallback, or thread switch.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the single inline transcript-tail session block contract.
