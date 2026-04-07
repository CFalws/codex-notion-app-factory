# Codex Notion App Factory

A Codex-driven app implementation environment that uses MCP-connected Notion as the intake queue.

For the fastest inspection path, start with `REAL_EXECUTION_SHOWCASE.md`.

## Problem

Most personal app ideas die before implementation because idea capture, scoping, and coding happen in disconnected tools.

I wanted a workflow where I could capture a request in Notion, mark it as executable, and let an agent-driven build loop turn it into planning artifacts and real code.

## What I Built

I designed an execution environment where:

- Notion acts as the intake queue
- MCP acts as the context bridge
- Codex acts as the implementation agent
- local repositories store the generated artifacts and code changes

The result is a repeatable loop from request capture to implemented app.

## Core Claim

This repository is designed to support one clear portfolio message:

**I built an agent execution environment where Notion acts as the request queue, Codex scans tagged requests through MCP, and then directly implements personal-use apps from those requests.**

This is not a chatbot demo. It is an operating model for turning idea capture into implemented software.

## What The System Does

1. I write an app request in Notion
2. I mark the request with a specific implementation tag
3. Codex scans the tagged request through the Notion MCP connection
4. Codex extracts the brief, constraints, and expected output
5. Codex implements the app directly in the local workspace
6. Codex writes back implementation artifacts such as specs, plans, or status notes

## Key Capabilities

- tagged request intake from Notion
- explicit request contract and execution rules
- generated intermediate artifacts such as brief, spec, plan, and tasks
- local sample apps produced from those requests
- validation artifacts that make the output inspectable

## Why This Is Stronger Than A Standard “Agent App”

The important point is not just model usage. The important point is the workflow design:

- Notion is used as the operational intake layer
- Codex is used as the execution engine
- MCP is used as the bridge between request management and implementation
- The system is optimized for building real personal-use tools, not generic chat interactions

This creates a durable app-building loop rather than a one-off automation.

## Architecture

### Intake Layer

Notion pages are used as structured implementation requests.

Each request contains:

- app name
- problem statement
- target users
- constraints
- desired stack
- delivery expectations

### Trigger Layer

A request becomes executable when a predefined tag is added in Notion.

Recommended tags:

- `codex-build`
- `codex-review`
- `codex-spec`

### Execution Layer

Codex scans tagged requests through the Notion MCP connection, reads the request page, and performs one of the following:

- generate a spec
- generate an implementation plan
- implement the app directly
- review an existing codebase change

### Artifact Layer

Each request produces concrete outputs in the local repository:

- source code
- generated specs
- implementation notes
- task checklists
- changelog or delivery summary

## Tech Stack

- Codex as the coding agent
- MCP-connected Notion integration
- Markdown-based execution artifacts
- Python sample apps used as concrete generated outputs

## Repository Structure

- `AGENTS.md`
  Execution rules for how Codex should interpret tagged Notion requests.
- `docs/system-design.md`
  High-level architecture and reasoning behind the workflow.
- `docs/notion-request-contract.md`
  Defines the structure of a valid Notion app request.
- `docs/operating-model.md`
  Describes the end-to-end execution loop from request to implemented app.
- `templates/notion_app_request.md`
  A reusable request template for Notion pages.
- `examples/generated_apps/sample-focus-launcher/`
  Example artifacts showing what a single intake request can produce.

## Example Workflow

### Notion Request

A page is created in Notion using the request template and marked with `codex-build`.

### Codex Execution

Codex reads the tagged page through MCP, extracts the brief, and creates or updates the local app workspace.

### Result

The system produces:

- an implementation-oriented spec
- a build plan
- a task breakdown
- actual code changes in the target repository

## Real Execution Proof

This repository includes a real session-backed example:

- a real Notion request page was created
- that page was fetched back through MCP
- the fetched content was persisted locally
- a working sample app called `Momentum Timer` was implemented from that request
- validation artifacts were saved

See `REAL_EXECUTION_SHOWCASE.md` for the full path.

## My Implementation Scope

I designed the workflow, request contract, execution rules, example artifacts, and the sample generated apps included in this repository.

This is not a mock architecture document. It is a working portfolio repository showing how I structure agent-led product implementation.

## Portfolio Framing

This repository is best presented as:

> Built a Codex-based agent execution environment where Notion served as the intake queue, MCP handled workspace-context retrieval, and tagged implementation requests were converted into real app specs, plans, and code changes for personal-use software projects.

## Publishing Note

If I were pinning one repository to represent my agent-driven workflow, this would be the first one.

## Why This Version Is Honest

This repository reflects the workflow I actually use:

- I capture requests in Notion
- I use Codex as the implementation agent
- I rely on MCP-connected tools for context retrieval
- I use the environment to build real personal apps for myself

That is a stronger and more credible portfolio story than claiming a generic autonomous framework that I do not actually use.
