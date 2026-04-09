# Factory Runtime Implementation Plan

1. Keep the current desktop layout hierarchy unchanged.
2. On narrow screens, make the active conversation pane render first and move the existing sidebar controls behind a one-tap drawer or sheet.
3. Reuse the current sidebar content instead of inventing new mobile-only navigation data or transport.
4. Preserve the autonomy rail, live run row, append stream strip, and composer as conversation-local surfaces in the main pane.
5. Extend the static verifier and docs so future sessions can prove the mobile drawer exists and the active conversation remains the first visible workspace surface.
