# Codex CLI Runtime

This repository now supports a persistent Python runtime that shells out to the local Codex CLI instead of calling the OpenAI API directly.

## Goal

The GitHub Pages site remains the phone-facing web surface.

The Python runtime is the stateful execution layer behind it:

- receive a maintenance request over HTTP
- resolve the target app from the local registry
- reuse the stored session id for that app
- run the change through `codex exec` or `codex exec resume`
- persist the Codex thread id back into the app registry
- preserve app memory and job state for later follow-up work

## Runtime Components

- `pyproject.toml`
  Declares the runtime dependencies.
- `src/codex_factory_runtime/main.py`
  FastAPI application with request and job endpoints.
- `src/codex_factory_runtime/agent_runtime.py`
  Builds prompts and runs Codex through the local CLI.
- `src/codex_factory_runtime/state.py`
  Reads and writes app records, request files, and runtime job status.
- `scripts/run_codex_agents_api.py`
  Local entry point for the API server.

## Important Environment Variables

- `CODEX_COMMAND`
  Defaults to `codex`.
- `CODEX_HOME`
  Optional override. Leave unset to reuse the local `~/.codex` login and thread state.
- `CODEX_PROFILE`
  Optional Codex profile name.
- `CODEX_MODEL`
  Optional Codex model override.
- `CODEX_ARGS_JSON`
  Optional JSON array of extra arguments inserted before `exec`.
- `CODEX_FACTORY_PORT`
  API port. Defaults to `8787`.
- `CODEX_FACTORY_CORS_ALLOWED_ORIGINS`
  Optional JSON array or comma-separated list of allowed frontend origins.

## Example

```bash
cd /Users/emil/emil/python/codex-notion-app-factory
python -m venv .venv
source .venv/bin/activate
pip install -e .

export CODEX_COMMAND="codex"

python scripts/run_codex_agents_api.py
```

The web console can then submit requests to `http://<server>:8787/api/requests`.

The runtime assumes the local machine already has a working Codex login or profile under the default Codex home. No OpenAI API key is required for the runtime itself.

## Deployment Split

- backend runtime:
  runs on a VPS or always-on machine
- frontend console:
  stays under `examples/generated_apps/` and is published to GitHub Pages on push

This keeps the operator UI phone-usable while preserving a stateful server-side session layer.
