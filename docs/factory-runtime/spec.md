# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread center session and footer are now unified, but the top header still keeps a separate phase chip and compact session summary row above the transcript. That header chrome competes with the inline session block instead of letting the conversation history start immediately under the title.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport, ownership, `liveRun`, transcript live activity, and `autonomySummary` data instead of adding a new backend or transport path.
- Keep the change bounded to the selected-thread header chrome and existing selected-thread SSE-owned datasets.
- Reuse the current header title block and session summary datasets instead of adding new status surfaces.
- Remove or compact the separate live-status header chrome so the conversation history becomes the first dominant center surface.
- Keep the inline session block, left rail, and composer-adjacent strip as the remaining selected-thread live surfaces.
- Keep degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states visibly non-owned or cleared so they cannot look like stale healthy live progression.

## Deliverable

Define and verify one selected-thread center workspace where the title stays, but the separate phase chip and session summary header chrome no longer compete with the transcript, while live session authority remains on the inline block, rail, and composer-adjacent strip.
