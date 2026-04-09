# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path, a compact active-session strip, and stronger composer hierarchy, but the left rail still makes the live session owner too easy to miss. The remaining friction is ownership ambiguity: the selected conversation should read unmistakably as the one live lane bound to the center transcript and composer.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only selected-row rail ownership treatment on top of the existing conversation card contract.
- Leave selected-thread transport, non-selected snapshot ownership, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but strengthen the selected conversation row so it reads as the live session owner at a glance while non-selected rows remain compact and snapshot-only.
