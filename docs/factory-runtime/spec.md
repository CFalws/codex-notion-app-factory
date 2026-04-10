# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread switch path already uses a dedicated transition shell, but the intended-path proof did not yet explicitly show that old-thread live ownership clears immediately. Without that proof, a healthy prior-thread inline block or follow ownership could survive a switch unnoticed and undermine the single-session workspace contract.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append SSE transport, ownership, `liveRun`, transcript live activity, and `autonomySummary` data instead of adding a new backend or transport path.
- Keep the change bounded to the selected-thread switch path and its existing selected-thread datasets.
- Reuse the current `threadTransition`, composer shell, inline session block, and follow ownership state instead of adding new status surfaces.
- Keep the center conversation shell and bottom-fixed composer mounted during an intentional switch.
- Show exactly one compact transition placeholder until the new selected-thread snapshot attaches.
- Clear prior-thread healthy inline-block ownership and follow ownership immediately on switch.
- Keep degraded reconnect, polling fallback, ownership loss, terminal idle, and switch states visibly non-owned or cleared so they cannot look like stale healthy live progression.

## Deliverable

Define and verify one selected-thread switch path where the conversation shell and composer stay mounted, exactly one compact transition placeholder appears before attach, and prior-thread live-owned inline-block and follow ownership cues clear immediately instead of lingering through the transition.
