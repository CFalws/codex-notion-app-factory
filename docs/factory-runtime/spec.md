# Factory Runtime Spec

## Iteration

- current iteration: `85`
- bounded focus: `selected-thread switch continuity contract`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread session ownership is already bounded, but the proposal branch still needs explicit iteration-85 evidence that intentional thread switches preserve one continuous selected-session workspace instead of falling back to generic empty-state semantics.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session, thread-transition, composer-dock, and active-session-row datasets.
- Keep the change bounded to the selected-thread switch continuity contract already present in the center shell, composer dock, and active-session rail mirror.
- Preserve one compact transition placeholder during switch and never flash the generic no-conversation empty state on intentional switches.
- Clear stale old-thread live ownership immediately and mirror the same switching target into the left-rail active-session row without making non-selected rows live-owned.
- Keep the bottom-fixed composer intact on desktop and phone layouts.
- Do not introduce new transport, new side surfaces, or renewed `/api/goals` dependency on the healthy path.

## Deliverable

Record and verify the selected-thread switch continuity contract so intentional thread switches keep the center shell and bottom-fixed composer mounted, show exactly one compact transition placeholder, clear stale old-thread ownership immediately, and mirror the same switching target into the active-session rail row until the new snapshot attaches.
