# Factory Runtime Tasks

- [x] Extend the selected-thread `session.bootstrap` event so it can mark both healthy attach and healthy cursor-based resume without changing `conversation.append`.
- [x] Reopen the selected-thread SSE stream from the last append cursor on reconnect instead of degrading immediately to polling on the healthy path.
- [x] Expose resume mode and resume cursor in machine-readable session-strip and thread-scroller datasets next to attach mode and bootstrap version.
- [x] Tighten browser verification so healthy reconnect requires SSE resume with no conversation snapshot fetch, no job polling takeover, and no duplicate append replay.
- [x] Align the focused verifier and iteration artifacts with the selected-thread bootstrap-resume contract.
