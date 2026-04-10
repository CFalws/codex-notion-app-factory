# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread workspace still risks feeling discontinuous during intentional thread switches if the center pane drops to a generic empty reset before the new snapshot binds. The switch path should keep the conversation shell mounted, clear stale old-thread ownership immediately, and render only one compact transition placeholder until attach completes.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-conversation SSE ownership, thread transition, and composer ownership model instead of widening transport scope.
- Constrain this iteration to the selected-thread switch continuity contract in the center-pane render path.
- Keep the selected-thread SSE path, footer composer structure, side-panel behavior, and left-rail ownership semantics unchanged.
- Leave transport scope, runtime APIs, polling fallback rules, and proposal flow unchanged while tightening the switch continuity contract.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but preserve one continuous workspace during intentional thread switches: clear old-thread live ownership immediately, keep the transcript and composer dock mounted, and render at most one compact `SWITCHING` placeholder until the new selected-thread snapshot attaches, with the generic empty state limited to true no-conversation idle.
