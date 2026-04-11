# Factory Runtime Implementation Plan

## Iteration 123

Tighten healthy selected-thread authority so poll-driven job and goals refresh cannot reclaim visible state after SSE becomes authoritative.

1. Reuse `isSelectedThreadSessionOwned(...)` as the single poll-fallback gate in the job controller.
2. Prevent late poll ticks from updating visible job meta, proposal readiness, conversation refetch, or goal-summary refresh once the selected-thread SSE path is authoritative.
3. Preserve reconnect and polling fallback behavior by allowing poll-driven updates only when selected-thread SSE ownership is no longer healthy.
4. Leave the timeline, header, and footer render surfaces unchanged so they continue projecting the same selected-thread live append state.
5. Extend the focused verifier layer and proposal artifacts so iteration 123 proves healthy selected-thread SSE authority suppresses poll-driven visible state updates.
