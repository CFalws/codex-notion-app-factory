# Factory Runtime Tasks

- [x] Keep the current selected-thread SSE path, conversation shell, footer composer dock, sticky active-session row, and side-panel behavior unchanged.
- [x] Tighten the intentional thread-switch path so the center pane keeps its mounted shell and shows the compact selected-thread transition placeholder instead of falling through to the generic empty-state reset.
- [x] Reuse the existing `threadTransition` and selected-thread ownership helpers so the old thread's live chips and rails clear immediately without introducing multi-thread live mirroring.
- [x] Clear the transition placeholder as soon as the target snapshot attaches, while degraded paths, terminal resolution, and non-selected threads continue to avoid live-owned treatment.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the selected-thread transition continuity contract.
