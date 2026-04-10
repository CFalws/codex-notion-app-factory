# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on compact footer utility ergonomics. The bounded expectation is that the utility cluster stays collapsed by default, the textarea and send button remain primary, and secondary apply or auto-open controls stay reachable through one explicit utility affordance without changing live-session behavior.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the footer utility cluster is collapsed by default and exposes explicit open or closed state through the existing workspace markers.
5. Confirm the textarea and primary send action remain visually dominant on desktop and phone widths.
6. Confirm apply and auto-open remain reachable only after intentionally opening the compact utility cluster.
7. Confirm the footer does not expand into a second form row or introduce a second live-status surface when the utility cluster is opened.
8. Confirm transcript history, selected-thread live strip, and composer access remain continuously available while the utility cluster opens and closes.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the compact footer utility proof still passes without degraded-path signals.
