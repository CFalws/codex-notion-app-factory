# Factory Runtime Deploy Plan

## Iteration 265

This deploy plan validates that intentional selected-thread switches preserve one mounted workspace with a compact center placeholder and a continuous composer dock instead of flashing a generic empty or reset state.

## Deployment Impact

This iteration keeps transport and authority behavior intact and records the already-present switch continuity contract. The gate should pass only when an intentional selected-thread switch preserves one compact switching placeholder, keeps the composer dock mounted, clears stale old-thread ownership immediately, and avoids any generic empty-state or reset flash before the incoming thread binds.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least two existing conversations.
4. Open a selected-thread conversation and then intentionally switch to another thread on desktop and phone widths.
5. Confirm the center pane shows exactly one compact switching placeholder sourced from selected-thread state.
6. Confirm the workspace never flashes the generic empty-state view during the switch.
7. Confirm stale old-thread live ownership clears immediately when the switch begins.
8. Confirm the bottom-fixed composer dock remains mounted and targeted through the switch window.
9. Confirm degraded, restore, handoff, and terminal paths still keep their explicit exception-state visibility.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when intentional thread switches preserve one compact placeholder, a mounted composer dock, and zero empty-state flashes.
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
