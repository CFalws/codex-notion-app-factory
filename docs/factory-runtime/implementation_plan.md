# Factory Runtime Implementation Plan

1. Extend the existing selected-thread `session.bootstrap` event additively so it distinguishes initial attach from cursor-based resume without changing `conversation.append`.
2. Change selected-thread reconnect to reopen the existing SSE route from the last append cursor, keep the conversation shell and composer mounted, and avoid immediate polling takeover on healthy resume.
3. Expose resume mode and resume cursor in the existing machine-readable session-strip and thread-scroller datasets alongside attach mode and bootstrap version.
4. Tighten browser verification so healthy reconnect proves no separate conversation snapshot fetch, no job polling takeover, and no duplicate append replay during resume.
5. Align focused verifier and iteration artifacts with the versioned bootstrap-resume contract and explicit degraded fallback.
