# Factory Runtime Implementation Plan

1. Add a minimal versioned `session.bootstrap` event to the existing selected-thread append SSE stream, keeping `conversation.append` unchanged.
2. Include only selected-thread bootstrap inputs needed for hydration: conversation snapshot, append cursor, active job or phase summary, composer ownership inputs, and explicit attach mode.
3. Change selected-thread attach to prefer SSE bootstrap before falling back to a conversation snapshot fetch, while exposing attach mode and bootstrap version in machine-readable datasets.
4. Tighten browser verification so healthy attach proves no separate conversation snapshot fetch happened after click, while degraded fallback remains explicit and observable.
5. Align focused verifier and iteration artifacts with the versioned bootstrap and attach-mode contract.
