# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live path is present, but the main conversation header still does not make intended-path transport ownership explicit enough. An operator should be able to see that the active workspace is healthy SSE-owned without inferring it from left-rail cues or follow-state wording.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread session summary, append-stream, live-follow, and degradation selectors instead of introducing a new runtime state source.
- Keep the change bounded to the selected-thread center workspace header and its machine-readable datasets.
- Do not add a prose-heavy status panel or broaden polling-driven state.
- Clear ownership immediately on thread switch, terminal resolution, reconnect downgrade, or polling fallback.

## Deliverable

Expose one compact selected-thread header ownership chip adjacent to the session summary that shows `SSE OWNER` on the healthy intended path, downgrades to `RECONNECT` or `POLLING` on degraded paths, publishes machine-readable ownership/source/reason datasets, and remains absent when the session is idle or no longer selected.
