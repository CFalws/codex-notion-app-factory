# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, composer dock, thread-switch continuity, selected-row live-owner contract, and non-selected snapshot rows unchanged.
- [x] Expose one compact bottom follow control only when the selected transcript is detached from the tail and unseen selected-thread appends are present.
- [x] Make the control publish explicit `NEW` vs `PAUSED` state plus unseen-count metadata derived from selected-thread append provenance and live-follow state.
- [x] Clear the control immediately on jump-to-latest, thread switch, terminal idle, reconnect downgrade, and polling-only fallback.
- [x] Extend focused verification so future sessions can prove the follow control remains selected-thread-only and distinguishes healthy live off-screen appends from degraded follow state.
