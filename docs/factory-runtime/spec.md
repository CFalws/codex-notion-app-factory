# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already exposes exact SSE-driven phase progression and better phone shell behavior, but live progress still sits at the workspace edges. The remaining friction is inside the transcript itself: the active conversation should show the current selected-thread live phase and detail in the message flow instead of making the operator scan to header or footer status surfaces.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected transcript and its composer-adjacent live-state mirror inside the existing center pane.
- Leave selected-thread transport ownership, non-selected thread rendering, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but add one compact transcript-tail live activity turn that mirrors the current selected-thread SSE-derived phase and detail, updates in place during active execution, and disappears cleanly when the live state is no longer selected-thread-SSE-owned.
