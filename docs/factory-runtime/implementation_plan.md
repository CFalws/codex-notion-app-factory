# Factory Runtime Implementation Plan

## Iteration 231

Collapse selected-thread live execution into one canonical transcript-tail session block.

1. Keep the change bounded to the existing selected-thread append SSE ownership path, current render boundaries, and matching proposal artifacts.
2. Reuse the inline session block, handoff state, selected-thread session-status helper, and existing mirror datasets instead of adding new transport or backend seams.
3. Keep the transcript-tail session block as the only healthy live-owned surface for handoff, phase, proposal, review, verify, ready, and applied progression.
4. Keep the bottom-fixed composer mounted and chat-first without letting it become a second status surface.
5. Demote header and rail mirrors to compact passive cues while preserving explicit degraded fallback that clears canonical live ownership immediately.
6. Align static checks, browser checks, and proposal artifacts with the unified transcript-tail session-block contract.
