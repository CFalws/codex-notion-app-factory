# Factory Runtime Implementation Plan

## Iteration 228

Preserve one continuous workspace during intentional selected-thread switches.

1. Keep the change bounded to the selected-thread switch path and matching proposal artifacts.
2. Reuse the existing thread-transition placeholder, mounted composer shell, and ownership-clearing datasets instead of adding new runtime behavior.
3. Preserve the center conversation shell and bottom-fixed composer through intentional switches.
4. Clear prior thread live, phase, proposal, and follow ownership immediately at switch start.
5. Keep exactly one compact transition placeholder visible until the target snapshot attaches, with no generic empty-state flash.
6. Align static checks, browser checks, and proposal artifacts with the selected-thread switch continuity contract.
