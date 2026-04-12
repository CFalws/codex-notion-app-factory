# Factory Runtime Tasks

## Iteration 230

- [x] Keep the change bounded to the existing selected-thread append SSE ownership path and matching proposal artifacts.
- [x] Reuse `appendStream.sessionStatus`, canonical selected-thread session-status derivation, and current render boundaries instead of adding new runtime behavior.
- [x] Keep the transcript-centered session surface as the only healthy live-owned authority for phase and proposal progression.
- [x] Prevent healthy `/api/jobs/{id}` and `/api/apps/{appId}/goals` polling reads from becoming visible owners in the selected-thread workspace.
- [x] Preserve reconnect and polling downgrade as explicit degraded fallback that clears live ownership immediately.
- [x] Align static checks, browser checks, and proposal artifacts with the selected-thread session-status authority contract.
