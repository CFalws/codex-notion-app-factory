# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Phone-width footer flow is materially closer to a live session now, but desktop still risks reading like an operator dashboard because execution logs, learning summaries, and workspace context remain mixed into the always-visible left rail instead of collapsing behind a secondary surface.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

On desktop widths, keep the thread rail continuously visible, keep the transcript and composer dominant in the center pane, and move nonessential operator and status content behind a secondary panel that stays collapsed by default while a conversation is active.
