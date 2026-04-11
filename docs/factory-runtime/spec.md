# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread session ownership and chrome vocabulary are now bounded, but intentional thread switches can still let an older in-flight fetch clear or render over the newer target, which breaks the feeling of one continuous live workspace.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread switch placeholder, mounted composer shell, and SSE ownership datasets.
- Keep the change bounded to selected-thread switch handling in the controller and existing browser-proof verifier.
- Clear old-thread live ownership immediately on intentional switch and keep it cleared until the new target attaches or degrades.
- Ensure rapid follow-up thread selection cancels the earlier switch path instead of letting stale async results retake the workspace.
- Keep the generic empty state limited to true no-conversation idle only.
- Do not introduce new transport, polling, or layout surfaces.

## Deliverable

Use request-scoped selected-thread transitions so the mounted conversation shell and composer stay continuous across intentional switches, exactly one bounded switching placeholder remains visible, and stale switch results cannot clear or render over the newer target.
