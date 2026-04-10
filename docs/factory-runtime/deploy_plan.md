# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the left-rail ownership presentation and verification layers. The bounded expectation is that the rail shows one healthy selected-session mirror only while the selected thread is the active SSE owner, and that the mirror clears immediately on degraded or no-longer-live paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Confirm the selected-thread header shows `SSE OWNER` and the left rail shows exactly one matching active-session mirror with no extra rail-only phase language.
5. Trigger reconnect or polling fallback and confirm the header downgrades while the left-rail mirror disappears immediately instead of lingering as a stale owner.
6. Switch intentionally to another thread and confirm the left-rail mirror clears on the same transition that removes old selected-thread ownership from the center workspace.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm header, transcript, composer, and left rail all agree on one canonical ownership source through the intended browser path.
