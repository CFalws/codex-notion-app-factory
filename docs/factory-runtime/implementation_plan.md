# Factory Runtime Implementation Plan

## Iteration 230

Promote selected-thread session status to the single healthy-path realtime authority.

1. Keep the change bounded to the existing selected-thread append SSE ownership path and matching proposal artifacts.
2. Reuse `appendStream.sessionStatus`, canonical selected-thread session-status derivation, and the current render boundaries instead of adding new transport or store seams.
3. Keep the transcript-centered session surface as the only healthy live-owned authority for phase, proposal, review, verify, and apply progression.
4. Prevent healthy `/api/jobs/{id}` and `/api/apps/{appId}/goals` polling reads from becoming visible owners in the selected-thread workspace.
5. Preserve reconnect and polling downgrade as explicit degraded fallback that clears live ownership immediately instead of looking like healthy realtime success.
6. Align static checks, browser checks, and proposal artifacts with the selected-thread session-status authority contract.
