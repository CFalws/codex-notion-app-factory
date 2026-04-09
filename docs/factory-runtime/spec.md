# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace now has a stronger realtime handoff inside the transcript and a cleaner active-thread header, but the bottom interaction surface still reads like an admin form. The remaining friction is a prose-heavy composer with competing controls that makes message entry feel secondary to proposal operations.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Convert the footer into a compact chat-style session composer where the textarea is the dominant surface, send is the primary action, proposal controls stay accessible but demoted, and the existing composer-adjacent activity bar remains the only live-status surface in the active pane.
