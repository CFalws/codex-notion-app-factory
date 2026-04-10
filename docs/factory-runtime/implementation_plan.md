# Factory Runtime Implementation Plan

1. Confirm the current selected-thread switch path already keeps the conversation shell mounted and routes through the dedicated transition placeholder instead of a generic empty reset.
2. Confirm old-thread selected-session ownership is cleared during switch, including inline healthy-block and follow ownership cues.
3. Tighten the deployed workspace gate so browser verification explicitly rejects stale healthy inline-block or follow ownership during an intentional switch.
4. Preserve degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states as explicitly non-owned or cleared.
5. Align the focused verifier and iteration artifacts with the tightened switch-continuity proof contract.
