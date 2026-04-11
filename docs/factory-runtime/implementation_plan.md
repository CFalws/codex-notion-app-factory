# Factory Runtime Implementation Plan

## Iteration 146

Preserve selected-thread workspace continuity across intentional thread switches.

1. Reuse the current selected-thread workspace placeholder path so intentional switches render one compact `SWITCHING` placeholder instead of dropping into the generic empty-state.
2. Keep the center conversation shell and bottom composer dock mounted throughout the switch window.
3. Clear the previous thread's live-owned treatment immediately when the switch begins, without leaving stale ownership cues behind.
4. Mark the switching placeholder with an explicit compact dataset so browser verification can distinguish it from true idle and from duplicate placeholders.
5. Extend the deployed verifier to observe the full switch window and fail if the empty-state flashes, the composer dock hides, the switching placeholder duplicates, or the placeholder clears before the new selected-thread snapshot attaches.
6. Align focused static verification and proposal artifacts with the iteration-146 switch-continuity contract.
