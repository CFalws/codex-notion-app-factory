# Factory Runtime Implementation Plan

## Iteration 94

Project the selected-thread SSE path into one explicit phase progression model without changing transport or polling behavior.

1. Add a canonical selected-thread live-autonomy helper and a canonical selected-thread phase-progression helper in `ops-store.js`.
2. Mark autonomy summaries projected from healthy selected-thread SSE append events as `source: "sse"`, `freshnessState: "fresh"`, and `fallbackAllowed: false`.
3. Reuse the canonical phase-progression helper in the transcript live session surface and the inline autonomy or session surface so proposal, review, verify, auto-apply, ready, applied, and fallback states read consistently.
4. Extend `deriveLiveRunState(...)` to recognize `AUTO APPLY` from the existing `goal.proposal.auto_apply.started` SSE event path so the composer-adjacent strip stays aligned with the center timeline.
5. Reconfirm the focused verifier layer and record the iteration-94 phase progression contract in the durable proposal artifacts.
