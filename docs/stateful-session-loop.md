# Stateful Session Loop

## Objective

Keep one durable work context per app so later changes can continue from the same session instead of starting from zero.

## Core Idea

This repository should treat each maintained app as its own product lane.

Each app gets:

- a stable `app_id`
- a dedicated workspace path
- a persisted session record
- a rolling memory snapshot
- a request history

## Directory Model

Tracked structure:

- `state/registry/apps/<app_id>.json`
- `state/memory/<app_id>.md`
- `state/requests/<app_id>/`
- `workspaces/<app_id>/`

Runtime-only structure:

- `state/runtime/`

`state/runtime/` now has a concrete role:

- `codex-home/` stores Codex thread state and runtime-local CLI data
- `jobs/` stores runtime execution status for API-triggered runs

## Why This Matters

If a mobile request says "change the habit button copy," the system should not behave like a brand-new greenfield task.

Instead it should:

1. resolve the request to an existing `app_id`
2. load the workspace path
3. load the latest session id if one exists
4. load the latest memory snapshot
5. continue from that state when possible

When the runtime API is active, that continuation path is no longer only a design goal. The API will:

1. accept the new request over HTTP
2. look up the app record
3. reuse the stored `session_id`
4. run the agent with a persistent SQLite session
5. record the new request and job status back into state files

## Session Strategy

### First choice

Reuse the stored session id for the app.

In the current implementation this session id is the Codex thread id returned by `codex exec --json`, so later requests can continue through `codex exec resume`.

### Fallback

If the old session cannot be resumed, rebuild context from:

- app workspace
- last summary
- recent request history
- latest commit
- deployment URL

This repository should always store enough context to do the fallback cleanly.

## Minimal App Record

Each app record should store:

- `app_id`
- `title`
- `workspace_path`
- `source_path`
- `platform`
- `delivery_type`
- `status`
- `session_id`
- `deployment_url`
- `latest_commit`
- `last_summary`
- `aliases`
- timestamps

The runtime also stores per-job records with:

- `job_id`
- `app_id`
- `request_id`
- `status`
- timestamps
- `result_summary`
- `error`

## Request Handling

Every change request should be recorded against the app workspace.

Recommended lifecycle:

1. `pending`
2. `in_progress`
3. `completed`
4. `archived`

## Operational Rule

When a request targets an existing app, Codex should load the app record first and prefer continuation over a fresh start.

This repository still keeps a fallback path through registry and memory files, but the preferred path is now:

- registry lookup
- session reuse
- runtime execution
- memory and job update
