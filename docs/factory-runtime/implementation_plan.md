# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, desktop shell, and selected-thread live rendering unchanged.
2. Tighten the phone nav sheet so the conversation list remains the first actionable surface and app or operator controls stay behind a collapsed secondary section.
3. Reuse the existing nav open and close path, but return focus to the selected conversation surface when the drawer closes or a thread or app is chosen.
4. Preserve transcript plus composer reachability and selected-thread ownership on desktop and phone widths.
5. Extend the focused verifier and docs so future sessions can prove the intended conversation-drawer contract instead of inferring it from incidental layout behavior.
