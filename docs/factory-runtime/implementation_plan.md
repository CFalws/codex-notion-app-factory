# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, left rail, collapsed secondary panel, and mobile drawer unchanged.
2. Move the selected-thread live status surface fully into the composer region so it reads as one activity bar rather than a separate footer-layer strip.
3. Reuse the existing session-strip state and draft-status surface instead of introducing any new transport or duplicated polling path.
4. Clear the unified activity bar on idle, terminal completion, and thread switch using the same selected-conversation state rules already in place.
5. Extend the focused verifier and docs so future sessions can prove the activity bar lives directly adjacent to the composer and remains the only foreground live-status surface in that region.
