# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread `liveRun` derivation as the only authority for healthy phase labels in the header and composer-adjacent strip.
2. Add explicit phase detail copy to the header badge state so healthy selected-thread progression is readable without inspecting deeper surfaces.
3. Add a live phase chip and phase-specific detail copy to the composer-adjacent strip while keeping switching and degraded transport states unchanged.
4. Preserve degraded reconnect, polling fallback, ownership loss, and thread-switch presentation as explicitly non-owned states.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the explicit-phase presentation contract.
