# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It improves sidebar thread clarity by adding preview-rich conversation cards and bounded state labels while keeping the existing selected-conversation SSE path, transcript follow behavior, desktop secondary panel, phone footer dock, and composer-adjacent live rail intact.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the console and confirm each conversation card shows a single-line recent preview without widening the sidebar or breaking phone-width scrolling.
4. Verify the selected thread shows `ACTIVE` plus the existing SSE-derived live label when it is running, reconnecting, or done.
5. Verify non-selected threads show only snapshot-derived `DONE` or `IDLE` labels and do not claim live progress from any new source.
6. On phone width, open the conversation-first nav sheet and confirm the richer cards remain readable and tap-safe.
7. Confirm the composer-adjacent live rail remains the only visible in-pane live-status surface inside the conversation pane.
