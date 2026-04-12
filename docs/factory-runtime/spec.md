# Factory Runtime Spec

## Iteration

- current iteration: `227`
- bounded focus: `prove one authoritative selected-thread SSE session source in deployed verification`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, switch continuity, handoff continuity, restore continuity, and the selected-thread session-stream contract are already present locally. The remaining bounded gap is deployed proof: the workspace gate still needs to fail for exactly one reason when the healthy selected-thread SSE path loses sole authority, polling takes over visibly, or stale ownership revives after downgrade.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting deployed verification to prove that one selected-thread SSE session remains the sole healthy live authority without hidden polling takeover or stale-state revival.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to deployed selected-thread session-authority verification.
- Reuse the current append SSE stream, session-status datasets, and passive mirrored-surface contract; do not broaden transport, UI layout, or store logic.
- Verify that the center timeline and composer-adjacent phase strip stay attributable to the same selected-thread SSE provenance on the healthy path.
- Fail when polling or goal refresh becomes the visible owner on the healthy path.
- Fail when session rotation occurs or when stale live-owned state revives after reconnect or offline downgrade.

## Deliverable

Expose one deployed verification contract where the healthy selected-thread SSE session is the sole live authority, mirrored surfaces stay passive, polling remains fallback-only, and authority loss cannot revive stale live-owned state.
