# Factory Runtime Tasks

- [x] Keep the current selected-thread SSE path, conversation shell, footer composer dock, transcript-tail live block, recent-thread rail, and side-panel behavior unchanged.
- [x] Reuse the existing thread-transition path so the center workspace stays mounted while the target thread snapshot attaches.
- [x] Keep the session summary and composer owner row in SWITCHING or ATTACH for the target thread during transition, and clear stale old-thread live ownership before the new thread attaches.
- [x] Restrict the generic empty-state branch to non-transition fallback only and keep exactly one compact transition placeholder in the timeline until attach completes.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the intentional thread-switch continuity contract.
