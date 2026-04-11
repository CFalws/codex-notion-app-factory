# Factory Runtime Tasks

- [x] Reuse the server-authored `autonomy_summary` freshness envelope as the first selected-thread autonomy source on snapshot and `session.bootstrap`.
- [x] Suppress `/api/apps/{app_id}/goals` polling on the healthy selected-thread SSE-owned path when the server contract says `fallback_allowed=false`.
- [x] Reopen goals polling only for canonical `stale-or-missing`, reconnect downgrade, or selected-thread ownership loss cases.
- [x] Keep append-driven autonomy updates carrying the server-authored freshness fields forward in state.
- [x] Align focused browser-proof verifiers and iteration artifacts with the bounded polling-suppression contract.
