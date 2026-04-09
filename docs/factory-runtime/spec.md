# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already exposes exact SSE-driven phase progression, but phone navigation still leaves too much shell chrome between the operator and the active conversation. The remaining friction is structural: on phone widths the conversation drawer should feel deliberate, thread-first, and secondary-control-light so the selected transcript and composer remain the default visible workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to phone-shell behavior in the existing nav sheet and selected conversation surface.
- Leave selected-thread transport ownership, non-selected thread rendering, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but make phone navigation behave like a deliberate conversation drawer: thread switching stays first, app and operator controls stay collapsed behind a secondary section, and closing or selecting from the drawer returns the operator to the selected transcript and composer surface.
