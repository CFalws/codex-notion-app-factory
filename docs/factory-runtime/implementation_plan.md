# Factory Runtime Implementation Plan

## Iteration 225

Drive selected-thread live status from one session-scoped append SSE stream.

1. Keep the change bounded to the selected-thread append SSE session-status path and its verifier expectations.
2. Reuse the existing conversation append stream, session-status envelopes, and selected-thread ownership datasets instead of adding a separate transport.
3. Keep the transcript timeline as the healthy live owner while mirrored surfaces stay passive or degraded-only.
4. Keep `ops-jobs` as fallback-only when the selected thread is already SSE-owned.
5. Preserve reconnect, offline, switch, deselection, and restore behavior on the existing fail-open path.
6. Align static checks, browser checks, and proposal artifacts with the selected-thread session-stream contract.
