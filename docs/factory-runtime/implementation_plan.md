# Factory Runtime Implementation Plan

## Iteration 236

Remove the center-pane recent-thread rail and keep thread switching owned by the left rail or mobile nav sheet.

1. Keep the change bounded to the center-pane recent-thread rail DOM, CSS, render wiring, and matching proposal artifacts.
2. Remove center-pane recent-thread navigation instead of introducing a replacement control in the main workspace.
3. Preserve left-rail conversation cards and the mobile nav sheet as the only selected-thread switch owners.
4. Keep switch and restore continuity in conversation mode through the existing inline `timeline-transition` item and mounted composer shell.
5. Preserve degraded fallback clearing, footer docking, and canonical live-ownership behavior.
6. Align static checks, browser checks, and proposal artifacts with the transcript-only center-pane contract.
