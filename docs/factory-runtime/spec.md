# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace is close to a continuous session shell, but thread switches still need to prove that the old thread loses ownership immediately and that the center pane never flashes a generic reset. Users should stay inside the mounted transcript and composer shell while one compact `SWITCHING` placeholder bridges the attach gap.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to selected-thread switch continuity in the existing center workspace and composer ownership path.
- Keep the selected-thread SSE path, session strip ownership, bottom follow control, composer behavior, and side-panel behavior unchanged.
- Leave transport scope, deployed verification gate, selected-row live ownership, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make intentional thread switches render as one continuous handoff: clear old-thread live ownership immediately, keep the transcript and composer mounted, show exactly one compact `SWITCHING` placeholder until attach resolves, and never fall back to a generic empty-state flash during that transition.
