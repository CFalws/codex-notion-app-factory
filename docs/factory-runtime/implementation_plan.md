# Factory Runtime Implementation Plan

1. Keep the existing selected-thread inline live block, degraded indicator, and bottom-fixed composer unchanged.
2. Add a compact transcript projection for selected-thread session milestone events using the append-event fields that already drive live phase state.
3. Replace generic event cards with the new session-event rows for proposal, review, verify, auto-apply, ready, applied, failure, and terminal milestones.
4. Leave degraded reconnect or polling fallback behavior unchanged so the existing degraded indicator remains the only current-session surface while ownership is lost.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the session-event timeline projection contract.
