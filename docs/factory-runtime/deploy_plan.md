# Factory Runtime Deploy Plan

## Iteration 151

This deploy plan validates the center-pane inline selected-thread session-block contract and does not introduce a new transport or backend protocol.

## Deployment Impact

This iteration changes center-pane selected-thread inline-session presentation and verification only. The bounded expectation is that the conversation workspace shows one compact inline selected-thread session block for healthy SSE-owned live progress or pending assistant handoff, and clears it immediately on degraded or lost-authority paths.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Start a healthy selected-thread SSE run and confirm the conversation pane shows exactly one compact inline session block with `SSE OWNER`, the selected-thread phase, and matching path, verifier, and blocker chips.
5. Trigger a bounded pending assistant handoff and confirm the same inline block flips to `HANDOFF` while the pending assistant placeholder is suppressed.
6. Trigger reconnect downgrade, polling fallback, terminal idle, deselection, and thread switch and confirm the inline block clears immediately instead of preserving stale selected-thread ownership.
7. Confirm no non-selected thread shows an inline live-owned session block.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible inline-session contract succeeds through the intended selected-thread session path.
