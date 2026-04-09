# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread transcript already carries one compact live activity turn, but typing and watching progress still require too much eye travel between the composer and the workspace edges. The remaining friction is immediately above the input area: the active conversation needs one compact composer-adjacent live strip that keeps current phase and latest SSE detail visible where the operator types, without lingering after terminal resolution.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the composer-adjacent live strip inside the existing selected conversation footer shell.
- Leave selected-thread transport ownership, non-selected thread rendering, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path, transcript-tail live turn, and workspace shell, but add one compact composer-adjacent live session strip that appears only while selected-thread SSE is actively driving a run, mirrors the current phase and detail in place, and hides cleanly on terminal resolution.
