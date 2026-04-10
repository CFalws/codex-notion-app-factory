# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The center-pane selected-thread session is now singular, but the bottom workspace still splits live cues between the composer-adjacent strip and the separate owner row underneath it. That duplication weakens the Codex-desktop-style feeling that the live session follows the operator right where they type.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport, ownership, `liveRun`, transcript live activity, and `autonomySummary` data instead of adding a new backend or transport path.
- Keep the change bounded to the composer-adjacent footer strip and existing selected-thread SSE-owned datasets.
- Reuse the current `session-strip`, `composerOwnerState`, transport, follow, and proposal helpers instead of adding new transport or backend state.
- Make the `session-strip` the only composer-adjacent live activity surface while the selected thread is targeted.
- Preserve the fixed composer shell and phone usability.
- Keep degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states visibly non-owned or cleared so they cannot look like stale healthy live progression.

## Deliverable

Define and verify one selected-thread composer-adjacent activity bar that renders ownership, transport, phase, and proposal progress from the same SSE-owned authority path, with no duplicate footer live-status surface while that bar is active.
