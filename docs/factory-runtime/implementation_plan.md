# Factory Runtime Implementation Plan

## Iteration 143

Make the center-timeline live-session item the primary selected-thread authority and demote duplicate center-lane status prose.

1. Add one render-layer selected-thread timeline authority helper derived from the existing selected-thread session surface and inline-session helpers.
2. Use that helper to decide when the header summary row should hide instead of competing with the timeline item.
3. Use the same helper to demote the autonomy detail and execution status cards into non-authoritative center-lane surfaces while the timeline item is active.
4. Publish machine-readable datasets on those demoted surfaces so verification can prove healthy and degraded authority paths explicitly.
5. Preserve existing transport, polling suppression, restore, handoff, switch, and composer behavior.
6. Extend focused static and deployed verification so iteration 143 proves the timeline item owns selected-thread authority and stale duplicate prose does not survive degraded or cleared paths.
