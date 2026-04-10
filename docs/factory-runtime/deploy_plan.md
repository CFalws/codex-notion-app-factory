# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside selected-thread SSE session authority, render derivation, and verification layers. The bounded expectation is that healthy selected-thread proposal, review, verify, ready, and applied progression now comes from the same append-driven live session authority as the transcript instead of depending on polling-backed or snapshot-only job identity.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Start a healthy selected-thread SSE-owned run and confirm the header summary row, transcript live activity, composer owner row, and composer-adjacent strip all move through PROPOSAL, REVIEW, VERIFY, AUTO APPLY, READY, and APPLIED progression from the same live session stream.
5. Confirm the visible phase progression does not require a hidden polling refresh or delayed snapshot-backed `latest_job_id` update to appear on the healthy path.
6. Trigger reconnect or polling fallback and confirm the header, transcript, and composer surfaces drop back to degraded non-owned labels instead of pretending the session is still healthy-live.
7. Switch intentionally to another thread and confirm phase-specific healthy labels clear with the ownership handoff instead of leaking into the new selection.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible workspace proves exact healthy selected-thread phase progression through the same append-driven session authority as the transcript.
