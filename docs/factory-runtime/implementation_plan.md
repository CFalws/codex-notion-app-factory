# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, selected-row live-owner contract, composer dock, thread-switch continuity, and non-selected snapshot rows unchanged.
2. Use the existing `liveFollow` state to expose one compact bottom follow control only when the selected transcript is detached from the tail and new selected-thread appends arrive off-screen.
3. Make the control expose explicit `NEW` vs `PAUSED` state plus unseen-count metadata derived from selected-thread append provenance and current scroll position instead of prose-only cues.
4. Clear the control immediately on jump-to-latest, composer re-engagement near the bottom, thread switch, terminal idle, reconnect downgrade, or polling-only fallback so only the healthy selected-thread path reads as actively live.
5. Extend the focused verifier and docs so future sessions can prove the follow control remains selected-thread-only, machine-readable, and clearly distinguishes healthy off-screen appends from degraded or snapshot behavior.
