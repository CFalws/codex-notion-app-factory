# Factory Runtime Implementation Plan

## Iteration 233

Replace switch and restore placeholder ownership with one inline timeline transition item.

1. Keep the change bounded to the existing selected-thread switch and restore path, current render boundaries, and matching proposal artifacts.
2. Reuse the existing inline `timeline-transition` item and mounted composer shell instead of introducing a second transition panel or transport.
3. Keep the center conversation timeline in conversation mode during switch or restore.
4. Clear old-thread live ownership immediately and allow exactly one inline transition item to represent attach or restore state.
5. Keep the composer target row and session strip synchronized to the same transition state while degraded fallback still clears healthy ownership immediately.
6. Align static checks, browser checks, and proposal artifacts with the inline transition continuity contract.
