# Factory Runtime Spec

## Iteration

- current iteration: `232`
- bounded focus: `extend selected-thread session_status into complete live autonomy authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, switch continuity, restore continuity, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, transcript-tail session block, and selected-thread session-status authority are already present. The remaining bounded gap is autonomy identity drift on the healthy path: goal identity and iteration metadata should travel inside `session_status` itself so the selected-thread workspace does not rely on separate goals polling while SSE ownership is intact.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting live autonomy identity, phase, proposal, review, verify, ready, and applied progression to stay coherent across the active session without hidden goals-summary refetches.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the existing selected-thread append SSE ownership path, the canonical runtime `conversation_session_status` helper, current selected-thread projections, and matching proposal artifacts.
- Add autonomy identity fields to `session_status` instead of introducing a new transport or a second authority path.
- Reuse the current transcript-tail session block, selected-thread session-status helper, and fallback gates.
- Keep the transcript-tail session block as the only healthy live-owned surface.
- Keep goals polling explicit fallback-only for degraded or non-authoritative states.
- Preserve reconnect and polling downgrade as explicit degraded fallback that clears canonical live ownership immediately.
- Keep switch, restore, handoff, and terminal clear behavior on the current intended path.

## Deliverable

Expose one conversation-first selected-thread workspace where healthy live autonomy identity and phase progression arrive through append/bootstrap `session_status`, the transcript-tail block remains the canonical live owner, and goals polling stays explicit fallback-only instead of a healthy visible authority.
