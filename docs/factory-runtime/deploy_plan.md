# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace render layer only. It keeps the selected-conversation SSE path, deployed workspace gate, composer-adjacent live strip, and non-selected thread rendering intact, but turns the selected-thread center pane into a more unified conversation-first session surface with one inline pending-assistant or live-progress block above the transcript history and the anchored composer below.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Submit a new message in the selected thread and confirm the center pane keeps one conversation-first column with transcript history above the anchored composer.
5. After request acceptance, confirm the inline selected-thread session block appears in the transcript flow for pending assistant state, then advances through the live SSE-owned phase detail without reading like a separate dashboard strip.
6. Confirm the inline session block clears on terminal resolution or thread switch without leaving stale live state in the selected transcript.
7. Confirm transcript plus composer reachability and the existing jump-to-latest behavior do not regress on phone or desktop widths.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the selected-thread SSE proof step still passes without degraded-path signals.
