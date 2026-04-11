# Factory Runtime Implementation Plan

## Iteration 211

Preserve one continuous center session workspace during intentional selected-thread switches.

1. Keep the change bounded to the selected-thread switch path, workspace placeholder behavior, and verifier expectations.
2. Reuse the existing thread-transition and selected-thread session datasets instead of adding new transport or polling logic.
3. Keep the center conversation shell and bottom-fixed composer mounted while a selected-thread switch is in flight.
4. Limit the switch path to one compact transition placeholder until the new snapshot attaches.
5. Clear stale old-thread live ownership immediately at switch start.
6. Reserve the generic empty workspace for true no-selection idle only.
7. Align static checks, browser checks, and proposal artifacts with the switch-continuity contract.
