# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live state is verified, but the primary execution signal in the active conversation still competes with header summary copy instead of reading like one compact Codex-style live rail anchored to the transcript and composer. The composer-adjacent strip should become the primary healthy-path signal and disappear immediately when the path degrades.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership, reconnect, polling, and terminal datasets instead of widening transport scope.
- Constrain this iteration to the compact composer-adjacent live session strip in the selected-thread workspace.
- Keep transport scope, runtime APIs, side-panel behavior, and cross-thread state unchanged.
- Remove the strip immediately on downgrade or terminal resolution rather than stretching it into a degraded-path status surface.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but render exactly one compact live session strip above the composer only while the selected thread is healthy and SSE-owned, keep it chip-first and selected-thread scoped, and clear it on reconnect downgrade, polling fallback, thread switch, or terminal completion.
