# Factory Runtime Deploy Plan

## Deployment Impact

This iteration changes only the frontend session chrome vocabulary in the existing conversation-first workspace. The bounded expectation is that healthy selected-thread state remains readable from fixed target-first tokens in the center chrome, while degraded and switching states stay explicit through short downgrade copy.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread and visible conversation history.
4. Open an existing selected thread on the healthy attach path and confirm the session summary row, composer owner row, and session strip use fixed tokens instead of sentence-style helper text.
5. Confirm the healthy selected-thread path reads through target, owner, follow, phase, and proposal tokens without reopening the secondary execution-status panel.
6. Submit a message from the fixed composer and confirm handoff and healthy run states read through `SEND`, `FIRST`, `OWNER`, `FOLLOW`, and proposal tokens while the central conversation surface remains authoritative.
7. Force reconnect downgrade or fallback and confirm short degraded tokens such as `RECONNECT` and `DEGRADED` appear without stale healthy ownership text surviving.
8. Confirm intentional thread switch still preserves the mounted shell and composer while the chrome resets to explicit attach vocabulary.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible selected-thread session succeeds through the intended chip-first session chrome contract.
