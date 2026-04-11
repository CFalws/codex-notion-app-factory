# Factory Runtime Implementation Plan

## Iteration 119

Converge the footer session strip and detached follow affordance into one bottom-fixed session bar above the composer.

1. Reuse the existing selected-thread footer dock and follow-control models as the only footer state inputs.
2. Keep the session strip visible as the single live-owned footer surface on the healthy selected-thread SSE path.
3. Route detached follow action through the same footer bar by turning the session-strip toggle into the jump-to-latest action when follow state is visible.
4. Keep the old transcript-bottom follow button hidden so no second footer follow surface remains.
5. Extend the focused verifier layer and proposal artifacts so iteration 119 proves the footer bar owns detached follow behavior without reintroducing stale or duplicate live-owned cues.
