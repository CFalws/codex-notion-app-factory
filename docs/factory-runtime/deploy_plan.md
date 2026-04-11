# Factory Runtime Deploy Plan

## Iteration 203

This deploy plan validates the fixed composer strip as the canonical healthy selected-thread session bar.

## Deployment Impact

This iteration keeps transport unchanged while shifting healthy selected-thread ownership chrome to the fixed composer surface. The healthy path should show owner, phase, and active run state there, while header and rail ownership chrome stay suppressed or cleared until authority is lost.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start from a healthy selected-thread conversation with internal append SSE enabled and drive the session through `PROPOSAL`, `REVIEW`, `VERIFY`, `AUTO APPLY`, `READY`, and `APPLIED`.
5. Confirm the fixed composer strip stays visible and exposes compact `SSE OWNER`, phase, and live-run state chips for the selected thread on the healthy path.
6. Confirm healthy header summary and healthy active-session rail ownership cues stay suppressed or cleared so the composer is the single authoritative session bar.
7. Confirm reconnect downgrade, polling fallback, switch, deselection, restore-gap loss, and terminal completion downgrade or clear the composer bar and related session chrome in the same transition frame.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy path passes only when the composer strip is authoritative and stale owner residue does not remain elsewhere.
