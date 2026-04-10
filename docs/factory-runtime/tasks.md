# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer, and non-selected snapshot rows unchanged.
- [x] Reuse the existing `threadTransition` state and selected-thread ownership path for switch continuity.
- [x] Clear old-thread live ownership immediately when a switch starts.
- [x] Render exactly one compact `SWITCHING` placeholder until the new snapshot attaches.
- [x] Keep send blocked only while selected-thread attach is unresolved.
- [x] Align focused verification and iteration artifacts with the continuous thread-switch shell contract.
