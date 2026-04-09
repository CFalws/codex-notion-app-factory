# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The workspace already has the intended selected-thread SSE proof path, a conversation-first center pane, and a clearer left rail, but the composer-adjacent live rail still asks users to read sentence-level status text. The remaining friction is scan speed: users should be able to understand the current handoff or phase from compact cues rather than prose.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to render-only footer live-rail cue work on top of the existing selected-thread state path.
- Leave the selected-thread timeline, left rail, center-pane header, deployed verification gate, and polling fallback rules unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and workspace shell, but tighten the composer-adjacent live rail so it renders compact action cues for sending, accepted, proposal, review, verify, ready, applied, failed, and idle states while keeping selected-thread ownership tied only to the existing selected-thread state path.
