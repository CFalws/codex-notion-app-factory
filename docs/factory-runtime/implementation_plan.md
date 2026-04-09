# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, deployed workspace gate, transcript-first center pane, phone conversation-first sheet behavior, and footer live rail placement unchanged.
2. Tighten the transport-health contract in the live rail so connecting, live, reconnecting, and offline states are explicit and compact.
3. Preserve the same selected-thread appendStream and live-run inputs so no new transport inference, polling-owned state, or extra status source is introduced.
4. Keep transcript and composer reachability unchanged on desktop and phone widths while making degraded stream state obvious in the same conversation-first surface.
5. Extend the focused verifier and docs so future sessions can prove the footer rail distinguishes healthy selected-thread SSE from degraded transport without drifting into prose-heavy operator status.
