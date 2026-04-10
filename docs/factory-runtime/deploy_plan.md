# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, rail behavior, and center-pane live surface intact, but turns the bottom transcript follow affordance into an explicit selected-thread `NEW` or `PAUSED` control with unseen-count metadata.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Scroll upward inside the selected conversation until tail-following pauses, then confirm the bottom follow control stays hidden until unseen output actually arrives.
5. Submit a new message in the selected thread and confirm off-screen healthy SSE appends flip the bottom control to `NEW`, while degraded detached state uses `PAUSED` instead of implying healthy live ownership.
6. Confirm tapping the bottom follow control or focusing the composer clears it immediately and restores tail-following.
7. Confirm non-selected rows remain snapshot-only, transcript plus composer reachability do not regress on phone or desktop widths, and reconnect or polling fallback does not surface as healthy `NEW`.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals or non-selected live leakage.
