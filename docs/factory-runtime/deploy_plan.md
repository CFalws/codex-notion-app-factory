# Factory Runtime Deploy Plan

## Deployment Impact

This changes deployed verification only. It keeps the selected-conversation SSE path, transcript follow behavior, footer dock, compact composer state row, and left-rail session markers intact, but adds a selected-thread workspace gate to the deployed console verification path so ordered SSE phase progression must be proven before more UX expansion.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh`.
4. Confirm the selected-thread workspace gate fetches the deployed `/ops/` assets and validates the desktop two-pane shell, phone conversation-first sheet, footer dock, selected-thread-only live markers, and machine-readable transport plus phase datasets.
5. Confirm the gate opens the selected-thread append SSE stream, submits one real `factory-runtime` conversation message, and requires ordered proposal, review, verify, proposal-ready, and terminal progression from the captured SSE append frames and conversation state.
6. Confirm the gate fails on `codex.exec.retrying`, `runtime.exception`, missing selected-thread SSE events, or unexpected session rotation, and does not treat polling-owned progress as acceptable healthy-path evidence.
