# Factory Runtime Deploy Plan

## Iteration 252

This deploy plan validates that healthy selected-thread success is proven through the same session-status plus append-SSE path the workspace already uses, without falling back to job polling in the deployed verifier.

## Deployment Impact

This iteration keeps transport and authority behavior intact and tightens the deployed proof path. The gate should pass only when the selected-thread conversation reaches `proposal.ready` through SSE-owned phase progression, while degraded events, unexpected session rotation, and job-poll-owned success remain explicit failures.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and trigger healthy SSE-owned progress, reconnect downgrade, polling fallback, terminal resolution, and a switch or restore path on desktop and phone widths.
5. Confirm the selected-thread workspace still shows healthy phase progression, timeline ownership, and composer ownership through session-status plus append SSE with zero selected-thread `/api/jobs/{id}` fetches on the browser-visible path.
6. Confirm reconnect downgrade and polling fallback remain explicit and machine-readable rather than being hidden by job polling.
7. Confirm the transcript inline session block remains the only in-timeline live progress surface.
8. Confirm the unified header capsule, footer dock, and left-rail cues remain coherent on the same selected-thread authority path.
9. Confirm `proposal.ready` is the deployed terminal proof point, while `codex.exec.retrying`, `runtime.exception`, job failure, or unexpected session rotation remain explicit failures.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread workspace remains conversation-first, single-owner, and the deployed verifier itself no longer depends on job polling for healthy success.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
