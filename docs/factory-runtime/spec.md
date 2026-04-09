# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now has a stronger active conversation pane and a more compact composer, but phone-width navigation still opens into app-level controls before thread switching. The remaining friction is a mobile nav sheet that feels like an admin sidebar instead of a conversation-first session switcher.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

On phone widths, make the nav sheet lead with the conversation list and new-conversation action, while moving app selector, deploy link, and related operator controls into a collapsed secondary section that remains reachable without displacing thread switching.
