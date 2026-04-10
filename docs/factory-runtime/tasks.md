# Factory Runtime Tasks

- [x] Keep the selected-thread inline timeline surface, bottom-fixed composer, and degraded polling fallback paths unchanged.
- [x] Reuse selected-thread SSE ownership and `deriveLiveRunState` as the healthy ownership source for visible phase and proposal/apply readiness.
- [x] Update the recent-activity panel to use conversation events and live-run phase directly while healthy selected-thread SSE ownership holds.
- [x] Preserve job payload and polling status as the fallback path for degraded, non-selected, reconnecting, or switched-thread states.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the selected-thread SSE-owned status contract.
