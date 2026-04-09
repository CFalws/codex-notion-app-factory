# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace still feels like separate header, transcript, and composer surfaces instead of one Codex-style session lane. The center pane needs to own message history, the in-flight assistant or live-progress block, and the active composer so one selected conversation reads as a single real-time workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to one selected-thread workspace surface and keep non-selected thread behavior unchanged.
- Leave selected-thread transport ownership, non-selected thread rendering, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and overall shell ownership, but turn the selected-thread center pane into one conversation-first session surface: conversation history in the middle, one inline pending-assistant or SSE-owned live-progress block in the transcript flow, and the anchored composer at the bottom, with secondary operator detail kept compact and separate.
