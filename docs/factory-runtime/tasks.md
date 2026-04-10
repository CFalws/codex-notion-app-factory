# Factory Runtime Tasks

- [x] Keep the existing selected-thread inline live block, degraded indicator, and bottom-fixed composer unchanged.
- [x] Add a compact transcript projection for selected-thread session milestone events using the append-event fields that already drive live phase state.
- [x] Replace generic event cards with the new session-event rows for proposal, review, verify, auto-apply, ready, applied, failure, and terminal milestones.
- [x] Leave degraded reconnect or polling fallback behavior unchanged so the existing degraded indicator remains the only current-session surface while ownership is lost.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the session-event timeline projection contract.
