# Factory Runtime Spec

## Iteration

- current iteration: `129`
- bounded focus: `use one authoritative SSE-derived phase vocabulary across selected-thread session surfaces`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership and verifier-evidence authority are already established, but the selected-thread shell still lets different surfaces fall back to generic labels like `LIVE`, `READY`, or `ACTIVE`. That forces the operator to infer which label is authoritative instead of reading one shared phase vocabulary.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session even while changing threads.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the selected-thread SSE ownership, switching continuity, transcript-owned rich live detail, compact header ownership chrome, footer session bar, left-rail compaction, and degraded fallback UI contracts intact.
- Do not introduce a new transport, backend protocol, persistence layer, or a second live-status authority.
- Reuse the existing selected-thread phase progression as the only healthy-path source for visible shell phase labels.
- Keep degraded reconnect, polling fallback, switch, and deselection labels explicit instead of leaving stale healthy-phase labels behind.
- Preserve reconnect and polling fallback only as explicit degraded paths that clear or downgrade healthy ownership in the same render cycle.

## Deliverable

Define and verify one selected-thread shell-phase contract where the left rail, header summary, and composer-adjacent live strip all use the same authoritative SSE-derived phase label on the healthy path, and clear or downgrade that label immediately on degraded paths.
