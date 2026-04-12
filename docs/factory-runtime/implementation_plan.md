# Factory Runtime Implementation Plan

## Iteration 242

Make the left-rail active-session row an explicit canonical mirror of selected-thread session-status plus SSE authority.

1. Keep the change bounded to `deriveSelectedThreadActiveSessionRowModel` and matching verifier expectations.
2. Preserve the existing selected-thread `session_status` plus SSE authority path.
3. Mark healthy selected-thread active-session visibility as canonical and owned when it is sourced from the selected-thread SSE path.
4. Keep switching, handoff, degraded, and idle clear behavior unchanged.
5. Keep non-selected rows snapshot-only.
6. Align proposal artifacts with the canonical left-rail active-session mirror contract.
Iteration 245 does not widen runtime or UI ownership. It records that the selected-thread center header already exposes the canonical ownership chip beside the session summary and that deployed verification already attributes healthy visibility to that selected-thread SSE-owned signal rather than to polling or side-panel inference.
Iteration 248 keeps transport and header ownership unchanged and restores the same selected-thread certainty directly at the input surface by keeping the composer owner row visible for healthy, handoff, switching, and restore states while preserving explicit degraded or idle clearing.
