# Factory Runtime Deploy Plan

## Iteration 145

This deploy plan validates the phase-specific selected-thread session-chrome contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes selected-thread header and composer-adjacent session-chrome presentation plus verification only. The bounded expectation is that healthy selected-thread SSE progress shows explicit phase labels in the existing chip-first chrome, while degraded and cleared paths still downgrade or remove that phase treatment immediately.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the header chip shows explicit phase progression such as `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`, while the compact copy carries ownership provenance like `SSE OWNER`.
5. Confirm the composer-adjacent live-follow chip reuses the same explicit phase label instead of falling back to generic `LIVE` or `READY`.
6. Trigger reconnect, polling fallback, restore, switching, deselection, and terminal idle and confirm the phase-owned treatment downgrades or clears in the same render pass.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible phase-specific session-chrome contract succeeds through the intended selected-thread session path.
