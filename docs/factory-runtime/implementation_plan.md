# Factory Runtime Implementation Plan

## Iteration 170

Collapse healthy selected-thread milestone appends into the transcript-tail live activity.

1. Keep the change read-only over the existing selected-thread SSE authority and transcript-tail live activity seam.
2. Treat the transcript-tail live activity as the only healthy selected-thread primary session item in the center pane.
3. Collapse proposal, review, verify, auto-apply, ready, and applied milestone session-event cards only while the selected-thread live item is healthy and SSE-owned.
4. Leave degraded, restore, snapshot, switching, and terminal-cleared paths explicit so they do not silently inherit healthy milestone ownership.
5. Keep non-live historical rendering behavior intact outside the healthy selected-thread path.
6. Align focused verification and proposal artifacts with the iteration-170 unified live-timeline contract.
