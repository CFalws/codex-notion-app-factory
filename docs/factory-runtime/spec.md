# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path and compact live cues, but append-stream health still feels implicit. The remaining friction is trust: users should be able to see immediately whether the selected thread is live, reconnecting, or offline without inferring that from hidden state or secondary operator surfaces.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only stream-health cue work on top of the existing selected-thread state path.
- Leave the selected-thread timeline, left rail, center-pane header, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but make the composer-adjacent live rail show an explicit live-session contract for connecting, live, reconnecting, and offline states, with compact degraded recovery cues while keeping selected-thread ownership tied only to the existing selected-thread state path.
