# Factory Runtime Implementation Plan

1. Keep the existing selected-thread inline session block, bottom-fixed composer, and degraded polling fallback paths unchanged.
2. Reuse `deriveLiveRunState` and selected-thread SSE ownership as the single healthy realtime source for visible phase and proposal/apply readiness.
3. Update the recent-activity panel so healthy selected-thread SSE ownership uses conversation events and live-run phase directly instead of waiting for polled job payload status.
4. Keep the existing job payload path for degraded, non-selected, reconnecting, polling, or switched-thread states.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the selected-thread SSE-owned status-ownership contract.
