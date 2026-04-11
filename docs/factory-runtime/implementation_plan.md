# Factory Runtime Implementation Plan

## Iteration 86

Tighten the center-header session contract so the selected-thread workspace exposes attached target and live ownership state directly without widening transport or timeline scope.

1. Reuse the existing selected-thread session summary row and live-indicator datasets instead of adding another status surface.
2. Keep the summary row visible for selected-thread and switching contexts so the center pane remains the authoritative session-context surface.
3. Show healthy selected-thread ownership as `SSE OWNER`, degraded ownership as `RECONNECT` or `POLLING`, and clear ownership immediately on switch or terminal idle.
4. Keep the existing switch continuity, composer docking, and side-surface suppression intact while removing the hidden-header contract.
5. Reconfirm the focused browser-proof and static verifiers around the bounded center-header ownership contract.
