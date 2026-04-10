# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership, polling suppression, and switch continuity are now in place, but the main workspace still splits live conversation from autonomy verdicts. Operators still need the secondary panel to understand the latest iteration path verdict, verifier acceptability, and blocker state, which breaks the single-session feel.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the already-fetched relevant goal summary and the existing selected-thread live-session ownership path instead of introducing new transport or proposal semantics.
- Keep the change bounded to the selected-thread inline session surface in the center workspace.
- Preserve snapshot-only behavior for non-selected threads and suppress the autonomy projection on degraded fallback, no-goal, or switch paths.

## Deliverable

Define and verify one compact autonomy row inside the selected-thread live session block so iteration number, intended-path verdict, verifier acceptability, and blocker reason are visible in the conversation workspace whenever the selected thread currently owns the live run.
