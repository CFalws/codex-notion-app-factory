# Factory Runtime Deploy Plan

## Iteration 259

This deploy plan validates that healthy selected-thread phase progression stays on one canonical in-timeline live owner rather than fragmenting into duplicate active-phase live surfaces.

## Deployment Impact

This iteration keeps transport and authority behavior intact and confirms center-timeline convergence. The gate should pass only when healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress remain on one canonical inline session owner, while duplicate active-phase SSE session-event cards stay suppressed until degraded or terminal resolution.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned proposal, review, verify, auto-apply, ready, and applied progress on desktop and phone widths.
5. Confirm healthy selected-thread progress remains on exactly one canonical inline session owner in the timeline.
6. Confirm duplicate active-phase SSE session-event cards do not render while that live owner is present.
7. Confirm degraded reconnect or polling fallback clears live-owned treatment immediately.
8. Confirm terminal resolution still allows the final outcome to remain inspectable after healthy progress finishes.
9. Confirm the bottom-fixed composer dock and selected-thread shell remain unchanged through the healthy path.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when healthy selected-thread progress stays on one canonical in-timeline owner with duplicate active-phase session-event cards suppressed.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
Iteration 253 deploy gate expectation: the selected-thread footer dock is a single merged session-composer surface, with the session strip carrying the live footer state and the composer owner row remaining hidden as merged state.
Iteration 254 deploy gate expectation: an intentional thread switch preserves one mounted selected-thread workspace with exactly one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and no generic empty-state flash before the incoming snapshot binds.
Iteration 259 deploy gate expectation: healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress remain on one canonical inline session owner, while duplicate active-phase SSE session-event cards are suppressed until degraded or terminal resolution.
