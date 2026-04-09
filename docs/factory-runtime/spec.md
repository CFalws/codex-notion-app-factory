# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path, explicit stream-health cues, and selected-row rail awareness, but the transcript still needs a better reading contract during live appends. The remaining friction is live reading flow: users should stay anchored on older content when they scroll up and only return to the latest append when they explicitly re-engage follow mode.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to selected-thread transcript follow behavior and the existing jump-to-latest affordance.
- Leave the selected-thread header, left rail markers, footer live rail, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but refine the selected-thread transcript so auto-follow only stays active while the reader is already near the latest append and the existing jump-to-latest control plus active composer can explicitly restore follow mode.
