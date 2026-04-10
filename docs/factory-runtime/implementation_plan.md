# Factory Runtime Implementation Plan

1. Confirm the current selected-thread inline session block already owns handoff and degraded rendering while healthy live still uses the transcript-tail activity.
2. Extend the inline block to render healthy selected-thread live progress from the same `liveRun` and selected-thread SSE authority path.
3. Suppress the separate transcript-tail live activity whenever the unified inline block is active.
4. Preserve degraded reconnect, polling fallback, ownership loss, terminal idle, and thread-switch states as explicitly non-owned or cleared.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the single-inline-session-block contract.
