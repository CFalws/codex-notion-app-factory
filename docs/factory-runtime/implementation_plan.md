# Factory Runtime Implementation Plan

## Iteration 103

Make healthy selected-thread autonomy progression read as one canonical timeline surface without changing transport or introducing a new status panel.

1. Reuse the existing selected-thread live-autonomy and phase-progression helpers instead of adding a second autonomy view model.
2. Derive a store-owned selected-thread timeline milestone model for proposal, review, verify, ready, and applied progression on the healthy SSE-owned path.
3. Render that milestone model only inside the transcript live activity item so the center conversation becomes the primary progression surface.
4. Keep degraded, reconnect, restore, and polling provenance explicit, and stop hiding the sidecar autonomy surface when the selected-thread session is not healthy-owned.
5. Extend the focused verifier layer and proposal artifacts so the healthy path proves timeline-owned progression and the degraded path proves visible non-healthy provenance.
