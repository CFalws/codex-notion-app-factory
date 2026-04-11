# Factory Runtime Implementation Plan

## Iteration 215

Preserve one continuous center session workspace during intentional selected-thread switches.

1. Keep the change bounded to the selected-thread switch path, workspace placeholder behavior, and verifier expectations.
2. Reuse the existing selected-thread session authority, switch monitor, workspace placeholder, and composer dock datasets instead of adding new transport or polling logic.
3. Keep the center conversation shell and bottom-fixed composer mounted during intentional selected-thread switches.
4. Show at most one compact switching placeholder until the new selected-thread snapshot attaches.
5. Clear stale live-owner treatment immediately when the switch starts.
6. Reserve the generic empty workspace for true no-selection idle only.
7. Align static checks, browser checks, and proposal artifacts with the switch-continuity contract.
