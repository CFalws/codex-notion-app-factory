# Factory Runtime Implementation Plan

## Iteration 105

Make the composer-adjacent footer strip the single healthy selected-thread live session dock without changing transport or introducing a new schema.

1. Reuse the existing selected-thread session-status, live-autonomy, phase-progression, timeline-milestone, and live-follow datasets instead of adding a new source.
2. Promote the healthy-path footer strip so current phase and milestone progression render beside the fixed composer.
3. Keep the transcript and summary datasets intact, but suppress their visible healthy live-status presentation while the footer dock owns the session.
4. Clear or downgrade footer ownership immediately on reconnect, polling fallback, restore, switch, or terminal idle.
5. Extend the focused verifier layer and proposal artifacts so the healthy path proves footer-owned live session state and degraded paths prove immediate non-healthy clearing.
