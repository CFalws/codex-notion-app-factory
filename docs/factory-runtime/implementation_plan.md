# Factory Runtime Implementation Plan

1. Keep the current selected-conversation SSE path, live rail, composer, and conversation content structure unchanged.
2. Make the phone-width navigation affordance explicitly control a drawer or sheet rather than reading like always-present top chrome.
3. Preserve one explicit action for thread switching while keeping app-level operator controls behind the existing collapsed mobile section.
4. Mark the active conversation shell as the primary mobile workspace surface and keep that state verifier-visible.
5. Extend the focused verifier and docs so future sessions can prove phone widths land on the conversation workspace rather than falling back to the old stacked navigation-first structure.
