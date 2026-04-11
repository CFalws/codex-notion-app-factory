# Factory Runtime Implementation Plan

## Iteration 155

Collapse the selected-thread header into a conversation-first identity surface with one live phase badge.

1. Reuse the existing selected-thread session ownership, transport, phase, and timeline-authority models to drive `#thread-phase-chip` as the only compact live badge in the center header.
2. Remove the standalone selected-thread session-summary row from the conversation header markup and DOM bindings.
3. Keep the title row identity-first so the selected-thread title stays primary and the badge remains secondary chrome.
4. Mirror healthy, degraded, switching, restore, and idle selected-thread states through the single header badge without introducing new state or transport sources.
5. Extend focused static and deployed verification so desktop and phone layouts fail if the old summary strip reappears or if stale ownership survives on the badge during degraded or switching paths.
6. Align proposal artifacts with the iteration-155 single-badge header contract.
