# Factory Runtime Deploy Plan

## Iteration 267

This deploy plan validates that one deployed browser scenario matrix already proves selected-thread realtime ownership across healthy streaming, restore or resume, degraded fallback, intentional switch, and cancelled-switch paths.

## Deployment Impact

This iteration keeps transport and authority behavior intact and records the already-present deployed scenario-matrix contract. The gate should pass only when the browser verifier proves selected-thread healthy, restore, degraded, and switch behavior through the intended SSE-owned path and explicit degraded fallback, not through silent polling-owned recovery or hidden resets.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with conversations available for healthy streaming, restore or resume, intentional switching, and degraded fallback.
4. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh`.
5. Confirm the deployed browser verifier exercises healthy selected-thread streaming and accepts success only when selected-thread live ownership remains SSE authoritative end to end.
6. Confirm the same run exercises restore or resume and rejects any early `/api/jobs/{id}` or `/goals` authority before explicit fallback is required.
7. Confirm the same run exercises intentional switch and cancelled-switch continuity with one compact placeholder, a mounted composer dock, and zero generic empty-state flashes.
8. Confirm the same run exercises degraded fallback and accepts success only when reconnect or polling is made explicit rather than silently treated as healthy ownership.
9. Confirm stale old-thread ownership, hidden degraded recovery, and polling-owned success all remain negative assertions inside the browser gate.
10. Treat the proposal as ready only after that deployed scenario matrix passes and the runtime contract check is rerun in an environment with the missing dependencies.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
Iteration 253 deploy gate expectation: the selected-thread footer dock is a single merged session-composer surface, with the session strip carrying the live footer state and the composer owner row remaining hidden as merged state.
Iteration 254 deploy gate expectation: an intentional thread switch preserves one mounted selected-thread workspace with exactly one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and no generic empty-state flash before the incoming snapshot binds.
Iteration 259 deploy gate expectation: healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress remain on one canonical inline session owner, while duplicate active-phase SSE session-event cards are suppressed until degraded or terminal resolution.
Iteration 260 deploy gate expectation: reopening or reselecting a selected thread enters explicit restore state, keeps the selected-thread shell and composer mounted, resolves healthy ownership through `session.bootstrap` or append SSE, and records zero early current-thread `/api/jobs/{id}` or goals authority before degraded fallback is required.
Iteration 262 deploy gate expectation: the healthy selected-thread SSE-owned path suppresses duplicate composer-adjacent strip chrome so the center timeline remains the sole visible live session owner, while degraded, restore, handoff, terminal, and follow-only exception paths retain explicit strip visibility.
Iteration 265 deploy gate expectation: intentional selected-thread switches already preserve one mounted selected-thread workspace with one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and explicit negative assertions against generic empty-state or reset flashes.
Iteration 266 deploy gate expectation: healthy and restore selected-thread proposal and phase visibility already remain session-status plus append-SSE owned in this branch, while job-poll and goals-poll authority remain absent until an explicit degraded fallback boundary is crossed.
Iteration 267 deploy gate expectation: the deployed browser verifier already covers healthy, restore, degraded, switch, and cancelled-switch selected-thread scenarios together and accepts success only when the selected-thread session stays authoritative through the intended path without silent polling-owned recovery, stale ownership, or empty-state flashes.
