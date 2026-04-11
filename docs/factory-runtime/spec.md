# Factory Runtime Spec

## Iteration

- current iteration: `89`
- bounded focus: `left-rail finite active-session row`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, switch continuity, explicit phase vocabulary, and transcript-top session presentation are already bounded, but the left rail still fails to expose the selected session state through a finite navigation contract. Operators still need the center pane to distinguish handoff from healthy follow or detached follow.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the canonical selected-thread session datasets already exposed through the center header and live follow state.
- Keep the change bounded to the sticky left-rail active-session row above the conversation list.
- Show only finite `HANDOFF`, `LIVE`, `NEW`, or `PAUSED` row labels for the intended selected-thread handoff and healthy live path.
- Clear the row immediately on reconnect downgrade, polling fallback, terminal idle, or thread switch, and keep non-selected rows snapshot-only.
- Keep the bottom-fixed composer intact on desktop and phone layouts.
- Do not introduce new transport, new side surfaces, or renewed `/api/goals` dependency on the healthy path.

## Deliverable

Expose and verify exactly one sticky left-rail active-session row derived only from canonical selected-thread state so operators can read `HANDOFF`, `LIVE`, `NEW`, or `PAUSED` at a glance without reopening the center timeline.
