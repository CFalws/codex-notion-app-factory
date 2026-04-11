# Factory Runtime Implementation Plan

## Iteration 210

Expose the left-rail sticky active-session row during the healthy selected-thread path.

1. Keep the change bounded to the sticky active-session row model, rail render behavior, and verifier expectations.
2. Reuse the existing selected-thread session authority, phase, and follow or unseen datasets instead of adding new transport or polling logic.
3. Keep the rail row chip-first and explicitly non-authoritative while mirroring the selected-thread owner, phase, and follow state.
4. Show exactly one sticky row for healthy live, handoff, switching, new, or paused selected-thread states.
5. Clear the row immediately on reconnect downgrade, polling fallback, switch, deselection, idle, or terminal resolution.
6. Keep the selected-card live-owner marker suppressed whenever the sticky row is present so no second rail row appears.
7. Align static checks, browser checks, and proposal artifacts with the rail-mirroring contract.
