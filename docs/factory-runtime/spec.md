# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread SSE ownership and the inline live session block are now in place, but downgrade transitions still lean on header or fallback chrome. When healthy ownership drops, the center conversation can stop feeling like the primary session surface.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread append-stream and selected-thread-only ownership guardrails instead of extending realtime semantics beyond the active conversation.
- Keep the change bounded to one inline degraded-session marker in the selected-thread timeline.
- Preserve polling and reconnect behavior as explicit degraded fallbacks without leaving stale healthy ownership behind.

## Deliverable

Define and verify one compact inline degraded-session marker for the selected thread so reconnect, polling fallback, session rotation, and ownership-loss transitions remain visible in the center timeline and clear immediately on reattach, idle, terminal, or thread switch.
