# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, transcript-first center pane, and selected-row live-owner treatment unchanged in ownership.
2. Refine non-selected conversation cards so their snapshot state resolves through one fixed-priority helper instead of a coarse idle or done fallback.
3. Refine preview selection so cards prefer the most useful recent assistant or user content before falling back to event summaries.
4. Preserve one bounded preview line and one snapshot-only chip per non-selected row so the rail stays compact on desktop and phone widths.
5. Extend the focused verifier and docs so future sessions can prove ready, review, verify, done, failed, and idle states stay distinguishable without implying live streaming off the selected thread.
