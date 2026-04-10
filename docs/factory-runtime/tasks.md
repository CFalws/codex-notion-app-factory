# Factory Runtime Tasks

- [x] Reuse the existing selected-thread thread-transition path instead of introducing a new switch transport or state machine.
- [x] Verify the center pane keeps the dedicated transition placeholder and never falls back to `.timeline-empty` during intentional thread switch.
- [x] Verify stale header live ownership clears immediately on switch.
- [x] Verify the composer remains bottom-fixed with explicit `SWITCHING` owner state and target copy during attach.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the switch-continuity contract.
