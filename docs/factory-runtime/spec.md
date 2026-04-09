# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path, stronger transcript follow behavior, and a more conversation-first composer hierarchy, but live progress is still presented as a split explanatory strip. The remaining friction is that the active workspace reads like a transcript plus status strip instead of one continuous realtime conversation surface.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only session-strip compression on top of the existing selected-thread footer dock.
- Leave selected-thread transport, footer live rail ownership, phase mappings, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but compress the selected-thread composer-adjacent live strip into one chip-first inline activity bar that keeps transport, phase, proposal readiness, provenance, and compact action cues readable without a split explanatory layout.
