# Factory Runtime Tasks

## Iteration 225

- [x] Keep the change bounded to the selected-thread append SSE session-status path and its existing ownership surfaces.
- [x] Reuse the current append stream, session-status envelopes, and selected-thread ownership datasets instead of adding a second transport.
- [x] Keep the transcript timeline as the healthy live owner while mirrored surfaces stay passive or degraded-only.
- [x] Keep `ops-jobs` as fallback-only when the selected thread is already SSE-owned.
- [x] Preserve reconnect, offline, switch, deselection, and restore behavior on the existing fail-open path.
- [x] Align static checks, browser checks, and proposal artifacts with the selected-thread session-stream contract.
