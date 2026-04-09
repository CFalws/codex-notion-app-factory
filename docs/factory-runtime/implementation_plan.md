# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, transcript-first center pane, phone conversation-first sheet behavior, and footer live rail unchanged.
2. Tighten the left-rail card state vocabulary into a small compact set that distinguishes live, reconnecting, done, failed, and idle states without adding a new state source.
3. Keep one bounded recent preview line visible per conversation card so users can re-enter a thread from the rail without opening it first.
4. Preserve the selected-thread-only live precedence so non-selected threads stay snapshot-only and do not imply cross-thread liveness.
5. Extend the focused verifier and docs so future sessions can prove the rail keeps the bounded preview and compact label contract without reintroducing prose-heavy status behavior or polling-owned primary signals.
