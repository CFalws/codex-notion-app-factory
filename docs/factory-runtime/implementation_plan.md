# Factory Runtime Implementation Plan

## Iteration 148

Mirror the selected-thread session into the left-rail active-session row through one store-owned row model.

1. Add one canonical selected-thread active-session row helper in the store derived from selected-thread session status, shell phase, and follow-control state.
2. Use that helper as the only source for the active-session row instead of reading summary or header state back out of the DOM.
3. Show compact `HANDOFF`, `LIVE`, `NEW`, `PAUSED`, and bounded `SWITCHING` cues through the existing row chips and datasets.
4. Keep degraded, polling, reconnect, terminal, deselection, and non-selected paths fail-closed so the row clears immediately when authority is lost.
5. Extend focused static and deployed verification so the left-rail row is checked against the same selected-thread session contract as the center workspace, including switching behavior.
6. Align proposal artifacts with the iteration-148 left-rail session-mirroring contract.
