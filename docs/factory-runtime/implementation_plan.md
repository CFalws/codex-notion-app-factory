# Factory Runtime Implementation Plan

## Iteration 104

Make healthy selected-thread detached follow state read as part of one unified footer surface without changing transport or introducing a new control surface.

1. Reuse the existing selected-thread live-follow datasets instead of adding a second follow-state source.
2. Move healthy-path detached `NEW` or `PAUSED` follow state into the composer-adjacent session strip and make that strip actionable through the existing footer toggle.
3. Keep the transcript-level jump control mounted but non-visible while the footer owns follow state so the healthy path has no duplicate follow surface.
4. Clear or downgrade footer follow ownership immediately on reconnect, polling fallback, terminal idle, or thread switch.
5. Extend the focused verifier layer and proposal artifacts so the healthy path proves footer-owned follow state and degraded paths prove immediate non-healthy clearing.
