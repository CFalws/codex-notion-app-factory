# Factory Runtime Implementation Plan

## Iteration 154

Demote the selected-thread secondary panel into a compact detail drawer.

1. Reuse the existing selected-thread session surface, phase progression, verifier, blocker, and follow-control models to render compact facts at the top of the secondary panel.
2. Keep the transcript and bottom composer as the only primary live session surfaces.
3. Keep autonomy and execution content in the secondary panel as detail-only drill-down content rather than center-lane substitutes.
4. Mirror healthy, degraded, switching, restore, and idle selected-thread states into the panel facts header without introducing new state or transport sources.
5. Extend focused static and deployed verification so the panel stays collapsed by default, exposes compact selected-thread facts when opened, and clears stale ownership immediately on degraded and switching paths.
6. Align proposal artifacts with the iteration-154 secondary-panel detail-drawer contract.
