# Factory Runtime Tasks

- [x] Add a versioned additive `session.bootstrap` event to the selected-thread append SSE route without changing `conversation.append`.
- [x] Hydrate healthy selected-thread attach from SSE bootstrap before falling back to a conversation snapshot fetch.
- [x] Expose attach mode and bootstrap version in machine-readable session-strip and thread-scroller datasets.
- [x] Tighten browser verification so healthy attach requires bootstrap plus no extra conversation snapshot fetch, while degraded fallback stays explicit.
- [x] Align the focused verifier and iteration artifacts with the versioned bootstrap attach contract.
