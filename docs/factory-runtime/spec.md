# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership is still hard to distinguish from degraded retry or polling fallback in the central conversation workspace. The header summary shows path and phase, but it does not yet expose one compact live-session ownership indicator that downgrades immediately when retry or session rotation breaks the intended path.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread header summary row, selected-thread SSE ownership datasets, and current app session metadata instead of widening transport scope.
- Constrain this iteration to one compact header live-session ownership indicator in the selected-thread workspace.
- Keep the selected-thread SSE path, transcript flow, footer live strip, side-panel behavior, and rail snapshot behavior unchanged.
- Leave transport scope, runtime APIs, polling fallback rules, and proposal flow unchanged while surfacing degraded-path visibility in the header.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but add exactly one compact header live-session indicator that shows `SSE OWNER` only on healthy selected-thread SSE ownership and downgrades to `RECONNECT` or `POLLING` on retry, polling fallback, or session rotation, while clearing on thread switch and terminal completion.
