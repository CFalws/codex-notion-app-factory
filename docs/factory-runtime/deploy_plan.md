# Factory Runtime Deploy Plan

## Deployment Impact

This iteration stays inside the GitHub Pages operator workspace presentation and verification layers. The bounded expectation is that the selected-thread inline phase item now has explicit terminal retention semantics for `READY` and `APPLIED` instead of ambiguous immediate-clear or stale-linger behavior.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with an active selected conversation.
4. Trigger a healthy selected-thread SSE session that reaches `READY` or `APPLIED` and confirm the transcript tail keeps exactly one inline live phase item briefly visible.
5. Confirm the retained item remains selected-thread-owned, SSE-scoped, and machine-readable while visible.
6. Confirm the item clears immediately on the next append, thread switch, reconnect downgrade, polling fallback, or ownership loss.
7. Confirm non-selected threads and degraded paths never retain a healthy terminal phase item.
8. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the terminal-retention contract passes without stale healthy ownership on degraded or switched-thread paths.
