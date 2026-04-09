# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, transcript-first desktop layout, phone conversation-first sheet behavior, left rail markers, pending-turn handoff, and central timeline unchanged.
- [x] Extend the deployed console verification entrypoint with a selected-thread workspace gate targeted at `factory-runtime`.
- [x] Assert the deployed browser-visible desktop shell, phone navigation, footer dock, selected-thread-only live markers, and machine-readable transport and phase datasets from that gate.
- [x] Open the selected-thread append SSE stream for one real conversation and require ordered proposal, review, verify, proposal-ready, and terminal progression from the captured SSE frames and conversation state.
- [x] Fail on degraded signals such as retry fallback, runtime exception, missing selected-thread SSE events, or unexpected session rotation, and keep focused verification wired to the new gate.
