# Factory Runtime Implementation Plan

## Iteration 151

Restore one compact inline selected-thread session block in the center conversation workspace.

1. Implement `renderInlineSessionBlock(...)` from the existing selected-thread session surface, phase progression, and live autonomy models.
2. Show the block only for healthy selected-thread SSE-owned live progress or pending assistant handoff.
3. Keep degraded, restore, terminal, deselected, non-selected, and switched-thread paths fail-closed so the inline block clears immediately when authority is lost.
4. Suppress the pending assistant placeholder when the handoff block is visible so the center lane keeps one compact live-session anchor instead of a second competing handoff surface.
5. Extend focused static and deployed verification so the healthy path requires exactly one selected-thread inline session block with matching phase, path, verifier, and blocker datasets, and degraded or switch paths require its absence.
6. Align proposal artifacts with the iteration-151 center-pane inline-session contract.
