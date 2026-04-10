# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already exposes ownership and transport through the intended SSE path, but the center header and footer still require too much prose reading. The session summary row, composer owner row, and composer-adjacent live strip should read as one compact target-first structure instead of helper-copy chrome.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE and handoff ownership model instead of widening transport scope.
- Constrain this iteration to the selected-thread center header summary row, composer owner row, and composer-adjacent live strip.
- Keep the selected-thread SSE path, footer composer structure, side-panel behavior, and rail ownership model unchanged.
- Leave transport scope, runtime APIs, thread-switch behavior, handoff semantics, and selected-row live ownership unchanged while making the visible session chrome shorter and more chip-first.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but compress the selected-thread summary row, composer owner row, and composer-adjacent live strip into one target-first chip structure: compact scope, path, state, and hint labels; compact owner target and attach labels; compact live strip detail copy; and no new status surface or prose-heavy helper row competing with the transcript.
