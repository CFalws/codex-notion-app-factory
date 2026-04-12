# Factory Runtime Deploy Plan

## Iteration 266

This deploy plan validates that selected-thread proposal and phase visibility remain owned by session-status plus append SSE across healthy and restore paths, with polling visible only as explicit degraded fallback.

## Deployment Impact

This iteration keeps transport and authority behavior intact and records the already-present selected-thread authority contract. The gate should pass only when healthy and restore selected-thread proposal or phase visibility stay session-status plus append-SSE owned, while goals-poll or job-poll state appears only after an explicit degraded fallback boundary is crossed.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation that can enter healthy live progress and one saved thread that can exercise restore.
4. Trigger healthy selected-thread progress and confirm proposal, review, verify, ready, and applied visibility remain on the selected-thread session surface.
5. Reselect or reopen a saved running thread and confirm restore-to-live visibility stays on selected-thread session authority before bootstrap completes.
6. Confirm no early `/api/jobs/{id}` or `/goals` authority shapes the visible selected-thread phase or proposal state on healthy or restore paths.
7. Confirm degraded reconnect or polling fallback still becomes explicit when selected-thread authority is actually lost.
8. Confirm switching, restore, degraded, and terminal paths still preserve their explicit exception-state visibility.
9. Confirm the bottom-fixed composer dock remains continuously usable through healthy, restore, and degraded paths.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when selected-thread proposal and phase visibility remain SSE owned until explicit degraded fallback is required.
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
