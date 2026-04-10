# Factory Runtime Tasks

- [x] Keep the current selected-thread SSE path, conversation shell, footer composer dock, sticky active-session row, left navigation rail, and side-panel behavior unchanged.
- [x] Add a compact recent-thread quick-switch rail beneath the conversation header using the existing conversation list payload and keep it bounded to a small set of recent threads.
- [x] Reuse the existing selected-thread ownership, handoff, follow, and snapshot label helpers so the center-pane rail mirrors the same selected and live-state cues without adding a second source of truth.
- [x] Route quick-switch clicks through the current `fetchConversation` and `threadTransition` path so transcript and composer continuity stay intact and stale live ownership still clears immediately.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the center-pane recent-thread rail contract.
