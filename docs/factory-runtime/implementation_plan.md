# Factory Runtime Implementation Plan

## Iteration 118

Move transcript-bottom follow ownership onto the selected-thread session model so the off-tail follow control is deterministic and healthy-path only.

1. Reuse `deriveSelectedThreadSessionStatus(...)` and `currentState.liveFollow` as the only inputs to a canonical selected-thread follow-control model in `ops-store.js`.
2. Keep the transcript-bottom control as the only detached follow surface, but wire it to that store-owned model instead of render-local transport checks.
3. Preserve existing switch, reconnect, polling fallback, terminal, and non-selected clearing behavior by letting the store model return hidden state on every degraded path.
4. Keep jump-to-latest and scroll re-engagement as the only ways to clear the control on the healthy path.
5. Extend the focused verifier layer and proposal artifacts so iteration 118 proves the bottom follow control is owned by selected-thread SSE state instead of polling or stale render datasets.
