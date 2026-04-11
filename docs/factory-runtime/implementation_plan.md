# Factory Runtime Implementation Plan

## Iteration 161

Preserve selected-thread session continuity during intentional thread switches.

1. Keep the center conversation shell and bottom composer mounted while `threadTransition.active` targets a new selected thread.
2. Clear old selected-thread live strip ownership explicitly during the switch window and expose that cleared state through machine-readable datasets.
3. Keep exactly one compact transition placeholder until the new selected-thread snapshot attaches, without letting `.timeline-empty` win during that switch path.
4. Preserve reconnect, polling fallback, deselection, terminal completion, and non-selected thread fail-closed behavior.
5. Extend focused verification so switch, degraded, and cleared paths prove the old thread cannot remain session-owned and non-selected threads cannot become primary owners.
6. Align proposal artifacts with the iteration-161 selected-thread switch continuity contract.
