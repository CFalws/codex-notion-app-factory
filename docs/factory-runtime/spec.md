# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace already exposes ownership and transport clearly, but the submit-to-first-append handoff is still too noisy. After submit, the active thread can imply acceptance in more than one place instead of resolving to exactly one pending outbound user turn, then exactly one temporary assistant placeholder, until the first real assistant append or a clear condition takes over.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE route instead of widening transport scope.
- Constrain this iteration to the selected-thread submit-to-first-append handoff in the existing center workspace and composer-adjacent activity bar.
- Keep the selected-thread SSE path, footer composer, side-panel behavior, and rail ownership model unchanged.
- Leave transport scope, runtime APIs, thread-switch behavior, and selected-row live ownership unchanged while making the handoff state singular and easier to read.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but make the selected-thread handoff resolve to one bounded state at a time: one pending outbound user turn before acceptance, one temporary assistant placeholder after acceptance, one composer-adjacent handoff bar that matches that stage, and immediate clearing on first assistant append, terminal failure, idle reset, polling-only fallback, or thread switch.
