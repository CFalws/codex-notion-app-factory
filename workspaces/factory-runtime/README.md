# Factory Runtime Workspace

This workspace anchors the self-edit lane for the Codex runtime repository.

- app_id: `factory-runtime`
- source_path: `.`
- execution_mode: `proposal`

Requests for this lane should:

- run in a dedicated git worktree
- create a proposal branch
- produce a commit and diff summary
- be applied only through the proposal apply API
