# Factory Runtime Implementation Plan

## Iteration 216

Preserve one continuous center session workspace during selected-thread restore or resume.

1. Keep the change bounded to the selected-thread restore or resume path, restore placeholder behavior, and verifier expectations.
2. Reuse the existing selected-thread session authority, restore transition, active-session row, and composer dock datasets instead of adding new transport or polling logic.
3. Keep the center conversation shell and bottom-fixed composer mounted during saved-session restore or resume.
4. Show exactly one compact restore or attach placeholder until authoritative SSE ownership returns.
5. Clear stale live-owner treatment immediately before fallback or degraded rendering appears.
6. Keep switch, degraded reconnect or polling fallback, and terminal paths on their existing clear or fail-open behavior.
7. Align static checks, browser checks, and proposal artifacts with the restore or resume continuity contract.
