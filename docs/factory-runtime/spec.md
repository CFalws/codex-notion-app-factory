# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The left rail now has stronger selected-thread session mirroring, but non-selected rows can still collapse too many snapshot states into `IDLE` and can fall back to noisier event prose when no recent message exists. Thread scanning should stay compact and snapshot-only while making waiting, active, ready, done, failed, and idle states easier to distinguish at a glance.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing conversation messages, event history, and selected-thread live owner datasets instead of widening transport scope.
- Constrain this iteration to the conversation-list snapshot labeling and preview helpers.
- Keep the selected-thread SSE path, footer composer structure, side-panel behavior, and center-pane session chrome unchanged.
- Leave transport scope, runtime APIs, polling fallback rules, and proposal flow unchanged while tightening rail scan clarity.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but refine non-selected conversation cards so each row resolves to one fixed-priority snapshot label and one bounded preview line that prefers recent assistant or user content over noisier event prose, while selected-row live mirroring remains the stronger surface.
