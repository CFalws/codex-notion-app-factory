# Factory Runtime Deploy Plan

## Iteration 268

This deploy plan validates that healthy selected-thread drill-down already lives on one canonical timeline card while secondary autonomy and execution detail remain reserved for exception paths.

## Deployment Impact

This iteration keeps transport and authority behavior intact and records the already-present canonical drill-down contract. The gate should pass only when the healthy selected-thread timeline card remains the sole visible live drill-down surface, while degraded, restore, handoff, switching, and exception paths still preserve explicit secondary-detail visibility.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread that can enter healthy live progress and separate paths that can exercise restore, switch, handoff, and degraded fallback.
4. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh`.
5. Confirm the healthy selected-thread path exposes phase, milestones, path verdict, verifier, blocker, and session metadata directly on the canonical timeline card.
6. Confirm the same healthy path keeps the autonomy and execution detail cards suppressed instead of requiring the secondary panel.
7. Confirm degraded, restore, handoff, switching, and exception paths still re-enable explicit secondary autonomy or execution visibility when the timeline is no longer the sole healthy owner.
8. Confirm no early `/api/jobs/{id}` or `/goals` authority is needed to shape healthy selected-thread drill-down.
9. Confirm the bottom-fixed composer dock remains continuously usable through healthy and exception paths.
10. Treat the proposal as ready only after the deployed verifier passes and the runtime contract check is rerun in an environment with the missing dependencies.
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
Iteration 268 deploy gate expectation: the healthy selected-thread timeline card already serves as the sole visible live drill-down surface in this branch, while autonomy and execution detail remain suppressed on that healthy path and explicit secondary-detail visibility returns only on degraded, restore, handoff, switching, and exception paths.
