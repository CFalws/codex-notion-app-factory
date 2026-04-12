# Factory Runtime Implementation Plan

## Iteration 229

Resolve the selected-thread submit-to-first-append handoff gap.

1. Keep the change bounded to the selected-thread handoff path and matching proposal artifacts.
2. Reuse the existing pending outgoing state, inline session block, composer-adjacent activity bar, and selected-thread SSE ownership datasets instead of adding new runtime behavior.
3. Preserve the center conversation shell and bottom-fixed composer through the full submit-to-first-append interval.
4. Keep exactly one handoff owner visible at a time: pending outbound user or temporary assistant placeholder, never both.
5. Clear the handoff owner immediately on first real assistant SSE append, terminal failure, idle reset, polling fallback, reconnect downgrade, or intentional thread switch.
6. Align static checks, browser checks, and proposal artifacts with the selected-thread handoff continuity contract.
