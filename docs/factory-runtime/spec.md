# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership and polling suppression are now in place, but the workspace still depends on explicit proof that thread switches preserve one continuous session shell instead of flashing a reset-like empty state. The remaining UX risk is any attach handoff that makes the center pane feel like it lost session continuity.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing `threadTransition`, selected-thread ownership, composer owner, and session-summary state instead of introducing a new state source.
- Keep the change bounded to the selected-thread switch handoff surface in the center workspace.
- Preserve snapshot-only behavior for non-selected threads and degraded fallback behavior for failed attaches.

## Deliverable

Define and verify the selected-thread switch path as one continuous session shell: clear old-thread live ownership immediately, keep the center workspace and bottom-fixed composer dock mounted, show exactly one compact attach placeholder, and replace it directly with the new snapshot when ownership transfers.
