# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, transcript-first center pane, and compact active-session strip unchanged in ownership.
2. Strengthen the selected conversation row with a selected-thread-only live-owner treatment that visually binds it to the center workspace.
3. Reuse the existing selected marker and session chip instead of adding a new status surface, but make their selected-live meaning more explicit.
4. Preserve non-selected rows as snapshot-only so they can still show compact idle or terminal cues without appearing actively streaming.
5. Extend the focused verifier and docs so future sessions can prove the selected row remains the only live-owned lane in the rail.
