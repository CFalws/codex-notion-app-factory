# Factory Runtime Implementation Plan

## Iteration 110

Project healthy selected-thread SSE phase progression into one compact in-timeline session event lane without changing transport or adding a new polling path.

1. Reuse the existing selected-thread phase progression, milestone, and live-autonomy helpers instead of creating a second transcript model.
2. Render exactly one healthy selected-thread live session item in the transcript with milestone datasets attached.
3. Keep the existing session-event collapse guard so healthy SSE authority events do not append duplicate transcript cards beside that item.
4. Clear or downgrade the transcript lane immediately when the selected thread is no longer healthy SSE-owned.
5. Extend the focused verifier layer and proposal artifacts so the healthy path proves in-timeline milestone ownership while degraded paths prove immediate fallback visibility.
