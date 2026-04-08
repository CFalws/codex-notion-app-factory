# Factory Runtime Implementation Plan

1. Identify where the per-message request title is collected, displayed, and required in the ops console and runtime API.
2. Remove the request-title input from the static console and send conversation messages with body text only.
3. Normalize title-less requests on the server so older clients still work and proposal mode keeps a usable internal label.
4. Refresh the app documentation and delivery notes to describe the conversation-first flow.
5. Verify the proposal branch contains one coherent, GitHub Pages-safe change set.
