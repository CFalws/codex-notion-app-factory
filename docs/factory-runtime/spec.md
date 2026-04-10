# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center pane now reads more like one session surface, but the left conversation rail still forces users to infer which thread is actively running. The navigation needs to mirror the selected-thread handoff and live session state so users can identify and return to the active conversation without relying on the side panel or scanning the center pane first.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to selected-thread navigation indicators and keep non-selected thread behavior snapshot-only.
- Leave selected-thread transport ownership, the center-pane inline session block, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and overall shell ownership, but let the selected conversation card mirror pending handoff, active live progress, and fresh assistant-append completion through compact selected-card-only chips and detail labels, then clear those markers on terminal resolution or thread switch.
