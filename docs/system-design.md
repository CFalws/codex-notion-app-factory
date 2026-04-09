# System Design

## Objective

Create a lightweight but stateful execution environment where idea capture, prioritization, implementation, and later maintenance happen in a consistent pipeline.

## Main Components

### 1. Intake surfaces

The system currently uses one intake surface:

- a runtime HTTP API, for direct maintenance requests from a phone-facing web console

It functions as:

- backlog
- project request form
- maintenance console endpoint
- lightweight product brief store

### 2. MCP as the context bridge

MCP provides the mechanism for Codex to read the request source and any connected context directly instead of relying on copy-paste.

That turns the workflow into a real execution environment rather than a manual prompt chain.

### 3. Codex as the builder

Codex is the implementation engine.

Its responsibilities are:

- read the intake request
- infer a build strategy
- generate planning artifacts
- implement code changes
- summarize delivery output

### 4. Codex CLI runtime as the state layer

The persistent Python runtime handles:

- request intake over HTTP
- app lookup through the local registry
- session reuse via persisted Codex thread ids
- launch of `codex exec` or `codex exec resume` in the repository workspace
- background job tracking for phone-originated changes

### 5. Local repository as the durable execution surface

The repository is where the workflow becomes inspectable and maintainable.

Every meaningful request should leave behind:

- generated planning files
- code changes
- operational documentation

## Why This Matters

The value is not merely “used AI to help code.”

The value is that the overall environment was designed so that:

- requests arrive in a structured place
- later requests can continue from the same app lane
- execution happens through a repeatable agent workflow
- outputs are durable and reviewable

That is what makes the environment durable and reviewable.
