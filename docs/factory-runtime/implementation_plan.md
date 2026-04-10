# Factory Runtime Implementation Plan

1. Keep the current selected-thread SSE path, conversation shell, footer composer dock, transcript-tail live block, recent-thread rail, and side-panel behavior unchanged.
2. Reuse the existing thread-transition path so the center workspace stays mounted while the target thread snapshot attaches.
3. Keep the session summary and composer owner row in SWITCHING or ATTACH for the target thread during transition, and clear stale old-thread live ownership before the new thread attaches.
4. Restrict the generic empty-state branch to non-transition fallback only and keep exactly one compact transition placeholder in the timeline until attach completes.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the intentional thread-switch continuity contract.
