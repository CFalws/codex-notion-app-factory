# Factory Runtime Implementation Plan

1. Confirm the current composer-adjacent footer still splits live status between `session-strip` and `composer-owner-row`.
2. Promote the `session-strip` into the single chip-first composer-adjacent activity bar by reusing owner, transport, phase, and proposal helpers there.
3. Hide the separate owner row whenever that merged activity bar is active, while preserving its data wiring for send-button ownership state.
4. Preserve degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states as explicitly non-owned or cleared.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the single composer-adjacent activity-bar contract.
