# Factory Runtime Implementation Plan

## Iteration 214

Make the sticky left-rail active-session row a strict mirror of selected-thread session authority.

1. Keep the change bounded to the active-session row mirror contract and verifier expectations.
2. Reuse the existing selected-thread session authority, inline transcript block, and composer dock datasets instead of adding new transport or polling logic.
3. Keep exactly one compact sticky rail row for healthy selected-thread SSE and intentional switch states.
4. Keep the rail row non-authoritative and chip-first, mirroring conversation id, phase, and follow state from the same selected-thread source of truth.
5. Keep the selected-card live-owner marker suppressed whenever the sticky rail row is present.
6. Clear or downgrade the rail row immediately on reconnect, polling fallback, deselection, or terminal completion.
7. Align static checks, browser checks, and proposal artifacts with the strict rail-mirroring contract.
