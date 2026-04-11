# Factory Runtime Implementation Plan

## Iteration 204

Extend the existing selected-thread live milestone lane so the healthy SSE-owned path shows explicit autonomy progression states without adding a new surface.

1. Keep the change bounded to the selected-thread milestone model, its timeline renderer, and verifier expectations.
2. Reuse the current selected-thread authority and live autonomy helpers instead of adding a new status owner.
3. Make the live milestone lane explicitly represent `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
4. Preserve the current healthy-path composer-authoritative ownership contract from iteration 203.
5. Preserve degraded, reconnect, polling fallback, switch, deselection, restore-gap, and terminal-clear behavior without adding new fallback UI.
6. Align static and browser verification with the explicit progression lane.
