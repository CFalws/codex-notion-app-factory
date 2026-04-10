# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread append SSE transport, liveRun state, transcript live item, and `autonomySummary` data instead of adding a new authority source.
2. Keep autonomy blocker, path, and verifier state rendered only inside the healthy selected-thread center live item.
3. Suppress the side-panel autonomy detail card while that healthy selected-thread center authority is active, and restore it outside that state.
4. Preserve degraded reconnect, polling fallback, ownership loss, terminal idle, and thread-switch states as explicitly non-owned and non-duplicated.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the single-center-authority contract.
