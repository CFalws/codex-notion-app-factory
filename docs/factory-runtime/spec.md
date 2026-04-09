# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live surface is stronger now, but phone-width layout still risks feeling like navigation-first chrome because thread switching and operator controls can visually compete with the active conversation. The remaining friction is that the mobile workspace does not yet make the active conversation unambiguously primary before navigation is opened.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing feature-flagged internal SSE route instead of widening transport scope.
- Leave broader polling, status, and fallback behavior unchanged in this iteration.

## Deliverable

Keep the existing selected-conversation SSE path and composer-adjacent live rail, but make phone-width navigation an explicit drawer or sheet with clear toggle semantics so the active conversation remains the first visible workspace surface until the user deliberately opens navigation.
