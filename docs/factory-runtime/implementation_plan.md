# Factory Runtime Implementation Plan

## Iteration 144

Expose one compact selected-thread header ownership indicator without weakening the center-timeline authority contract.

1. Reuse existing selected-thread session-status and timeline-authority helpers to derive one compact header ownership indicator for healthy, degraded, and restore states.
2. Keep that indicator secondary by collapsing the summary row into an indicator-only row whenever timeline authority or restore visibility is active.
3. Hide the indicator immediately on switch and terminal idle.
4. Publish machine-readable datasets for indicator visibility, presentation, and provenance so browser verification can prove it comes from the intended selected-thread session path.
5. Preserve transport, polling suppression, composer, and cross-thread behavior unchanged.
6. Extend focused static and deployed verification plus proposal artifacts so iteration 144 proves healthy and degraded ownership visibility without reintroducing duplicate authority prose.
