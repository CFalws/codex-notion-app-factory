# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace still splits one healthy live session across two center-pane surfaces: the inline session block handles handoff and degraded states, while the transcript-tail live activity separately handles healthy live progress. That fragmentation weakens the conversation-first session feel and makes the operator infer that both surfaces belong to the same live run.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport, ownership, `liveRun`, transcript live activity, and `autonomySummary` data instead of adding a new backend or transport path.
- Keep the change bounded to selected-thread center-pane rendering and existing selected-thread SSE-owned datasets.
- Reuse the current inline session block, `liveRun`, phase mapping, and autonomy summary instead of adding new transport or a new timeline surface.
- Route healthy selected-thread live progress through the same inline block path already used for handoff and degraded states.
- Suppress the separate transcript-tail live activity whenever that unified inline block is active.
- Keep degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states visibly non-owned or cleared so they cannot look like stale healthy live progression.

## Deliverable

Define and verify one selected-thread center session block that renders handoff, healthy live, and degraded states from the same SSE-owned authority path, with no duplicate transcript-tail live activity while that block is active.
