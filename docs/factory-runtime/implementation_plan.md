# Factory Runtime Implementation Plan

## Iteration 266

Keep selected-thread proposal and phase authority on session-status plus append SSE across healthy and restore paths, with polling visible only as explicit degradation.

1. Keep the change bounded to selected-thread session authority, phase derivation, and fallback gating.
2. Preserve the existing selected-thread `session_status` plus SSE authority path.
3. Keep proposal, review, verify, ready, and applied visibility sourced from selected-thread session-status and append SSE whenever the selected thread is healthy, attached, or restoring.
4. Allow goals-poll and job-poll data to shape visible state only after selected-thread authority is explicitly absent or degraded.
5. Keep the bottom-fixed composer dock, selected-thread shell, and one-owner timeline behavior unchanged.
6. Keep negative verifier coverage for zero silent polling-owned phase authority on healthy, restore, and switching paths.
7. Align proposal artifacts with the already-present selected-thread authority contract.
Iteration 245 does not widen runtime or UI ownership. It records that the selected-thread center header already exposes the canonical ownership chip beside the session summary and that deployed verification already attributes healthy visibility to that selected-thread SSE-owned signal rather than to polling or side-panel inference.
Iteration 248 keeps transport and header ownership unchanged and restores the same selected-thread certainty directly at the input surface by keeping the composer owner row visible for healthy, handoff, switching, and restore states while preserving explicit degraded or idle clearing.
Iteration 249 does not widen runtime or UI ownership because the selected-thread rail mirror is already correct in this branch: the sticky active-session row is canonical on the healthy selected-thread SSE path, non-selected rows remain snapshot-only, and the deployed gate already attributes that rail marker to the intended selected-thread authority source.
Iteration 252 keeps the selected-thread runtime path unchanged because healthy SSE ownership was already correct in this branch, and tightens the deployed verification seam so that proof of success follows selected-thread SSE phase progression to `proposal.ready` rather than job polling.
Iteration 253 keeps transport and verifier ownership unchanged and merges the previously split footer owner row into the session strip so the selected-thread typing surface reads as one canonical session-composer bar.
Iteration 254 keeps runtime ownership unchanged because switch continuity is already correct in this branch: intentional thread changes already clear old ownership immediately, preserve the selected-thread shell and composer dock, render one compact switching placeholder, and explicitly reject empty-state flashes in the browser gate.
Iteration 259 does not widen runtime or verifier ownership because the one-owner healthy selected-thread timeline contract is already correct in this branch: the inline selected-thread live owner remains canonical during active SSE progress and active SSE session-event cards are already collapsed beneath it.
Iteration 260 does not widen runtime or verifier ownership because the restore path is already correct in this branch: reselecting a saved selected thread enters explicit restore state, mounts the selected-thread shell immediately, resolves healthy ownership through `session.bootstrap` or append SSE, and the deployed gate already rejects early current-thread job or goals polling.
Iteration 262 keeps transport and authority unchanged and narrows only the healthy presentation boundary: the composer-adjacent strip is now suppressed on the healthy selected-thread SSE-owned path so the center timeline remains the sole visible live session owner, while degraded, restore, handoff, terminal, and follow-only paths still retain explicit strip visibility.
Iteration 265 does not widen runtime or verifier ownership because intentional thread switch continuity is already correct in this branch: the selected-thread shell stays mounted, one compact switching placeholder remains visible, the composer dock stays present, stale ownership clears immediately, and the deployed gate already rejects generic empty-state flashes.
Iteration 266 does not widen runtime or verifier ownership because selected-thread session authority is already correct in this branch: healthy and restore paths already derive proposal and phase visibility from session-status plus append SSE, and polling-driven goals or job state remains gated behind explicit loss of selected-thread ownership.
