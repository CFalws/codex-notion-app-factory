# Factory Runtime Spec

## Iteration

- current iteration: `120`
- bounded focus: `left rail exposes exactly one sticky active-session row from the healthy selected-thread session model`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, one center live session lane, and one footer session bar are already established. The remaining gap is the left rail: the sticky active-session row still mixes in transition behavior instead of mirroring only the healthy selected-thread SSE session and clearing immediately on degraded or non-selected paths.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, center live-lane, footer session bar, and polling-fallback contracts unchanged.
- Do not introduce a new transport, polling path, backend protocol, or a second rail live-status surface.
- Reuse the existing selected-thread session-status and follow-control models instead of adding another rail authority source.
- Show exactly one sticky active-session row above the left conversation list on the healthy selected-thread SSE path only.
- Let that row carry owner, current phase, and `NEW` or `PAUSED` follow state with unseen-count metadata from the same selected-thread datasets as the center and footer surfaces.
- Clear that row immediately on jump-to-latest follow re-engagement, idle, terminal, reconnect downgrade, polling fallback, deselection, and thread switch.

## Deliverable

Define and verify one active-session rail contract where the left navigation exposes exactly one sticky row for the healthy selected-thread SSE session with owner, phase, and detached follow state, while degraded and non-selected paths clear it immediately.
