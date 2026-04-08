# Codex Notion App Factory

A stateful Codex app implementation environment that supports both MCP-connected Notion intake and a runtime HTTP control surface.

The current target is not only "working code." The target is personal apps that are actually usable from a phone without your laptop staying awake.

## Problem

Most personal app ideas die before implementation because idea capture, scoping, coding, and later maintenance happen in disconnected tools.

I wanted a workflow where I could capture a request in Notion, or send one from a phone-friendly control console, and let an agent-driven build loop turn it into planning artifacts and real code.

That solved the build problem, but a second problem remained: many generated tools still depended on a local desktop runtime. This repository now treats that as a design bug.

## What I Built

I designed an execution environment where:

- Notion can act as the intake queue
- a runtime HTTP API can also accept follow-up maintenance requests
- MCP acts as the context bridge for tool access
- Codex acts as the implementation agent
- local repositories store the generated artifacts and code changes
- the default delivery target is an installable mobile-first PWA unless the request clearly requires native APIs
- app-specific session state is stored so later requests can continue from the same lane

The result is a repeatable loop from request capture to implemented app and mobile-ready deployment output.

The next layer on top of that loop is stateful maintenance: each app should keep its own workspace and durable session record so later changes can continue from context instead of restarting cold.

## Core Claim

This repository is designed to support one clear portfolio message:

**I built an agent execution environment where tagged requests can enter through Notion or a runtime control console, Codex executes through MCP-connected tooling, and personal-use apps are implemented with phone-usable delivery as the default.**

This is not a chatbot demo. It is an operating model for turning idea capture into implemented software that can actually be launched on a phone.

## What The System Does

1. I capture a new request in Notion or send it through the runtime console
2. The request is resolved to a new app or an existing app lane
3. Codex loads the app session record and memory when available
4. Codex extracts the brief, constraints, and expected output
5. Codex chooses the smallest delivery target that is actually usable on my phone
6. Codex implements the app directly in the local workspace
7. Codex writes back implementation artifacts, state updates, and deployment notes

## Key Capabilities

- tagged request intake from Notion
- runtime HTTP intake for phone-triggered maintenance
- explicit request contract and execution rules
- generated intermediate artifacts such as brief, spec, plan, and tasks
- mobile-first scaffolding for installable PWAs
- local sample apps produced from those requests
- validation artifacts that make the output inspectable
- app-specific workspace and session state management
- GitHub Pages deployment for the phone-facing static surfaces

## Why This Is Stronger Than A Standard “Agent App”

The important point is not just model usage. The important point is the workflow design:

- Notion and the runtime console are used as operational intake layers
- Codex is used as the execution engine
- MCP is used as the bridge between request management and implementation
- the system is optimized for building real personal-use tools, not generic chat interactions
- output is judged by deployability and accessibility, not only by local correctness

This creates a durable app-building loop rather than a one-off automation.

## Architecture

### Intake Layer

Notion pages and the runtime HTTP API are used as structured implementation requests.

Each request contains:

- app name
- problem statement
- target users
- primary device
- constraints
- desired stack
- delivery expectations

### Trigger Layer

A request becomes executable either when a predefined tag is added in Notion or when the runtime API receives an app-scoped maintenance request.

Recommended tags:

- `codex-build`
- `codex-review`
- `codex-spec`

### Execution Layer

Codex reads tagged requests through the Notion MCP connection or receives a runtime request from the API layer, then performs one of the following:

- generate a spec
- generate an implementation plan
- implement the app directly
- review an existing codebase change

### Delivery Layer

Codex should prefer these delivery targets in order:

1. installable PWA on static hosting
2. PWA plus optional serverless API
3. wrapped web app using Capacitor only if native packaging is required
4. fully native stack only when device APIs or store distribution demands it

### Runtime Layer

The persistent runtime uses:

- FastAPI for request intake
- `X-API-Key` request authentication for `/api/*`
- the local Codex CLI for session-backed execution
- persisted Codex thread ids for app-specific conversation continuity
- app registry and memory files for durable state outside the model context window

### Artifact Layer

Each request produces concrete outputs in the local repository:

- source code
- generated specs
- implementation notes
- task checklists
- deployment notes
- changelog or delivery summary

## Tech Stack

- Codex as the coding agent
- local Codex CLI as the persistent runtime layer
- MCP-connected Notion integration
- Markdown-based execution artifacts
- installable PWA scaffolds for phone-first delivery
- Python utilities used for local generation, preview, and runtime orchestration

## Repository Structure

- `AGENTS.md`
  Execution rules for how Codex should interpret tagged Notion requests.
- `docs/system-design.md`
  High-level architecture and reasoning behind the workflow.
- `docs/mobile-first-operating-model.md`
  Delivery rules for apps that must be usable on a phone.
- `docs/github-pages-automation.md`
  Explains how generated apps are assembled and deployed to GitHub Pages.
- `docs/notion-request-contract.md`
  Defines the structure of a valid Notion app request.
- `docs/agents-sdk-runtime.md`
  Explains the Python runtime that accepts maintenance requests and reuses app sessions through the local Codex CLI.
- `docs/operating-model.md`
  Describes the end-to-end execution loop from request to implemented app.
- `src/codex_factory_runtime/`
  Python API server and agent runtime built on FastAPI plus the local Codex CLI.
- `scripts/run_codex_agents_api.py`
  Launches the runtime API that accepts maintenance requests over HTTP.
- `scripts/scaffold_mobile_pwa.py`
  Generates a phone-ready PWA scaffold from an idea statement.
- `scripts/manage_app_sessions.py`
  Creates app-specific workspaces, stores session ids, and records maintenance requests.
- `.github/workflows/deploy-generated-apps-pages.yml`
  Publishes all generated apps to a single GitHub Pages site.
- `scripts/build_pages_site.py`
  Assembles generated app outputs into a Pages-ready static bundle.
- `state/`
  Durable registry, memory, and request history for existing apps.
- `workspaces/`
  Dedicated app-specific workspaces used for stateful maintenance.
- `templates/notion_app_request.md`
  A reusable request template for Notion pages.
- `examples/generated_apps/sample-focus-launcher/`
  Example artifacts showing what a single intake request can produce.
- `examples/generated_apps/habit-tracker-pwa/`
  Example output generated for a mobile habit tracker.
- `examples/generated_apps/codex-ops-console/`
  Phone-first operator console that stores the runtime URL and API key locally, submits requests to the runtime server, polls jobs, and opens the target app after completion.

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
- a delivery target that can be launched from a phone

## Real Execution Proof

This repository includes real session-backed examples and a mobile-first scaffold:

- a real Notion request page was created
- that page was fetched back through MCP
- the fetched content was persisted locally
- a working sample app called `Momentum Timer` was implemented from that request
- validation artifacts were saved
- a mobile habit tracker scaffold can be generated into an installable PWA shell
- a phone-facing operator console can submit follow-up requests to the runtime

See `REAL_EXECUTION_SHOWCASE.md` for the full path.

## My Implementation Scope

I designed the workflow, request contract, execution rules, example artifacts, and the sample generated apps included in this repository.

This is not a mock architecture document. It is a working portfolio repository showing how I structure agent-led product implementation.

## Portfolio Framing

This repository is best presented as:

> Built a Codex-based agent execution environment where requests could enter through Notion or a phone-friendly runtime console, MCP handled workspace-context retrieval, and implementation requests were converted into real app specs, deployable PWAs, stateful maintenance sessions, and code changes for personal-use software projects.

## Publishing Note

If I were pinning one repository to represent my agent-driven workflow, this would still be the first one, but now with a stronger claim: the workflow does not stop at implementation. It drives toward use.

## Why This Version Is Honest

This repository reflects the workflow I actually use:

- I capture requests in Notion or send maintenance requests through the runtime console
- I use Codex as the implementation agent
- I rely on MCP-connected tools for context retrieval
- I use the environment to build real personal apps for myself
- I care whether those apps can be launched comfortably from my phone

That is a stronger and more credible portfolio story than claiming a generic autonomous framework that I do not actually use.
