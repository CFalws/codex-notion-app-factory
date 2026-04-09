# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, navigation structure, composer-adjacent activity bar, and footer composer unchanged.
2. Add transcript-local follow state so the selected conversation stays pinned to the newest append while the user is already near the bottom.
3. Stop forced scrolling when the user scrolls upward and expose one compact jump-to-latest control that restores the newest append and follow mode.
4. Clear the affordance on thread switch, empty or terminal reset, and when the user returns to the bottom.
5. Extend the focused verifier and docs so future sessions can prove live progress stays bound to the existing append SSE path without adding more status chrome.
