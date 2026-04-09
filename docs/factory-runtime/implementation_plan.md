# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, sidebar layout, composer rail, and mobile navigation structure unchanged.
2. Add one bounded recent-preview line to each conversation card using only existing conversation snapshot data from the conversation list payload.
3. Keep the selected-thread card driven by the existing session presentation datasets so active, running, reconnecting, and done states stay tied to the current SSE-backed thread only.
4. Show a compact bounded state label on every card so active, running, done, and idle threads are easier to distinguish without opening them.
5. Extend the focused verifier and docs so future sessions can prove sidebar clarity improved without adding a new live transport or polling path.
