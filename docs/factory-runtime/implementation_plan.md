# Factory Runtime Implementation Plan

1. Add one backend helper that builds a minimal autonomy summary plus freshness envelope from the latest relevant app goal.
2. Expose that additive `autonomy_summary` payload on both `/api/conversations/{id}` and `session.bootstrap`, with explicit `source`, `generated_at`, `freshness_state`, and `fallback_allowed`.
3. Hydrate selected-thread autonomy state from that server payload in `ops-conversations.js` before the existing goals polling fallback runs.
4. Preserve append-driven autonomy updates and goals polling fallback behavior, but carry the server-authored freshness fields forward in state.
5. Align focused verifier, runtime contract checks, and iteration artifacts around the bounded freshness-envelope contract.
