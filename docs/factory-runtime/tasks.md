# Factory Runtime Tasks

- [x] Add one additive `session_phase` payload to selected-thread `session.bootstrap` and `conversation.append` envelopes.
- [x] Limit authoritative phase values to `PROPOSAL`, `REVIEW`, `VERIFY`, `READY`, `APPLIED`, and `FAILED`.
- [x] Move selected-thread live surfaces onto that single phase model and render `LIVE` or `UNKNOWN` when the payload is non-authoritative.
- [x] Expose phase value, authoritative bit, and provenance consistently in the session strip, thread scroller, and inline live block.
- [x] Align the focused verifier and iteration artifacts with the authoritative selected-thread phase contract.
