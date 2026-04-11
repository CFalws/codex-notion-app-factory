# Factory Runtime Implementation Plan

## Iteration 147

Collapse duplicate selected-thread SSE session-event cards into the canonical center-timeline live activity block.

1. Reuse the current selected-thread transcript live activity as the only primary center-lane session surface during active SSE-owned execution.
2. Add one explicit shared timeline-session helper so both live-activity rendering and session-event suppression follow the same selected-thread visibility contract.
3. Keep the live activity's existing phase, path verdict, verifier acceptability, blocker, and milestone chips as the in-place session progression surface.
4. Collapse duplicate selected-thread SSE session-event cards while that live activity block is visible, while preserving degraded, restore, handoff, terminal clear, and switch fail-closed behavior.
5. Extend focused static and deployed verification to require exactly one primary selected-thread live-session block and zero duplicate SSE session-event cards on the healthy intended path.
6. Align proposal artifacts with the iteration-147 unified center-timeline contract.
