# Factory Runtime Implementation Plan

## Iteration 113

Tighten intentional selected-thread switch continuity so the center workspace publishes switching state explicitly instead of resembling generic empty idle.

1. Reuse `selectedThreadWorkspacePlaceholder(...)` as the only null-conversation presentation model for switch, restore, and true empty states.
2. Add explicit workspace summary copy for switching, restore, and true empty modes.
3. Publish the current placeholder mode and conversation id on the thread scroller as well as the conversation timeline.
4. Reset those placeholder datasets immediately when the target conversation attaches.
5. Extend the focused verifier layer and proposal artifacts so iteration 113 proves switching continuity is distinguishable from no-selection idle.
