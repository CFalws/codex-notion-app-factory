# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the deployed workspace verification layer. The bounded expectation is that the deployed gate now proves the selected-thread session surface through actual browser DOM state, not only through static asset inspection plus API and SSE capture.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Ensure a Playwright-capable Python environment with browser binaries is available before running the deployed verifier.
4. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh`.
5. Confirm the browser probe submits through the selected-thread composer, observes a healthy inline live block, forces one bounded downgrade transition, and then observes the inline degraded marker in the selected-thread timeline without stale healthy ownership.
6. Confirm the same probe switches to a second conversation and sees exactly one thread-switch placeholder plus composer switching datasets before the new snapshot attaches.
7. Treat the deployed verifier as failed if the browser runtime cannot prove the intended selected-thread DOM path or if it succeeds only through polling-backed fallback without the expected inline markers.
