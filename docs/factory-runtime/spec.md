# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center pane is now more message-first, but session ownership and unseen live pressure are still hard to read from the navigation column alone. The left rail should mirror the active selected-thread session state in one compact sticky row so users can keep track of owner, switching, reconnecting, handoff, and unseen live pressure without leaving the conversation-first workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE ownership, thread transition, and live-follow datasets instead of widening transport scope.
- Constrain this iteration to the left conversation navigation render path.
- Keep the selected-thread SSE path, footer composer structure, side-panel behavior, and center-pane session chrome unchanged.
- Leave transport scope, runtime APIs, polling fallback rules, and proposal flow unchanged while tightening selected-thread navigation mirroring.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but add one compact sticky active-session row above the conversation list that mirrors the selected-thread conversation id, current owner or phase cue, follow or unseen state, and switching status from existing selected-thread state, then clears on true idle, terminal resolution, reconnect downgrade, polling fallback, or thread switch.
