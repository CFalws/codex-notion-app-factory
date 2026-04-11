# Factory Runtime Deploy Plan

## Iteration 112

This deploy plan validates the composer utility collapsed-by-default contract and does not introduce new transport, polling behavior, or a second footer status surface.

## Deployment Impact

This iteration changes composer footer utility behavior only. The bounded expectation is that apply and auto-open stay behind one compact utility toggle, expose explicit open or closed datasets and aria state, and close immediately on send or selected-thread transitions without reappearing as live session chrome.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation and one additional conversation for switching.
4. Confirm the composer utility menu is collapsed by default and the textarea plus primary send action remain the dominant footer surface.
5. Open the utility menu and verify the toggle, menu, and utility cluster all report synchronized open state through datasets and aria state.
6. Start a send flow and confirm the utility menu closes immediately without reopening during healthy selected-thread SSE updates.
7. Switch threads, create a new conversation, and change the selected app; confirm the utility menu closes immediately on each transition and does not retain stale open state.
8. Confirm reconnect, polling fallback, restore-only, switch, terminal, and true empty paths do not restyle the utility affordance as live session status.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible composer utility contract succeeds through the intended path.
