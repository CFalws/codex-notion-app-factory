# Factory Runtime Implementation Plan

## Iteration 166

Preserve the selected-thread conversation shell and composer dock during intentional thread switches.

1. Keep the change read-only over the existing selected-thread ownership and switch seam.
2. Preserve the center shell and bottom-fixed composer dock while an intentional thread switch is in flight.
3. Keep exactly one compact transition placeholder visible until the new selected-thread snapshot attaches or the switch is cancelled.
4. Clear old-thread live ownership immediately on switch and fail closed on reconnect downgrade, polling fallback, deselection, terminal completion, or lost authority.
5. Keep the composer target row finite and explicit so switch state remains legible at the bottom dock.
6. Align focused verification and proposal artifacts with the iteration-166 switch-continuity contract.
