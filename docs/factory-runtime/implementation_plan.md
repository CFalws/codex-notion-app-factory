# Factory Runtime Implementation Plan

## Iteration 102

Make intentional selected-thread switching read as one continuous session workspace without changing transport or introducing a new render surface.

1. Reuse the existing `threadTransition` and selected-thread session-status helpers instead of introducing another switch state model.
2. Keep the center conversation shell mounted and render exactly one compact transition placeholder while `threadTransition` is active.
3. Make the composer strip show an explicit `SWITCHING` target state during attach instead of a generic target label.
4. Clear switch mirrors from the recent-thread rail so the transition is owned by the center pane and fixed composer only.
5. Extend the focused verifier layer and proposal artifacts so the switch path proves no empty-state flash, no stale old-thread ownership, and no polling-owned success presentation.
