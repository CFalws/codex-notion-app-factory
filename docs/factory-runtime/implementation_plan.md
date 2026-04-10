# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, selected-row live-owner contract, dock behavior, transcript-tail live item, and non-selected snapshot rows unchanged.
2. Introduce one bounded `threadTransition` state for intentional thread switches so the center pane can render a compact in-place handoff placeholder instead of a blank reset.
3. Clear prior-thread live ownership immediately when the switch starts, keep the composer dock and thread surface anchored, and attach the new snapshot plus selected-thread SSE path as soon as the fetch completes.
4. Preserve phone and desktop continuity by keeping non-selected rows snapshot-only and avoiding any second switch-status panel in the rail or header.
5. Extend the focused verifier and docs so future sessions can prove thread-switch continuity, transition placeholder rendering, and immediate stale-live clearing on thread change or degraded fallback.
