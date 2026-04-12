# Factory Runtime Implementation Plan

## Iteration 232

Extend selected-thread `session_status` into complete live autonomy authority.

1. Keep the change bounded to the existing selected-thread append SSE ownership path, the canonical runtime `conversation_session_status` helper, current selected-thread projections, and matching proposal artifacts.
2. Add goal identity and iteration metadata directly to `session_status` instead of introducing new transport or a second authority path.
3. Reuse the existing selected-thread session-status normalization and transcript-tail session block instead of widening render ownership.
4. Keep the transcript-tail session block as the only healthy live-owned surface while goals polling remains fallback-only for degraded or non-authoritative states.
5. Preserve reconnect and polling downgrade as explicit degraded fallback that clears canonical live ownership immediately.
6. Align static checks, browser checks, and proposal artifacts with the richer streamed autonomy-identity contract.
