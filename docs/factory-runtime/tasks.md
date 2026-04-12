# Factory Runtime Tasks

## Iteration 252

- [x] Keep the change bounded to selected-thread SSE proof and verifier artifacts.
- [x] Preserve the existing selected-thread `session_status` plus SSE authority path unchanged.
- [x] Leave the already-correct selected-thread runtime polling suppression unchanged.
- [x] Remove deployed verifier dependence on `latest_job_id` discovery and `/api/jobs/{id}` polling.
- [x] Require healthy selected-thread success to terminate on `proposal.ready` and SSE phase ordering.
- [x] Align proposal artifacts with the selected-thread SSE proof-path contract.
- Iteration 245: confirm the selected-thread center header already exposes the canonical ownership chip and keep deployed verification bound to that machine-readable selected-thread signal without adding another live-status surface.
- Iteration 248: keep the selected-thread composer owner row visible on healthy and transition paths, render `READY` only on healthy SSE-owned state, and assert degraded paths never retain stale ready ownership.
- Iteration 249: record that the sticky left-rail active-session row is already the canonical selected-thread SSE mirror and keep non-selected rows snapshot-only with immediate clear or downgrade on degraded paths.
- Iteration 252: record that healthy selected-thread runtime transport was already session-scoped and move the remaining deployed proof path off job polling and onto `proposal.ready`.
