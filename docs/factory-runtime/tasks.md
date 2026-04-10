# Factory Runtime Tasks

- [x] Keep the current selected-thread SSE path, conversation shell, transcript-tail live block, footer dock, recent-thread rail, and side-panel behavior unchanged.
- [x] Reuse existing live-follow and selected-thread ownership state to scope the bottom follow affordance to the current healthy SSE-owned thread only.
- [x] Tighten the visibility rule so the follow control appears only when the operator is detached from the tail and unseen live appends actually exist.
- [x] Preserve explicit NEW versus PAUSED state mapping and unseen-count datasets while clearing the control immediately on jump-to-latest, thread switch, reconnect downgrade, polling fallback, or terminal completion.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the detached-tail follow affordance contract.
