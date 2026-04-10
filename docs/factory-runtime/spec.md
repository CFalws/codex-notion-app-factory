# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The healthy selected-thread SSE path now drives the center workspace accurately, but the sticky left-rail active-session row still stops short of mirroring that same phase authority. It marks that a live session exists, yet still leaves the operator inferring the exact current phase from the center pane instead of showing the same owner-phase-follow state directly in the rail.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport, ownership, `liveRun`, session-summary, and active-session row contracts instead of adding a new backend or transport path.
- Keep the change bounded to the sticky left-rail active-session row for the selected thread.
- Make the active-session row mirror the same selected-thread SSE owner, phase, and follow or unseen state already proven in the center workspace.
- Keep degraded reconnect, polling fallback, ownership loss, and switch states visibly non-owned so they cannot look like healthy live progression.

## Deliverable

Define and verify one healthy selected-thread SSE path where the sticky active-session row mirrors compact owner, phase, and follow or unseen state from the same append-driven session authority as the selected conversation, while degraded states remain clearly non-owned.
