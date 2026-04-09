# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, desktop transcript-first layout, phone conversation-first sheet behavior, left rail markers, pending-turn handoff, and central timeline unchanged.
2. Re-center the active header on the selected conversation instead of the selected app.
3. Render one compact selected-thread phase badge in the header from the existing selected-thread live state and keep it machine-readable.
4. Demote app-level identity and explanatory copy out of the center-pane reading path while leaving richer detail in the sidebar and secondary panel.
5. Extend the focused verifier and docs so future sessions can prove the active header stays conversation-first and does not reintroduce app-centric header chrome or a second status path.
