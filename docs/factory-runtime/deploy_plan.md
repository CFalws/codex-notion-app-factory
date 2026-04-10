# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the selected-thread switch continuity and verification layers. The bounded expectation is that intentional thread switches keep the center workspace shell and bottom-fixed composer mounted, show one compact switch placeholder, and never fall through to the generic empty workspace.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a healthy selected-thread live session.
4. Select one active conversation, then switch intentionally to a second conversation and confirm the center pane stays mounted with exactly one compact switch placeholder instead of the generic empty workspace.
5. Confirm the bottom-fixed composer remains attached to the same shell during the switch and exposes switching ownership state for the target thread.
6. Confirm the old thread's healthy live or degraded ownership markers clear immediately when the switch placeholder takes over, and that reconnect or polling fallback is not mislabeled as healthy continuity.
7. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread switch continuity contract passes through the intended browser path.
