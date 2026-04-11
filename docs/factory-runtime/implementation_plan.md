# Factory Runtime Implementation Plan

## Iteration 120

Tighten the sticky left-rail active-session row so it mirrors only the healthy selected-thread SSE session and clears immediately on degraded or non-selected paths.

1. Reuse `deriveSelectedThreadSessionStatus(...)` and `deriveSelectedThreadFollowControlModel(...)` as the only active-session row inputs.
2. Keep the row visible only for the healthy selected-thread SSE-owned path instead of transition or handoff or degraded branches.
3. Mirror owner, current phase, and `NEW` or `PAUSED` follow state with unseen-count metadata from the canonical selected-thread datasets.
4. Clear the row on switching, polling fallback, reconnect downgrade, terminal idle, and deselection so no stale live-owned rail surface survives outside the intended path.
5. Extend the focused verifier layer and proposal artifacts so iteration 120 proves both presence on the healthy path and absence on degraded or switching paths.
