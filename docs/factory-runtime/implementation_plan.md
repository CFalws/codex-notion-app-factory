# Factory Runtime Implementation Plan

## Iteration 153

Collapse the selected-thread center-pane realtime status surfaces into one transcript-native session timeline item.

1. Reuse the existing selected-thread primary timeline session helper as the single center-pane session contract.
2. Remove the standalone inline session block so healthy and handoff states render only through the transcript-native live activity item.
3. Preserve degraded and restore session visibility through that same transcript-native session item without leaving duplicate inline ownership behind.
4. Keep reconnect, polling fallback, switch, terminal, deselected, non-selected, and lost-authority paths fail-closed so no stale inline session surface remains mounted.
5. Extend focused static and deployed verification so healthy, degraded, restore, and switching states prove the center pane exposes exactly one selected-thread session item and zero duplicate inline session blocks.
6. Align proposal artifacts with the iteration-153 center-pane timeline convergence contract.
