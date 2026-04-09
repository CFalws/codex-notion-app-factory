# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, header phase chip, left rail, footer dock, and live-follow behavior unchanged.
2. Reuse the existing selected-thread live-run derivation, but mirror its current phase and detail into one compact transcript-tail activity item for the active conversation only.
3. Show that tail item only while the selected conversation is currently driven by selected-thread SSE state, and let it resolve cleanly without duplicating itself across rerenders.
4. Preserve transcript plus composer reachability and keep non-selected threads snapshot-only on desktop and phone widths.
5. Extend the focused verifier and docs so future sessions can prove the transcript-tail activity turn remains selected-thread-SSE-owned.
