# Factory Runtime Deploy Plan

## Iteration 262

This deploy plan validates that healthy selected-thread live ownership remains visible only in the center conversation timeline while the composer-adjacent strip is reserved for exception paths.

## Deployment Impact

This iteration keeps transport and authority behavior intact and narrows healthy footer presentation. The gate should pass only when the healthy selected-thread SSE-owned path keeps the timeline as the sole visible live session owner, suppresses duplicate healthy strip state beside the composer, and still preserves explicit strip visibility for degraded, restore, handoff, terminal, or follow-only exception paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation on desktop and phone widths and trigger SSE-owned live progress.
5. Confirm the center timeline remains the sole visible healthy live session owner.
6. Confirm the composer-adjacent strip is hidden or reduced to follow-only behavior on the healthy path and no duplicate healthy strip state is visible.
7. Confirm degraded, restore, handoff, or terminal paths still show explicit strip state near the composer.
8. Confirm no early `/api/jobs/{id}` or goals polling authority is needed to shape healthy selected-thread visibility.
9. Confirm the bottom-fixed composer dock remains continuously usable through healthy and degraded paths.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when healthy selected-thread strip chrome is suppressed and the timeline remains the canonical live owner.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
Iteration 253 deploy gate expectation: the selected-thread footer dock is a single merged session-composer surface, with the session strip carrying the live footer state and the composer owner row remaining hidden as merged state.
Iteration 254 deploy gate expectation: an intentional thread switch preserves one mounted selected-thread workspace with exactly one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and no generic empty-state flash before the incoming snapshot binds.
Iteration 259 deploy gate expectation: healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress remain on one canonical inline session owner, while duplicate active-phase SSE session-event cards are suppressed until degraded or terminal resolution.
Iteration 260 deploy gate expectation: reopening or reselecting a selected thread enters explicit restore state, keeps the selected-thread shell and composer mounted, resolves healthy ownership through `session.bootstrap` or append SSE, and records zero early current-thread `/api/jobs/{id}` or goals authority before degraded fallback is required.
Iteration 262 deploy gate expectation: the healthy selected-thread SSE-owned path suppresses duplicate composer-adjacent strip chrome so the center timeline remains the sole visible live session owner, while degraded, restore, handoff, terminal, and follow-only exception paths retain explicit strip visibility.
