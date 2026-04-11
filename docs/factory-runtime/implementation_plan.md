# Factory Runtime Implementation Plan

1. Reuse the existing thread-transition placeholder path and selected-thread continuity shell instead of introducing a new switching surface.
2. Make switching explicitly clear phase datasets to non-authoritative `UNKNOWN` with `thread-transition` provenance while the target snapshot and SSE attach are pending.
3. Keep the session strip and composer dock mounted, keep the placeholder singular, and leave old-thread live ownership cleared across the switch path.
4. Tighten browser verification so the switch placeholder, composer target state, and cleared ownership all remain true without empty-state fallback or hidden attach-time job polling.
5. Align focused verifier and iteration artifacts around the bounded switch continuity contract.
