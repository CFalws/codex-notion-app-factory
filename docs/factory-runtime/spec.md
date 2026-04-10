# Factory Runtime Spec

## Request

- title: `Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread session cues are now compact and expected-path healthy, but intentional thread switches can still feel fragile unless the conversation shell clearly stays in place during attach. The key remaining UX risk is any reset-like transition that makes the workspace look like it lost context instead of moving from one live session to another.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave more like a Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing `threadTransition`, session summary, composer owner, and selected-thread SSE ownership selectors instead of adding a new runtime state source.
- Constrain this iteration to the selected-thread transition path in the center conversation workspace and composer ownership surface.
- Keep the left rail, runtime APIs, side-panel behavior, SSE transport, and broader workspace layout unchanged.
- Clear stale old-thread live ownership immediately during switch and keep the generic empty state limited to non-transition fallback paths.

## Deliverable

Preserve the conversation-first shell during intentional thread switches by keeping the composer dock mounted, moving the session summary and composer owner row into SWITCHING or ATTACH for the target thread, and showing exactly one compact attach placeholder until the new snapshot attaches, with no stale live ownership from the old thread.
