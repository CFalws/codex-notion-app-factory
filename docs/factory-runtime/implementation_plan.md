# Factory Runtime Implementation Plan

1. Identify the existing runtime URL entry points in the Codex Ops Console UI and request flow.
2. Replace free-form backend URL handling with a fixed runtime base URL constant.
3. Update the UI copy so the fixed runtime is visible but not required as editable operator input.
4. Refresh the local app documentation to reflect the new behavior.
5. Verify that the static app still initializes, loads apps automatically, and remains proposal-ready.
