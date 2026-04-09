# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, transcript-first center pane, phone conversation-first sheet behavior, and existing jump-to-latest affordance unchanged in ownership.
2. Tighten the selected-thread live-follow contract so scrolling away suppresses auto-follow without immediately surfacing the jump affordance until unseen live content actually arrives.
3. Preserve the same selected-thread append-stream and scroll-state inputs so no new transport inference, polling-owned state, or extra status surface is introduced.
4. Let the existing jump-to-latest control and active composer re-engage follow mode while keeping transcript and composer reachability unchanged on desktop and phone widths.
5. Extend the focused verifier and docs so future sessions can prove the transcript stays pinned only while the user is already near the latest append and resumes follow through the intended explicit paths.
