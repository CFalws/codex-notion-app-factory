# Factory Runtime Spec

## Iteration

- current iteration: `180`
- bounded focus: `make the transcript live rail the only healthy selected-thread readable session surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center pane already has healthy transcript, header, and footer session surfaces. That leaves the operator cross-reading multiple regions to understand the same live session instead of reading one canonical conversation-first rail.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the active conversation flow itself to explain the current live session without needing header or footer mirrors.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the healthy selected-thread presentation seam across transcript, header, and footer surfaces in the operator console.
- Reuse the existing selected-thread SSE and session model already driving transcript, header, and footer surfaces; do not change transport ownership rules.
- Render exactly one compact chip-first readable session rail in the transcript on the healthy selected-thread path.
- Keep header and footer surfaces as degraded, reconnect, restore, switch, and non-authoritative fallback only.
- Fail closed on degraded, reconnect, polling fallback, restore-gap, deselected, switched, and no-selection states.

## Deliverable

Expose one compact authoritative transcript-local session rail so the operator can read selected-thread scope, ownership, phase, path, and autonomy progression without relying on healthy header or footer mirrors.
