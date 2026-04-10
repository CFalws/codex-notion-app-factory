# Factory Runtime Implementation Plan

1. Keep the existing selected-thread SSE ownership source, bottom follow control location, and bottom-fixed composer layout unchanged.
2. Continue using `syncJumpToLatest(...)` as the single render owner for detached-tail visibility and machine-readable follow-state datasets.
3. Change the follow control contract so healthy detached selected-thread sessions render `PAUSED` even before backlog exists, then upgrade in place to `NEW` when unseen append count becomes positive.
4. Preserve immediate clear behavior on jump-to-latest, reconnect downgrade, polling fallback, thread switch, terminal idle, or ownership loss.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the explicit detached-tail indicator contract.
