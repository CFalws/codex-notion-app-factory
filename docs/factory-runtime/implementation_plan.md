# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, session strip ownership, bottom follow control, footer composer, and non-selected snapshot rows unchanged.
2. Add one compact composer target row that names the currently selected thread and shows `READY`, `SWITCHING`, or `HANDOFF`.
3. Reuse the existing selected-thread owner state and `threadTransition` contract instead of introducing a second ownership source.
4. Disable send only while selected-thread attach is unresolved, and prevent stale old-thread target state from surviving a switch.
5. Keep the focused verifier and durable docs aligned with the composer target ownership contract.
