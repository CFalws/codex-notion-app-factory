# Factory Runtime Implementation Plan

## Iteration 206

Tighten the selected-thread healthy-path transport boundary so append SSE session state is the sole live authority for job, phase, proposal, verifier, and apply state.

1. Keep the change bounded to the selected-thread append SSE path, its session-status projection, and verifier expectations.
2. Prefer append SSE session-status job identity over snapshot or polling-owned `currentJobId/latest_job_id` while healthy selected-thread authority is active.
3. Preserve apply readiness from the selected-thread session strip model instead of live-run or polling-only fallbacks.
4. Suppress polling-owned `syncLatestJob` and goals refresh mutations during healthy selected-thread attach.
5. Preserve reconnect, switch, deselection, restore-gap, and terminal-clear fallback behavior unchanged.
6. Align static checks, browser checks, and proposal artifacts with the tightened healthy-path authority contract.
