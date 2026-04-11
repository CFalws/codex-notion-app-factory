# Factory Runtime Implementation Plan

## Iteration 116

Extend the sticky active-session row so the left rail mirrors the selected thread's switching or attach, handoff, and healthy live follow state without creating a new authority source.

1. Reuse `deriveSelectedThreadSessionStatus(...)`, selected-thread summary datasets, and existing follow-state fields as the only active-session row inputs.
2. Add an explicit switching branch that mirrors the target conversation id and title while marking the row as non-owned transition state.
3. Preserve the existing handoff and healthy live follow mirrors, including unseen-count projection for `NEW`.
4. Keep the active-session row hidden for reconnect downgrade, polling fallback, terminal idle, and non-selected contexts.
5. Extend the focused verifier layer and proposal artifacts so iteration 116 proves the rail mirrors selected-thread switching instead of clearing to generic idle.
