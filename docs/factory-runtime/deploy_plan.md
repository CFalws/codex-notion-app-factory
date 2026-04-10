# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the sticky left-rail active-session row plus verification layers. The bounded expectation is that the rail row now mirrors the same healthy selected-thread SSE owner, phase, and follow or unseen state as the selected conversation workspace, while degraded states remain explicitly non-owned.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Start a healthy selected-thread SSE-owned run and confirm the sticky active-session row shows `OWNER`, the same current phase as the selected conversation workspace, and a `LIVE`, `PAUSED`, or `NEW` follow chip from the same authority.
5. Confirm the rail row clears healthy-owned treatment immediately on reconnect downgrade, polling fallback, idle, terminal resolution, or thread switch.
6. Confirm non-selected thread chips remain snapshot-only and do not inherit the active session’s live phase.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible rail row mirrors the same healthy selected-thread authority as the center workspace instead of polling or snapshot-only labels.
