# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path, explicit stream-health cues, and stronger transcript follow behavior, but the composer still reads more like a compact admin form than a continuous chat surface. The remaining friction is action hierarchy: message entry and send should dominate the footer while proposal apply and auto-open recede into utility space.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only composer layout work on top of the existing selected-thread footer dock.
- Leave selected-thread transport, footer live rail ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but compress the selected-thread composer so the textarea and primary send action dominate while proposal apply and auto-open move into a compact secondary utility cluster.
