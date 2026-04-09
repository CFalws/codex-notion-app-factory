# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, desktop transcript-first layout, phone conversation-first sheet behavior, left rail markers, pending-turn handoff, and central timeline unchanged.
2. Extend the deployed console verification entrypoint with a selected-thread workspace gate targeted at `factory-runtime`.
3. Fetch the deployed `/ops/` assets in that gate and assert the browser-visible desktop shell, phone navigation, footer dock, selected-thread-only live markers, and machine-readable transport and phase datasets.
4. Open the selected-thread append SSE stream for one real conversation, submit one bounded `factory-runtime` request, and require ordered proposal, review, verify, proposal-ready, and terminal progression from the captured SSE append frames and conversation state.
5. Fail the gate on degraded signals such as retry fallback, runtime exception, missing selected-thread SSE events, or unexpected session rotation, and extend the focused verifier and docs so future sessions can prove this gate remains wired into the intended path.
