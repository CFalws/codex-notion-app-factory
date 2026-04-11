# Factory Runtime Spec

## Iteration

- current iteration: `171`
- bounded focus: `keep switch and attach continuity inside one compact session-timeline transition item`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center workspace still breaks continuity at switch and attach boundaries. Operators can keep the live session surface during healthy progression, but switch and restore still split across placeholder modes that feel less like one continuous session timeline.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting selected-thread switch or attach boundaries to stay inside one continuous conversation shell with a compact transition item instead of dropping toward a generic empty workspace feel.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to selected-thread switch and attach continuity in the center conversation workspace.
- Reuse the existing selected-thread session-status, switch-state, and transport datasets; do not add a new authority source.
- Keep switch and attach inside one compact transcript-bound transition item while the composer dock stays fixed.
- Fail closed to the generic empty state only when there is truly no selected conversation.

## Deliverable

Render exactly one compact transcript-bound transition item during intentional selected-thread switch or attach, keep the conversation shell and composer dock visible, clear stale old-thread ownership immediately, and use the true empty state only when no conversation is selected.
