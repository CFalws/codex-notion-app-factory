# Factory Runtime Implementation Plan

## Iteration 173

Make selected-thread `session_status` the healthy live autonomy source across the workspace.

1. Keep the change read-only over the existing selected-thread append SSE and `session_status` seam.
2. Derive autonomy summary state from canonical `session_status` during healthy selected-thread ownership.
3. Suppress goals polling fallback on the intended healthy selected-thread SSE path.
4. Keep degraded, restore, deselected, reconnect, and polling-owned paths explicitly non-authoritative.
5. Make the store prefer canonical `session_status` autonomy fields over stale fallback summary state while healthy ownership is active.
6. Align focused verification and proposal artifacts with the iteration-173 autonomy authority contract.
