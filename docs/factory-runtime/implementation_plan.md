# Factory Runtime Implementation Plan

## Iteration 101

Make healthy selected-thread SSE session state the only authoritative autonomy summary source without changing transport or the visible session layout.

1. Reuse the existing selected-thread session, restore, live-autonomy, and phase helpers rather than adding a new authority model.
2. Mark `session.bootstrap` autonomy data as fresh and fallback-disallowed when the bootstrap payload already carries the selected-thread autonomy summary.
3. Prefer bootstrap autonomy over snapshot autonomy during `fetchConversation(...)` so the selected-thread session path becomes authoritative as soon as bootstrap succeeds.
4. Gate `/api/goals` refresh behind explicit degraded transport, missing selected-thread authority, or stale-or-missing autonomy data instead of always refreshing after conversation fetch.
5. Extend the focused verifier layer and proposal artifacts so the healthy path proves session-owned autonomy state and the negative case proves the absence of polling-owned success.
