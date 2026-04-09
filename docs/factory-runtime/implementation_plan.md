# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, transcript-first center pane, phone conversation-first sheet behavior, and footer live rail unchanged.
2. Add one compact session marker to the selected conversation row so the active thread is recognizable directly from the left rail.
3. Preserve the same selected-thread live-run and append-stream inputs so no new transport inference, polling-owned state, or extra status source is introduced.
4. Keep non-selected rows snapshot-only while leaving transcript and composer reachability unchanged on desktop and phone widths.
5. Extend the focused verifier and docs so future sessions can prove the left rail distinguishes the selected live session without turning every row into a prose-heavy status surface.
