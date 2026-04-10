# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread live state is now compact and verified, but an intentional thread switch can still feel like a reset if the active conversation shell drops to the generic empty view before the next snapshot attaches. The workspace should keep the conversation shell and composer dock mounted and show one compact attach placeholder tied to the target thread until the selected-thread handoff completes.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing `threadTransition`, selected-thread SSE ownership, append-stream, and snapshot attach datasets instead of widening transport scope.
- Constrain this iteration to intentional selected-thread switch continuity inside the center conversation shell.
- Keep transport scope, runtime APIs, side-panel behavior, sticky live rail surfaces, and cross-thread mirroring unchanged.
- Clear the old thread's live ownership immediately on switch and never show the generic empty-state reset during an intentional selected-thread handoff.

## Deliverable

Keep the existing conversation-first shell and composer dock mounted during an intentional selected-thread handoff, render exactly one compact transition placeholder for the target conversation until the new snapshot and append stream attach, and ensure stale live-owned chips and rails from the old thread clear immediately while the generic empty-state view remains reserved for true no-conversation idle.
