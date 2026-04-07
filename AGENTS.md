# AGENTS.md

## Purpose

This repository documents how Codex should operate when a Notion page becomes an app implementation request.

The goal is to make the execution loop consistent and demonstrable:

1. Find a tagged Notion request
2. Read the request in full
3. Extract the implementation brief
4. Produce execution artifacts
5. Implement or update the target app
6. Summarize delivery output

The default quality bar is that the result should be usable from a phone, not only from the development machine.

## Trigger Rules

Codex should treat a Notion page as executable work only when it includes one of these tags:

- `codex-build`
- `codex-spec`
- `codex-review`

## Request Interpretation

When reading a tagged request, Codex should identify:

- project name
- problem being solved
- target user or usage context
- primary device
- constraints
- expected deliverable
- preferred stack if specified

If information is missing, Codex should make the smallest reasonable assumption and proceed.

Default assumptions for personal tools:

- target device is phone first
- delivery target is installable PWA
- deployment target is static hosting unless backend features are required

## Execution Modes

### `codex-spec`

Generate:

- `spec.md`
- `implementation_plan.md`
- `tasks.md`

Do not start coding unless the page explicitly asks for implementation.

### `codex-build`

Generate:

- `spec.md`
- `implementation_plan.md`
- `tasks.md`
- `deploy_plan.md`
- source code changes in the target workspace

Unless the request says otherwise, produce output that can be launched on a phone without the local desktop runtime remaining active.

### `codex-review`

Perform code review against the requested project or diff.

Output should prioritize:

- bugs
- regressions
- missing tests
- implementation risks

## Artifact Expectations

For each request, Codex should try to leave behind durable artifacts that make the work inspectable:

- written spec
- implementation plan
- checklist
- code changes
- deployment notes
- final delivery summary

## Portfolio Principle

This repository is not about maximizing autonomy claims.

It is about showing a real and defensible execution environment:

- Notion for intake
- MCP for context access
- Codex for implementation
- repository artifacts as proof of work
- phone-usable delivery as the default outcome
