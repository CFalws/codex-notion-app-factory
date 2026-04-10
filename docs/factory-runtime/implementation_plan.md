# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, transcript shell, footer composer dock, sticky active-session row, and side-panel behavior unchanged.
2. Add one compact selected-thread live-session ownership chip to the header summary row and drive it strictly from healthy SSE ownership or explicit degraded-path signals.
3. Reuse app `session_id` data from the existing app list payload to detect unexpected selected-app session rotation without adding new runtime routes.
4. Downgrade or clear the header indicator immediately on reconnect retry, polling fallback, thread switch, or terminal completion so stale live-owned UI never remains in the workspace.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the header live-session indicator contract.
