# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace is already close to the intended conversation-first layout, but this lane still lacks a deployed proof step that demonstrates one real browser-visible session advancing through the healthy selected-thread SSE path instead of polling or fallback. The remaining friction is intended-path evidence, not another layout gap.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to deployed selected-thread workspace verification and its focused static wiring.
- Leave the selected-thread timeline, header minimization, chip-first live rail, submit handoff, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace UI unchanged, but add a deployed workspace gate that proves one real `factory-runtime` conversation advances through ordered selected-thread SSE phase evidence and fails on degraded signals such as retry fallback, runtime exception, missing SSE ownership, or unexpected session rotation.
