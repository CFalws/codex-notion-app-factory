# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the selected conversation transcript now carries a single inline tail session block for pending handoff or healthy SSE-owned progress, so live execution reads like part of the conversation stream instead of surrounding chrome.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation attached through the internal append SSE path.
4. Send a message and confirm the selected transcript shows exactly one compact HANDOFF block at the tail while awaiting the first assistant append.
5. Confirm the block becomes a LIVE transcript-tail block only while the selected thread remains healthy and SSE-owned, and that it stays inside the conversation stream rather than moving into a secondary panel.
6. Confirm the block clears immediately on the first real assistant append, terminal completion, reconnect downgrade, polling fallback, or thread switch, without giving any non-selected thread a live-owned inline block.
7. Confirm transcript history and composer access remain dominant and reachable on phone widths while the inline block appears and clears.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread inline transcript-tail proof passes without stale ownership on degraded or terminal paths.
