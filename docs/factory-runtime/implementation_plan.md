# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, desktop secondary panel, and phone footer dock unchanged.
2. Reuse the existing left rail instead of adding a new status panel or transport source.
3. Add compact selected-thread and live-state markers directly to conversation cards using the existing session-strip and thread-scroller datasets.
4. Clear those markers automatically when the selected session returns to idle or when selection changes.
5. Extend the focused verifier and docs so future sessions can prove the left rail exposes the current active or generating thread without introducing duplicate status surfaces.
