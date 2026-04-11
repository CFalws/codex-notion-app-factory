# Factory Runtime Tasks

## Iteration 101

- [x] Mark healthy selected-thread `session.bootstrap` autonomy data as fresh and fallback-disallowed when bootstrap already carries autonomy state.
- [x] Prefer bootstrap autonomy over snapshot autonomy during `fetchConversation(...)` so healthy selected-thread session bootstrap owns autonomy state immediately.
- [x] Allow `/api/goals` refresh only when selected-thread session authority is degraded, missing, or stale-or-missing instead of always refreshing after conversation fetch.
- [x] Keep the existing render surface unchanged while exposing enough provenance for verification to prove healthy session-owned autonomy success.
- [x] Align focused verifiers and proposal artifacts with the iteration-101 autonomy-authority contract.
