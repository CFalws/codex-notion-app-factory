# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, footer composer, transcript follow behavior, and navigation structure unchanged.
2. Define an explicit conversation-local collapse rule for the live rail: expanded for sending, thinking, running, connecting, and reconnecting states; collapsible only for idle and terminal states.
3. Preserve the latest meaningful run outcome in a one-line collapsed summary instead of hiding the rail entirely.
4. Add one in-rail toggle so the user can re-expand terminal or idle detail without opening another panel.
5. Extend the focused verifier and docs so future sessions can prove the rail stays conversation-local, keeps terminal visibility, and does not introduce a new status source.
