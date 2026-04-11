# Factory Runtime Spec

## Iteration

- current iteration: `90`
- bounded focus: `selected-thread switch continuity contract`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread switch path is already implemented in the runtime, but this proposal branch still needs explicit iteration-90 evidence that intentional thread switches preserve one continuous center workspace with one compact attach placeholder instead of resetting through a generic empty-state view.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread switch, summary, composer, and transcript datasets already present in the center workspace.
- Keep the change bounded to the selected-thread switch continuity contract in the center timeline and bottom-fixed composer shell.
- Preserve exactly one compact transition placeholder during switch and never flash the generic timeline empty state on intentional conversation changes.
- Clear previous-thread live ownership and follow markers immediately while keeping the composer fixed and reachable.
- Keep the bottom-fixed composer intact on desktop and phone layouts.
- Do not introduce new transport, new side surfaces, or renewed `/api/goals` dependency on the healthy path.

## Deliverable

Record and verify the selected-thread switch continuity contract so intentional thread switches keep the conversation shell and composer mounted, show exactly one compact attach placeholder, clear stale live ownership immediately, and avoid `/api/jobs` and `/api/goals` fallback on the intended path.
