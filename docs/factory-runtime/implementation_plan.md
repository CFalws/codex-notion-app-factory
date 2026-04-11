# Factory Runtime Implementation Plan

## Iteration 175

Make the sticky active-session row the single healthy navigation mirror for the selected thread.

1. Keep the change presentation-only inside the left navigation seam over the existing selected-thread authority.
2. Let the sticky active-session row remain the only healthy live navigation mirror for the selected thread.
3. Suppress selected-card helper live detail when that sticky row is authoritative.
4. Keep selected-card session chips minimal and finite.
5. Fail closed immediately on degraded, restore-gap, deselected, switched, and terminal paths.
6. Align focused verification and proposal artifacts with the iteration-175 rail-authority contract.
