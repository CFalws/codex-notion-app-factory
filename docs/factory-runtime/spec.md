# Factory Runtime Spec

## Iteration

- current iteration: `147`
- bounded focus: `collapse selected-thread SSE session-phase event cards into the existing single center-timeline live activity block`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live timeline, header ownership, phase chips, and switch continuity are already stronger, but healthy SSE execution can still leave session progress split between the center live activity block and duplicate selected-thread session-event cards.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the selected conversation to read like one live session timeline instead of two competing center-pane session surfaces.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the selected-thread center-timeline render path plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, or composer ownership rules.
- Reuse the existing selected-thread live activity item, session surface model, and degraded-path fail-closed rules.
- Keep the center timeline as the only authority-looking selected-thread live-session surface during active SSE execution.
- Suppress duplicate selected-thread session-event cards only while the selected-thread live activity block is visible.
- Preserve existing degraded, restore, handoff, terminal clear, and thread-switch clearing rules.
- Keep the bottom-fixed composer behavior unchanged.

## Deliverable

Expose exactly one machine-readable selected-thread live-session block in the center timeline during healthy SSE execution by collapsing duplicate selected-thread SSE session-event cards into the existing live activity block while its chips and detail copy carry phase, verdict, verifier, blocker, and milestone progress.
