# Factory Runtime Spec

## Iteration

- current iteration: `86`
- bounded focus: `selected-thread center-header session contract`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread session ownership and switch continuity are already bounded, but the center workspace still hides the most direct answer to which selected session is attached and whether that session is actually live, degraded, or no longer owned.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread attach, SSE authority, reconnect, polling, terminal, and switch datasets.
- Keep the change bounded to the center-header session summary row and adjacent live-ownership indicator in the conversation-first workspace.
- Show healthy selected-thread ownership as `SSE OWNER`, degraded ownership as `RECONNECT` or `POLLING`, and clear ownership immediately on switch or terminal idle.
- Preserve one compact summary row for selected-thread scope and attach state without reviving prose-heavy side status surfaces.
- Keep the bottom-fixed composer intact on desktop and phone layouts.
- Do not introduce new transport, new side surfaces, or renewed `/api/goals` dependency on the healthy path.

## Deliverable

Expose and verify one compact selected-thread center-header session contract so the main conversation workspace shows the attached target and authoritative live ownership state directly from canonical selected-thread state, with healthy `SSE OWNER`, degraded `RECONNECT` or `POLLING`, and immediate ownership clear on switch or terminal idle.
