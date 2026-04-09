# Factory Runtime Implementation Plan

1. Keep the current conversation-first shell, mobile drawer, and selected-conversation SSE path unchanged.
2. Move the existing session strip into the same footer dock as the composer so phone-width interaction reads as one persistent conversation-local action region.
3. Reuse the current session-strip state handling instead of introducing new transport or polling-derived behavior.
4. Make the footer dock sticky on phone widths while keeping desktop layout unchanged and preserving machine-readable strip markers for browser verification.
5. Extend the focused verifier and docs so future sessions can prove the footer dock contains both live state and composer without reintroducing competing status surfaces.
