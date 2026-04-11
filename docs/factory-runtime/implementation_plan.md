# Factory Runtime Implementation Plan

## Iteration 109

Keep the selected-thread workspace shell mounted during intentional thread switches without changing transport or adding a new polling path.

1. Reuse the existing selected-thread session-status and thread-transition helpers instead of creating a separate switch renderer contract.
2. Make the null-conversation branch resolve through one explicit workspace placeholder model with `switching`, `restore`, and `empty` states.
3. Keep the center pane limited to one compact `SWITCHING` placeholder while the new thread attaches.
4. Mirror the same switch state into the existing composer target row or merged session strip without leaving stale live ownership behind.
5. Extend the focused verifier layer and proposal artifacts so the intended switch path proves no generic empty-state flash and no stale live-owned treatment.
