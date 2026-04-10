# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread handoff and quick-switch paths are now compact and verified, but the workspace still makes users infer whether they are attached to the live tail after scrolling up to read history. That weakens the realtime-session feel because healthy SSE ownership remains active while the visible workspace no longer says whether follow is still attached or paused.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing `liveFollow`, selected-thread SSE ownership, append-stream, and jump-to-latest state instead of widening transport scope.
- Constrain this iteration to live progress visibility inside the selected-thread header summary, jump-to-latest affordance, and composer-adjacent session strip.
- Keep the left rail, runtime APIs, side-panel behavior, SSE transport, and recent-thread quick-switch rail unchanged.
- Clear paused or following follow-state signals immediately on thread switch, reconnect downgrade, polling fallback, and terminal completion.

## Deliverable

Promote the existing selected-thread `liveFollow` state into the conversation-first workspace so the header summary, composer-adjacent session strip, and jump-to-latest affordance explicitly distinguish FOLLOWING versus FOLLOW PAUSED on the healthy selected-thread SSE path, while degraded and terminal paths clear those signals immediately.
