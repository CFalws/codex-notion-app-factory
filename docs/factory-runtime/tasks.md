# Factory Runtime Tasks

## Iteration 229

- [x] Keep the change bounded to the selected-thread handoff path and matching proposal artifacts.
- [x] Reuse the current pending outgoing state, inline session block, composer-adjacent activity bar, and selected-thread SSE ownership datasets instead of adding new runtime behavior.
- [x] Preserve the center conversation shell and bottom-fixed composer through the full submit-to-first-append interval.
- [x] Keep exactly one handoff owner visible at a time: pending outbound user or temporary assistant placeholder, never both.
- [x] Clear the handoff owner immediately on first real assistant SSE append, terminal failure, idle reset, polling fallback, reconnect downgrade, or intentional thread switch.
- [x] Align static checks, browser checks, and proposal artifacts with the selected-thread handoff continuity contract.
