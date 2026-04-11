# Factory Runtime Implementation Plan

## Iteration 112

Collapse the composer utility controls into one closed-by-default utility affordance without changing selected-thread session authority or footer layout.

1. Reuse `setComposerUtilityOpen(...)` as the only source of truth for utility open or closed datasets, hidden state, and aria state.
2. Keep the utility controls collapsed by default in markup and on init.
3. Close the utility affordance on send start, app changes, new conversation creation, and selected-thread changes.
4. Keep the utility affordance independent from healthy SSE ownership and degraded transport markers so it never reads like session-status chrome.
5. Extend the focused verifier layer and proposal artifacts so iteration 112 proves collapsed-by-default behavior and close-on-transition wiring.
