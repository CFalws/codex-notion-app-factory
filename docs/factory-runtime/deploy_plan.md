# Factory Runtime Deploy Plan

## Iteration 171

This deploy plan validates selected-thread switch and attach continuity in the center pane.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while making switch and restore or attach boundaries use one compact transcript-bound transition item instead of splitting into different center-pane placeholder treatments.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a selected-thread switch and confirm the center workspace keeps the shell and fixed composer visible while showing exactly one compact transcript-bound transition item.
5. Reload into a saved selected-thread resume or attach path and confirm restore uses that same compact transition item shape instead of a separate live-activity placeholder card.
6. Confirm stale old-thread ownership clears immediately while the transition item is active.
7. Confirm reconnect downgrade, polling fallback, deselection, terminal completion, and true no-selection idle still fail closed correctly and only true idle shows the generic empty state.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible switch or attach boundary uses one compact transition item sourced from the selected-thread datasets without flashing the generic empty view.
