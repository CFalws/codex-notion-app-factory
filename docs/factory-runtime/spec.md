# Factory Runtime Spec

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

The selected-thread inline phase item has healthy-path transport and phase data, but terminal `READY` and `APPLIED` visibility is not explicit enough. Without a deterministic retention rule, the timeline can either clear too quickly to verify or linger long enough to imply stale healthy ownership.

## Target User

The primary user is the operator or developer using the phone-friendly workspace and expecting the active conversation to behave like one live Codex desktop session.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Reuse the existing selected-thread SSE ownership, append-stream append ids, and live-run event metadata instead of introducing a new runtime state source.
- Keep the change bounded to the selected-thread inline live phase item in the conversation timeline.
- Do not add a second status surface or broaden polling-driven state.
- Clear retained terminal visibility immediately on next append, thread switch, reconnect downgrade, polling fallback, or ownership loss.

## Deliverable

Define and implement explicit inline terminal retention semantics so exactly one selected-thread inline live phase item can retain `READY` or `APPLIED` briefly while the same healthy SSE-owned session still owns the thread, then clear deterministically on the next append or ownership loss.
