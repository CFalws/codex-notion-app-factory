# Factory Runtime Tasks

## Iteration 173

- [x] Keep the autonomy-state change read-only over the existing selected-thread append SSE and `session_status` seam.
- [x] Derive visible selected-thread autonomy state from canonical `session_status` on the healthy SSE-owned path.
- [x] Suppress goals polling fallback on the intended healthy selected-thread SSE path.
- [x] Fail closed back to degraded or polling treatment on reconnect, restore gap, deselection, and polling-owned paths.
- [x] Make the selected-thread store prefer canonical `session_status` autonomy fields while healthy ownership is active.
- [x] Align focused docs and verification with the iteration-173 autonomy authority contract.
