# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on the selected-thread submit-to-first-append handoff. The bounded expectation is that the selected conversation exposes exactly one pending outbound user turn before acceptance, exactly one temporary assistant placeholder after acceptance, and one matching composer-adjacent handoff bar without duplicate accepted-status blocks.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Submit one message in the selected conversation and confirm the transcript shows exactly one pending outbound user turn before acceptance.
5. After acceptance, confirm the transcript clears that user placeholder and shows exactly one temporary assistant placeholder instead of a second accepted-status block.
6. Confirm the composer-adjacent activity bar matches the same selected-thread handoff stage and does not diverge from the transcript placeholder.
7. Confirm first assistant append, terminal failure, idle reset, polling-only fallback, and thread switch each clear the temporary assistant placeholder immediately.
8. Confirm no state ever shows both pending-user and pending-assistant surfaces at once, and no duplicate accepted-status block reappears in the transcript.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread handoff proof still passes without degraded-path signals or duplicate pending surfaces.
