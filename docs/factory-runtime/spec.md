# Factory Runtime Spec

## Iteration

- current iteration: `145`
- bounded focus: `map explicit selected-thread SSE phase labels into the existing header and composer-adjacent session chrome without adding a new authority surface`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread header ownership chip and composer-adjacent session rail already reflect healthy and degraded ownership, but they still leave operators inferring the current live stage because generic ownership wording survives where explicit phase labels already exist in the selected-thread SSE state.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the existing session chrome to show the current live selected-thread phase at a glance without introducing another status surface.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration presentation-only in the render layer plus focused verifier and doc updates.
- Do not change transport, polling suppression, backend state sources, or composer ownership rules.
- Keep the center timeline as the only authority-looking live session surface.
- Reuse the existing selected-thread session status, shell-phase derivation, and degraded-path rules.
- Clear phase-owned treatment immediately on reconnect downgrade, polling fallback, switch, deselection, and terminal idle.

## Deliverable

Expose explicit selected-thread phase labels through the existing header indicator context and composer-adjacent live session chrome so healthy SSE progression reads as `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED` without adding a second authority surface.
