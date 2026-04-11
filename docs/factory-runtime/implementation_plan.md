# Factory Runtime Implementation Plan

## Iteration 106

Make the healthy selected-thread transcript read as one compact live session timeline without changing transport or adding a new event schema.

1. Reuse the existing selected-thread footer-dock, live-activity, and timeline-event helpers instead of introducing a new transcript model.
2. Suppress healthy selected-thread SSE authority event cards when the same run is already represented by the live session surfaces.
3. Keep degraded, restore, reconnect, switching, failure, ready, and applied evidence explicit when the session is no longer healthy live-owned.
4. Leave the footer-dock and existing machine-readable datasets intact so the rail and verifier layers keep their current contract.
5. Extend the focused verifier layer and proposal artifacts so the healthy path proves transcript collapse and degraded paths prove explicit fallback evidence.
