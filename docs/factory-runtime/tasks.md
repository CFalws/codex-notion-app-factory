# Factory Runtime Tasks

- [x] Reuse the existing selected-thread session and thread-transition datasets for the sticky active-session row.
- [x] Keep the row visible for healthy selected-thread `OWNER` plus phase and `LIVE` or `NEW` or `PAUSED` state without making non-selected rows live-owned.
- [x] Add one non-owned `SWITCHING` row state that retargets immediately to the latest pending conversation during intentional switches.
- [x] Clear the row immediately on reconnect downgrade, polling fallback, terminal idle, and true no-conversation idle.
- [x] Align focused browser-proof verifiers and iteration artifacts with the bounded active-session-row continuity contract.
