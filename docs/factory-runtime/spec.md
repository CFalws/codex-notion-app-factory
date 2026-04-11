# Factory Runtime Spec

## Iteration

- current iteration: `162`
- bounded focus: `render canonical session_status as one inline selected-thread timeline lane`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center workspace still reads like a transcript plus a separate selected-thread strip. The remaining UX gap is that canonical `session_status` does not yet feel like part of the conversation timeline itself.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting non-message execution progress to appear inside the selected conversation timeline as one live session lane.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the canonical `session_status` to selected-thread timeline rendering seam.
- Do not change transport scope, transcript message ownership, composer docking, footer ownership rules, rail mirroring, or secondary-panel behavior.
- Keep the canonical session-status surface single-instance and fail closed on switch, deselection, terminal completion, or lost authority.
- Keep reconnect and polling fallback visible only as explicitly labeled degraded states.
- Do not let stale thread state or polling-owned residue populate the inline session lane.
- Never make a non-selected thread appear live-owned.

## Deliverable

Render one canonical inline selected-thread session-event lane inside the conversation timeline from `appendStream.sessionStatus`, with immediate fail-closed clearing on switch, deselection, terminal completion, or lost authority.
