# Factory Runtime Deploy Plan

## Iteration 129

This deploy plan validates the selected-thread shell-phase vocabulary contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread shell-phase derivation and presentation only. The bounded expectation is that healthy selected-thread SSE surfaces present one shared authoritative phase vocabulary, while degraded reconnect, polling fallback, switch, and deselection paths clear or downgrade that phase treatment immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one healthy selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the left rail, header summary dataset, and footer strip all show the same authoritative phase label for `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm those shell surfaces do not keep generic `LIVE`, `READY`, or `ACTIVE` labels once a more specific authoritative SSE phase is available.
6. Trigger switching, reconnect downgrade, polling fallback, deselection, and terminal resolution and confirm the shell phase label clears or downgrades in the same render cycle without stale healthy-phase ownership.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible shell-phase contract succeeds through the intended path.
