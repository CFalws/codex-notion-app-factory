# Factory Runtime Implementation Plan

## Iteration 89

Tighten the sticky left-rail active-session row so it mirrors only canonical selected-thread state and uses a finite navigation vocabulary.

1. Reuse the existing active-session row surface instead of introducing another rail model.
2. Show `HANDOFF` during pending submit and first-assistant handoff from canonical selected-thread state.
3. Show `LIVE`, `NEW`, or `PAUSED` only while the selected thread remains healthy SSE-owned, with the real phase kept only in metadata and datasets.
4. Clear the row immediately on reconnect downgrade, polling fallback, terminal idle, or thread switch.
5. Reconfirm the focused browser-proof and static verifiers around the bounded finite-state rail contract.
