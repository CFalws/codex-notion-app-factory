# Factory Runtime Deploy Plan

## Iteration 180

This deploy plan validates the healthy selected-thread transcript rail as the only readable session summary surface.

## Deployment Impact

This iteration keeps transport and healthy live ownership unchanged while turning the existing transcript rail into the sole healthy-path readable session summary and demoting header and footer mirrors to fallback-only roles.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with at least one selected-thread conversation.
4. Open a healthy selected-thread conversation with internal append SSE enabled and confirm the transcript live rail shows the readable session chips for selected scope, SSE owner, phase, path, verifier, blocker, and milestone progression.
5. Confirm the healthy header summary row and healthy footer strip are hidden or neutralized on that authoritative path, and the side-panel facts do not become a competing healthy summary surface.
6. Confirm reconnect downgrade, polling fallback, restore-gap, deselection, switch, and terminal completion immediately hide or neutralize the healthy transcript rail and return authority to explicit degraded or fallback surfaces.
7. Confirm non-selected threads and no-selection idle do not leave stale transcript-owned session continuity behind.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the browser-visible healthy selected-thread path shows one authoritative transcript rail while header and footer mirrors stay suppressed and degraded or ambiguous paths clear it immediately.
