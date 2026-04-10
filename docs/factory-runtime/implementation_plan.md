# Factory Runtime Implementation Plan

1. Keep the existing selected-thread switch render path, thread placeholder, and bottom-fixed composer shell unchanged unless a real gap appears.
2. Prove that an intentional thread switch keeps the center workspace mounted and never falls through to the generic empty-state branch.
3. Prove that old selected-thread live ownership clears immediately on switch and does not survive beside the loading placeholder.
4. Keep degraded reconnect and polling fallback behavior separate from switch continuity so the verifier does not mistake a fallback path for healthy session continuity.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the selected-thread switch continuity contract.
