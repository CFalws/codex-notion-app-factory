# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The main workspace still risks feeling discontinuous during intentional thread switches if the center pane briefly reads like an empty request viewer instead of one continuous session. The switch path should keep the conversation shell and composer dock mounted, clear stale old-thread ownership immediately, and show one compact transition placeholder until the new snapshot attaches.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership, thread transition, and composer target datasets instead of widening transport scope.
- Constrain this iteration to the intentional selected-thread switch path in the center workspace and footer composer.
- Keep the selected-thread SSE path, footer composer structure, side-panel behavior, and rail snapshot behavior unchanged.
- Leave transport scope, runtime APIs, polling fallback rules, and proposal flow unchanged while tightening switch continuity.

## Deliverable

Keep the existing selected-conversation SSE path and conversation-first shell ownership, but preserve one continuous selected-thread workspace during intentional thread switches: clear old-thread live and follow ownership immediately, keep the transcript and composer dock mounted, and render exactly one compact `SWITCHING` placeholder until the new selected-thread snapshot attaches, with the generic empty state limited to true no-conversation idle.
