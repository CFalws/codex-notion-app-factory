# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, dock behavior, selected-row live-owner contract, and non-selected snapshot rows unchanged.
- [x] Add one bounded `threadTransition` state so intentional thread switches render a compact in-place handoff instead of a blank reset.
- [x] Keep the center conversation surface and composer dock persistent while the target thread snapshot is loading.
- [x] Clear prior-thread live ownership immediately on thread switch without leaving stale live markers in the rail or center pane.
- [x] Extend focused verification so future sessions can prove thread-switch continuity and transition placeholder behavior remain strict.
