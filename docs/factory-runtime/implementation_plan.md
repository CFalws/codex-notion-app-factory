# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, pending-turn handoff, live rail, composer, and conversation layout unchanged.
2. Add one authoritative event-to-phase mapping for healthy selected-thread events such as proposal, review, verify, auto-apply, ready, and applied.
3. Render those phases as compact distinct labels and detail text in the existing composer-adjacent live surface instead of generic thinking or done wording.
4. Keep the phase model conversation-local and machine-readable so selected-thread switching clears or replaces it immediately.
5. Extend the focused verifier and docs so future sessions can prove the central session surface derives phase visibility from the intended SSE event path rather than from polling or prose-heavy side panels.
