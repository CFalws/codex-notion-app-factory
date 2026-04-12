# Factory Runtime Implementation Plan

## Iteration 253

Unify the selected-thread footer dock into one canonical session-composer bar.

1. Keep the change bounded to selected-thread footer dock rendering and matching verifier expectations.
2. Preserve the existing selected-thread `session_status` plus SSE authority path.
3. Reuse the existing selected-thread owner, transport, proposal, and follow models from the footer strip.
4. Hide the separate composer owner row whenever its state is merged into the strip.
5. Keep non-selected rows snapshot-only.
6. Keep switching, restore, degraded, handoff, and idle state explicit in that same single footer surface.
7. Align proposal artifacts with the merged footer-session contract.
Iteration 245 does not widen runtime or UI ownership. It records that the selected-thread center header already exposes the canonical ownership chip beside the session summary and that deployed verification already attributes healthy visibility to that selected-thread SSE-owned signal rather than to polling or side-panel inference.
Iteration 248 keeps transport and header ownership unchanged and restores the same selected-thread certainty directly at the input surface by keeping the composer owner row visible for healthy, handoff, switching, and restore states while preserving explicit degraded or idle clearing.
Iteration 249 does not widen runtime or UI ownership because the selected-thread rail mirror is already correct in this branch: the sticky active-session row is canonical on the healthy selected-thread SSE path, non-selected rows remain snapshot-only, and the deployed gate already attributes that rail marker to the intended selected-thread authority source.
Iteration 252 keeps the selected-thread runtime path unchanged because healthy SSE ownership was already correct in this branch, and tightens the deployed verification seam so that proof of success follows selected-thread SSE phase progression to `proposal.ready` rather than job polling.
Iteration 253 keeps transport and verifier ownership unchanged and merges the previously split footer owner row into the session strip so the selected-thread typing surface reads as one canonical session-composer bar.
