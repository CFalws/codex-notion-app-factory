# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, session strip ownership, bottom follow control, footer composer, and non-selected snapshot rows unchanged.
- [x] Add one compact composer target row that names the selected thread and shows `READY`, `SWITCHING`, or `HANDOFF`.
- [x] Reuse existing selected-thread ownership state instead of inventing a second composer-only source of truth.
- [x] Disable send only while selected-thread attach is unresolved.
- [x] Clear stale old-thread target ownership immediately on thread switch and degrade reconnect or polling fallback back to non-live `READY`.
- [x] Align focused verification and iteration artifacts with the composer target ownership contract.
