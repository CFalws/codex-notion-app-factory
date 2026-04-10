# Factory Runtime Implementation Plan

1. Add one additive `session_phase` payload to selected-thread `session.bootstrap` and `conversation.append` envelopes, sourced only from unambiguous SSE-owned signals.
2. Store that phase model in selected-thread append-stream state and have the existing live surfaces read it instead of deriving proposal, review, verify, ready, or applied from latest-event heuristics.
3. Render only the bounded authoritative subset as real phases, and render `LIVE` or `UNKNOWN` whenever the phase payload is missing, stale, or non-authoritative.
4. Expose phase value, authoritative bit, and provenance consistently across the session strip, thread scroller, and inline live block.
5. Tighten focused verification and iteration artifacts around the bounded authoritative phase contract.
