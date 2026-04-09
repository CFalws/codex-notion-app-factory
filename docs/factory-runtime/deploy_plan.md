# Factory Runtime Deploy Plan

## Deployment Impact

This changes the GitHub Pages operator workspace only. It adds an inline active-session progress row on top of the existing selected-conversation live workspace state. Broader polling, transport, and proposal behavior stay unchanged.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open one active conversation and confirm the inline run row appears only for that selected thread.
4. Trigger a request and confirm the row moves through compact states such as `thinking`, `running tool`, `waiting`, and `done` without needing the inspector panel.
5. Verify the row's machine-readable state attributes change alongside live conversation events and that healthy live appends still carry SSE provenance.
6. Switch conversations and confirm the prior run row state clears with the old thread instead of leaking into the new selection.
