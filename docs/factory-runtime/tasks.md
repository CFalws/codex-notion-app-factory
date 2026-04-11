# Factory Runtime Tasks

- [x] Add one shared helper that recognizes when the selected thread still owns the active session through SSE.
- [x] Suppress routine `/api/jobs/{id}` polling across healthy attach, resume, and send flows while that selected-thread session remains SSE-owned.
- [x] Reopen job polling only for explicit degraded conditions such as reconnect fallback, ownership loss, stale-or-missing freshness, or off-thread tracking.
- [x] Keep live proposal, review, verify, ready, and applied visibility sourced from the existing selected-thread session strip and timeline.
- [x] Align focused browser-proof verifiers and iteration artifacts with the bounded active-run polling-suppression contract.
