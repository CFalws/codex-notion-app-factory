# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread transcript now carries the live session block, but the bottom follow affordance still exposes a paused state too eagerly. That makes detached-tail behavior feel noisy because the control can appear without real unseen backlog, even though the intended UX should only surface it when the current SSE-owned thread has live appends the operator has not read yet.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread live-follow, append-stream, and selected-thread ownership selectors instead of adding a new runtime state source.
- Constrain this iteration to the transcript-bottom follow affordance in the selected conversation pane.
- Keep the left rail, runtime APIs, side-panel behavior, SSE transport, and broader workspace layout unchanged.
- Clear the follow affordance immediately on jump-to-latest, thread switch, reconnect downgrade, polling fallback, and terminal completion.

## Deliverable

Show the bottom follow control only when the current selected thread is healthy and SSE-owned, the operator is detached from the tail, and unseen live appends exist, while keeping explicit NEW versus PAUSED state mapping and unseen-count datasets machine-readable for the intended selected-thread path.
