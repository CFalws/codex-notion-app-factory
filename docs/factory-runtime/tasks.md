# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer dock, sticky active-session row, and side-panel behavior unchanged.
- [x] Add one compact selected-thread live-session ownership chip to the header summary row and drive it strictly from healthy SSE ownership or explicit degraded-path signals.
- [x] Reuse app `session_id` data from the existing app list payload to detect unexpected selected-app session rotation without adding new runtime routes.
- [x] Downgrade or clear the header indicator immediately on reconnect retry, polling fallback, thread switch, or terminal completion so stale live-owned UI never remains in the workspace.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the header live-session indicator contract.
