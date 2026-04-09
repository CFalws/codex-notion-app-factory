# Change Boundaries

This repository should stay flexible by keeping volatile logic inside small modules with clear ownership.

## Runtime Boundary Map

- `src/codex_factory_runtime/api_app.py`
  App assembly only. Creates the FastAPI app, wires middleware, and registers routes.
- `src/codex_factory_runtime/api_routes.py`
  HTTP contract only. Defines request/response routes and delegates runtime work.
- `src/codex_factory_runtime/api_runtime_context.py`
  Request orchestration only. Owns conversation events, request enqueueing, and API-facing runtime flow.
- `src/codex_factory_runtime/agent_runtime.py`
  Job orchestration only. Coordinates Codex execution, decision summary handling, proposal finalization, and apply flow.
- `src/codex_factory_runtime/runtime_cli.py`
  Codex and git subprocess I/O only.
- `src/codex_factory_runtime/runtime_proposals.py`
  Proposal worktree, merge, restart, and push behavior only.
- `src/codex_factory_runtime/runtime_engineering.py`
  Prompt construction and engineering-log parsing/normalization only.
- `src/codex_factory_runtime/state.py`
  Persistent state layout and file-backed state mutations only.

## Frontend Boundary Map

- `examples/generated_apps/codex-ops-console/web/app.js`
  UI entrypoint only. Wires controllers and user interactions.
- `examples/generated_apps/codex-ops-console/web/ops-conversations.js`
  App selection and conversation continuity only.
- `examples/generated_apps/codex-ops-console/web/ops-jobs.js`
  Job polling and proposal readiness only.
- `examples/generated_apps/codex-ops-console/web/ops-api.js`
  Runtime URL and HTTP request behavior only.
- `examples/generated_apps/codex-ops-console/web/ops-render.js`
  DOM rendering only.
- `examples/generated_apps/codex-ops-console/web/ops-store.js`
  Local UI state and persistence only.

## Refactoring Rule

When a change touches more than one boundary, stop and decide which module should own the behavior before editing code.

## Verification Rule

After moving behavior across boundaries, run:

```bash
make verify
```

For runtime, proposal, auth, deployment, or operator-console behavior changes, also run:

```bash
API_KEY=<runtime-api-key> make verify-deployed
```
