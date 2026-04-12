# Factory Runtime Deploy Plan

## Iteration 229

This deploy plan validates selected-thread submit-to-first-append handoff continuity in the deployed workspace gate.

## Deployment Impact

This iteration keeps runtime behavior unchanged and records the intended handoff path. The gate should pass only when selected-thread submit immediately enters one explicit handoff owner state, avoids duplicate pending surfaces, replaces handoff cleanly with the first real assistant SSE append, and clears handoff ownership immediately on fallback or switch.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a selected-thread conversation and submit a new request through the bottom-fixed composer.
5. Confirm the center conversation shell and composer stay mounted and immediately show one explicit handoff owner.
6. Confirm the workspace renders either exactly one pending outbound user turn or exactly one temporary assistant placeholder, never both at the same time.
7. Confirm the composer-adjacent handoff state matches the same selected-thread handoff stage without becoming a second live owner.
8. Confirm the first real assistant SSE append replaces the temporary handoff state cleanly.
9. Confirm reconnect downgrade, polling fallback, terminal failure, idle reset, and intentional thread switch clear the handoff owner immediately.
10. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible path passes only when the selected-thread handoff path remains SSE-scoped, single-owner, and free of duplicate or stale placeholders.
