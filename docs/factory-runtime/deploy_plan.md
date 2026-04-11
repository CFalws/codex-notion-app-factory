# Factory Runtime Deploy Plan

## Iteration 124

This deploy plan validates the healthy selected-thread live-surface composition contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes render composition only. The bounded expectation is that healthy selected-thread SSE appends continue to own the same live state, but rich phase detail now lives only in the transcript item while the footer stays compact and degraded paths remain explicit.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm proposal, review, verify, ready, auto-apply, and applied progression appear through one transcript live activity item.
5. Confirm the footer session bar stays compact on that healthy path, exposes only one chip plus minimal ownership or follow detail, and does not repeat milestone or verifier or blocker detail.
6. Trigger reconnect or polling fallback and confirm the transcript live item downgrades explicitly in the same render cycle while the compact fallback indicators remain accurate.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread live-surface composition contract succeeds through the intended path.
