# Factory Runtime Tasks

- [x] Add one additive `autonomy_summary` freshness envelope to conversation snapshot and `session.bootstrap`.
- [x] Carry server-authored `source`, `generated_at`, `freshness_state`, and `fallback_allowed` semantics through the selected-thread client hydration path.
- [x] Use one canonical `stale-or-missing` marker for missing or degraded autonomy freshness cases.
- [x] Keep existing `/api/apps/{app_id}/goals` fallback behavior unchanged in this iteration.
- [x] Align focused verifier, runtime contract checks, and iteration artifacts with the bounded freshness-envelope contract.
