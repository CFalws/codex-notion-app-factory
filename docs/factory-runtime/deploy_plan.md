# Factory Runtime Deploy Plan

## Iteration 253

This deploy plan validates that the selected-thread footer dock uses one canonical session-composer bar rather than a visible owner row plus a second session strip.

## Deployment Impact

This iteration keeps transport and authority behavior intact and tightens footer presentation. The gate should pass only when the selected-thread footer dock remains one merged session-composer surface across healthy and degraded states, while switching and restore remain explicit replacement states and the old owner row stays hidden as merged state.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and a switch or restore path on desktop and phone widths.
5. Confirm the selected-thread footer dock stays visible as one merged session-composer bar on desktop and phone widths.
6. Confirm the strip itself carries target, transport, phase, proposal readiness, and follow cues for healthy selected-thread runs without a second visible owner row.
7. Confirm reconnect downgrade, polling fallback, handoff, restore, switching, and idle states all remain explicit in that same bottom surface.
8. Confirm the transcript inline session block remains the only in-timeline live progress surface and the header and left rail remain coherent on the same selected-thread authority path.
9. Confirm the old composer owner row stays hidden when merged and no stale `READY` or duplicate footer live surface survives degraded or switched ownership loss.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first and the footer dock is a single canonical merged session-composer bar.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
Iteration 253 deploy gate expectation: the selected-thread footer dock is a single merged session-composer surface, with the session strip carrying the live footer state and the composer owner row remaining hidden as merged state.
