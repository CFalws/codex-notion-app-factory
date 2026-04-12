# Factory Runtime Tasks

## Iteration 233

- [x] Keep the change bounded to the existing selected-thread switch and restore path, current render boundaries, and matching proposal artifacts.
- [x] Reuse the existing inline `timeline-transition` item and mounted composer shell instead of adding new runtime transport or a second transition panel.
- [x] Keep the center conversation timeline in conversation mode during switch or restore.
- [x] Clear old-thread live ownership immediately and allow exactly one inline transition item to represent attach or restore state.
- [x] Keep the composer target row and session strip synchronized to the same transition state while degraded fallback still clears healthy ownership immediately.
- [x] Align static checks, browser checks, and proposal artifacts with the inline transition continuity contract.
