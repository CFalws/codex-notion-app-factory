# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The active conversation can now show live append state and provenance, but the central workspace still makes users look away from the thread to understand whether the agent is currently thinking, running a tool, waiting, or done. That keeps the experience closer to a request form plus separate status panels than to a realtime session workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Add an inline active-session progress row at the timeline/composer boundary for the selected conversation only, driven by existing live conversation events and exposing machine-readable state so browser verification can prove the row follows the intended live path instead of polling-only refresh.
