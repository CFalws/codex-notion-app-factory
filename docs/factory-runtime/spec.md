# Factory Runtime Spec

## Iteration

- current iteration: `154`
- bounded focus: `demote the secondary panel into a compact selected-thread detail drawer`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The main transcript now behaves like one selected-thread session surface, but the secondary panel still reads like a parallel status dashboard with prose summary and a primary-looking execution headline. That keeps the workspace short of a single live session feel.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the transcript and bottom composer to stay primary while the secondary panel acts only as an optional drill-down drawer.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread secondary panel render path plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, transcript ownership rules, footer ownership rules, or rail mirroring.
- Reuse the existing selected-thread session, autonomy, phase, verifier, blocker, and timeline milestone models.
- Keep the transcript and composer as the primary live session surfaces and the secondary panel detail-only.
- Render compact selected-thread scope, path, phase, verifier, and blocker facts at the top of the secondary panel.
- Keep deeper autonomy and execution detail in the panel without a competing primary execution strip.
- Clear stale selected-thread ownership immediately on reconnect downgrade, polling fallback, switch, terminal idle, deselection, or thread loss of authority.
- Never make a non-selected thread appear live-owned.

## Deliverable

Demote the selected-thread secondary panel into an optional compact detail drawer so it mirrors selected-thread facts and drill-down detail from the existing session contract without competing with the transcript-native session surface.
