# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already shows live progress near the composer and inside the transcript, but the submit-to-first-append handoff still feels like a gap. After send, the active conversation needs one temporary outbound turn and then one temporary assistant placeholder so the handoff remains visible in the conversation flow until the first real SSE assistant append arrives.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected-thread transcript handoff state inside the existing conversation flow.
- Leave selected-thread transport ownership, composer-adjacent live strip, non-selected thread rendering, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path, transcript-tail live turn, and workspace shell, but make the selected transcript expose exactly one temporary pending user turn after submit and exactly one temporary assistant placeholder after acceptance until the first real assistant SSE append arrives, then clear that handoff state cleanly on append, terminal resolution, idle reset, or thread switch.
