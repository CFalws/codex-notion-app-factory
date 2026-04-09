# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, compact composer row, left rail markers, pending-turn handoff, and central timeline unchanged.
2. Preserve only thread identity and navigation affordances in the desktop active-pane header.
3. Remove stale render hooks and CSS for header-level autonomy and status chrome that no longer have DOM ownership.
4. Keep fuller autonomy, review, verifier, and operator detail only in the existing secondary panel.
5. Extend the focused verifier and docs so future sessions can prove the active-pane header stays minimal and the transcript remains the first readable desktop surface.
