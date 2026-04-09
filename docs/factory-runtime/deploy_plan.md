# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, header phase chip, composer-adjacent live strip, transcript-tail live activity turn, and non-selected thread rendering intact, but tightens the selected-thread submit handoff so the conversation shows one temporary pending outbound turn and then one temporary assistant placeholder until the first real assistant SSE append arrives.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Submit a new message in the selected thread and confirm the transcript shows exactly one temporary outbound user turn immediately near the composer.
5. After request acceptance, confirm that temporary user turn is replaced by exactly one temporary assistant placeholder until the first real assistant SSE append arrives.
6. Confirm the synthetic handoff turns clear on first real assistant append, terminal resolution, idle reset, or thread switch without leaving duplicate or stale placeholders behind.
7. Confirm transcript plus composer reachability and the existing jump-to-latest behavior do not regress on phone or desktop widths.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the existing selected-thread SSE proof step still passes without degraded-path signals.
