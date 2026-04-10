# Factory Runtime Implementation Plan

1. Keep the existing selected-thread SSE ownership, inline live block, composer dock, and degraded fallback behavior unchanged.
2. Reuse the already-fetched relevant goal summary as a single cached `autonomySummary` snapshot in client state.
3. Project that summary into the existing inline live session block only while the selected thread owns the healthy live run.
4. Suppress the autonomy row on thread switch, degraded fallback, ownership loss, or no-goal states so the timeline stays single-surface.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the inline autonomy-visibility contract.
