# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The footer composer still reads too much like an operator form because apply and auto-open stay fully expanded beside the primary send path. Even after live-state ownership was simplified, the active workspace still does not feel chat-first enough at the point where the operator actually types.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the footer composer surface and its local utility affordance.
- Keep the selected-thread SSE path, session strip ownership, bottom follow control, thread navigation behavior, and side-panel behavior unchanged.
- Leave transport scope, selected-row live ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make the footer composer read as a stricter chat-first surface: the textarea plus primary send action stay visually dominant, while apply and auto-open move behind one compact secondary utility affordance. The session strip and bottom follow control remain the only live-progress surfaces, and no new footer status surface is introduced.
