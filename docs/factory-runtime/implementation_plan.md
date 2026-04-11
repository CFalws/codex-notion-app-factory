# Factory Runtime Implementation Plan

## Iteration 152

Wire the existing left-rail sticky active-session row to selected-thread session authority.

1. Derive the sticky row only from the existing selected-thread session status, shell phase, and follow-control models.
2. Render the row only for healthy selected-thread ownership or bounded selected-thread handoff.
3. Keep reconnect, polling fallback, switch, terminal, deselected, non-selected, and lost-authority paths fail-closed so the sticky row clears immediately when authority is lost.
4. Keep the row compact while mirroring owner, phase, and follow or unseen cues from the selected-thread session contract.
5. Extend focused static and deployed verification so healthy, degraded, and switching states prove the sticky row matches the selected-thread contract and never preserves stale switching ownership.
6. Align proposal artifacts with the iteration-152 left-rail sticky-row contract.
