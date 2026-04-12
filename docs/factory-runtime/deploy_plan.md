# Factory Runtime Deploy Plan

## Iteration 260

This deploy plan validates that reopening or reselecting a running selected thread stays on one restore-to-live selected-thread authority path before any current-thread polling fallback can shape visible state.

## Deployment Impact

This iteration keeps transport and authority behavior intact and confirms restore continuity. The gate should pass only when healthy selected-thread restore enters explicit restore state, keeps the selected-thread shell and composer mounted, resolves ownership through `session.bootstrap` or append SSE, and shows zero early current-thread `/api/jobs/{id}` or goals authority on the healthy path.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Reopen or reselect a running selected-thread conversation on desktop and phone widths.
5. Confirm restore enters one explicit selected-thread `ATTACH` or `RESUME` state before healthy live ownership resolves.
6. Confirm the selected-thread shell and bottom-fixed composer dock stay mounted throughout restore.
7. Confirm healthy restore resolves through `session.bootstrap` or append SSE with zero early current-thread `/api/jobs/{id}` or goals authority.
8. Confirm degraded timeout, reconnect, or append-stream failure clears restore ownership immediately into the existing downgraded path.
9. Confirm the selected-thread timeline and footer remain targeted to the same conversation through restore.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when healthy selected-thread restore stays on the intended bootstrap-owned path without early current-thread polling authority.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
Iteration 253 deploy gate expectation: the selected-thread footer dock is a single merged session-composer surface, with the session strip carrying the live footer state and the composer owner row remaining hidden as merged state.
Iteration 254 deploy gate expectation: an intentional thread switch preserves one mounted selected-thread workspace with exactly one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and no generic empty-state flash before the incoming snapshot binds.
Iteration 259 deploy gate expectation: healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress remain on one canonical inline session owner, while duplicate active-phase SSE session-event cards are suppressed until degraded or terminal resolution.
Iteration 260 deploy gate expectation: reopening or reselecting a selected thread enters explicit restore state, keeps the selected-thread shell and composer mounted, resolves healthy ownership through `session.bootstrap` or append SSE, and records zero early current-thread `/api/jobs/{id}` or goals authority before degraded fallback is required.
