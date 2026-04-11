# Factory Runtime Implementation Plan

## Iteration 212

Activate the inline selected-thread session block in the center transcript.

1. Keep the change bounded to the prepared inline session-block render path and verifier expectations.
2. Reuse the existing selected-thread session authority, handoff, autonomy, and phase datasets instead of adding new transport or polling logic.
3. Render exactly one compact inline session block for healthy selected-thread SSE ownership or pending assistant handoff.
4. Suppress the older healthy live-activity row while the inline block is present so the transcript has one owner surface instead of two.
5. Keep degraded reconnect or polling fallback, switch, restore, deselection, and terminal paths on their existing clear or fail-open behavior.
6. Align static checks, browser checks, and proposal artifacts with the inline session-block contract.
