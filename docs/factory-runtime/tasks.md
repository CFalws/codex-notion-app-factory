# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript shell, footer composer dock, and side-panel behavior unchanged.
- [x] Reuse the existing selected-thread handoff, live-follow, append-stream, and thread-transition state instead of introducing another session source.
- [x] Add one compact active-session row above the conversation list that mirrors selected-thread owner, phase, follow or unseen state, and switching status.
- [x] Clear the active-session row immediately on true idle, terminal resolution, reconnect downgrade, polling fallback, or thread switch so stale ownership never survives.
- [x] Keep the focused verifier and iteration artifacts aligned with the sticky active-session row contract.
