# Factory Runtime Deploy Plan

## Iteration 254

This deploy plan validates that intentional thread switches preserve one mounted selected-thread workspace rather than flashing a generic empty-state reset.

## Deployment Impact

This iteration keeps transport and authority behavior intact and confirms switch continuity. The gate should pass only when an intentional thread switch preserves the selected-thread shell and bottom-fixed composer dock, renders exactly one compact transition placeholder, and never falls back to a generic empty state while the incoming snapshot is attaching.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and an intentional thread switch or restore path on desktop and phone widths.
5. Confirm an intentional thread switch never drops the selected workspace to a generic empty state.
6. Confirm exactly one compact switching placeholder remains visible until the incoming snapshot binds.
7. Confirm the bottom-fixed composer dock stays mounted through the switch on desktop and phone widths.
8. Confirm stale `LIVE`, `READY`, or polling-owned cues from the old thread clear immediately during the switch.
9. Confirm the transcript inline session block remains the only in-timeline live progress surface once the new thread binds and that no duplicate transition or footer live surfaces survive.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first through the switch with no empty-state flash.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
Iteration 253 deploy gate expectation: the selected-thread footer dock is a single merged session-composer surface, with the session strip carrying the live footer state and the composer owner row remaining hidden as merged state.
Iteration 254 deploy gate expectation: an intentional thread switch preserves one mounted selected-thread workspace with exactly one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and no generic empty-state flash before the incoming snapshot binds.
