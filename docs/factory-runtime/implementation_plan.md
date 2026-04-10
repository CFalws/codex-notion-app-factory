# Factory Runtime Implementation Plan

1. Keep the current selected-thread SSE path, conversation shell, transcript-tail live block, footer dock, recent-thread rail, and side-panel behavior unchanged.
2. Reuse existing live-follow and selected-thread ownership state to scope the bottom follow affordance to the current healthy SSE-owned thread only.
3. Tighten the visibility rule so the follow control appears only when the operator is detached from the tail and unseen live appends actually exist.
4. Preserve explicit NEW versus PAUSED state mapping and unseen-count datasets while clearing the control immediately on jump-to-latest, thread switch, reconnect downgrade, polling fallback, or terminal completion.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the detached-tail follow affordance contract.
