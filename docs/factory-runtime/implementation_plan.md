# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread append-stream state to define an authoritative startup boundary for `connecting` and `live` SSE ownership.
2. Remove the eager `pollCurrentState()` submit follow-up on the healthy selected-thread path so local pending turns, handoff, and the transcript-tail live item carry startup instead.
3. Keep polling available only for degraded paths: unavailable EventSource, reconnect, ownership loss, or downgraded append-stream transport.
4. Ensure the job controller respects the same authoritative boundary so it does not restart polling while selected-thread SSE is already connecting or live.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the degraded-only polling boundary contract.
