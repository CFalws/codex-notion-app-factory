# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path and compact live rail, but the active center header still reads too much like app chrome. The remaining friction is hierarchy: the first readable surface in the center pane should be the selected conversation and its live phase, not the app shell.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only center-pane header work on top of the existing selected-thread state path.
- Leave the selected-thread timeline, footer rail, submit handoff, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but make the active header conversation-first by showing selected-thread identity plus a compact live phase label derived from the existing selected-thread state while pushing app-level identity out of the primary reading path.
