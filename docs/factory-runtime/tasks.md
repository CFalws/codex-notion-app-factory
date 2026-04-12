# Factory Runtime Tasks

## Iteration 232

- [x] Keep the change bounded to the existing selected-thread append SSE ownership path, the canonical runtime `conversation_session_status` helper, current selected-thread projections, and matching proposal artifacts.
- [x] Add goal identity and iteration metadata directly to `session_status` instead of introducing new runtime transport.
- [x] Reuse the existing selected-thread session-status normalization and transcript-tail session block instead of widening render ownership.
- [x] Keep the transcript-tail session block as the only healthy live-owned surface while goals polling remains fallback-only for degraded or non-authoritative states.
- [x] Preserve reconnect and polling downgrade as explicit degraded fallback that clears canonical live ownership immediately.
- [x] Align static checks, browser checks, and proposal artifacts with the richer streamed autonomy-identity contract.
