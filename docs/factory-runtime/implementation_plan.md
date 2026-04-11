# Factory Runtime Implementation Plan

## Iteration 164

Mirror the selected-thread live session onto the selected conversation row.

1. Keep the change read-only over the existing selected-thread canonical session and follow state seam.
2. Add one store-owned selected-row live marker model with finite labels `HANDOFF`, `LIVE`, `NEW`, and `PAUSED`.
3. Render exactly one selected-card live marker row in the left rail and keep non-selected cards snapshot-only.
4. Clear that marker immediately on reconnect downgrade, polling fallback, terminal completion, deselection, or thread switch.
5. Do not add a recent-thread rail mirror or any new authority source in this iteration.
6. Align focused verification and proposal artifacts with the iteration-164 selected-row live-marker contract.
