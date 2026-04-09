# AGENTS.md

## Purpose

This repository is a conversation-driven Codex app factory.

The active goal is not only to implement app changes, but to do so in a way that stays:

- sustainable across later sessions
- robust under deployment and self-edit flows
- usable from a phone
- inspectable through durable state and verification artifacts

## Operating Model

The normal loop is:

1. open or continue an app-scoped conversation
2. read the current app record, workspace, and memory
3. make the smallest reasonable change
4. preserve the existing app lane unless a reset is explicitly required
5. write back durable state, summaries, and proposal metadata when needed
6. verify before commit and again before deployment when the change is risky

## Current Request Entry Points

Requests can enter through:

- the runtime HTTP API
- the phone-facing `codex-ops-console`
- direct maintenance work inside this repository

When a request comes through the runtime API, Codex should assume conversation continuity matters and preserve the same app lane whenever possible.

## Runtime Modes

### Standard App Lane

Used for normal app maintenance such as `habit-tracker-pwa`.

Rules:

- continue from the existing app workspace
- preserve app session continuity
- keep the app phone-usable by default
- update memory and summaries after completion

### Proposal Lane

Used for self-editing the app factory itself such as `factory-runtime`.

Rules:

- work must happen in a proposal worktree
- do not change the running checkout directly during execution
- proposal work must end in a commit on the proposal branch
- apply must remain explicit and reviewable
- apply may restart the runtime and push to GitHub

## Change Boundary Rule

Before editing code, decide which module owns the behavior.

Reference: `docs/change-boundaries.md`

If a change crosses more than one boundary, prefer moving logic into the owning module instead of adding more coupling to the caller.

## State Contract Rule

Runtime changes must preserve the file-backed state contract unless the change explicitly migrates it.

Reference: `docs/state-contract.md`

This applies to:

- app registry records
- requests
- jobs
- proposals
- conversations
- engineering log entries

## Verification Rule

Do not treat a change as done until the required verification gate passes.

Reference: `docs/verification-gates.md`

Minimum expectations:

- low-risk change: `make verify-static`
- medium-risk change: `make verify`
- high-risk runtime or deployment change: `make verify` plus deployed runtime verification

## High-Risk Changes

The following always count as high-risk:

- runtime API behavior
- authentication
- proposal creation or apply flow
- self-edit behavior
- Git push after apply
- deployment scripts
- service worker behavior
- app-factory state schema changes

## Artifact Expectations

Each meaningful change should leave behind durable evidence:

- code changes
- updated docs when contracts or operations change
- decision summary and engineering log entries from runtime work
- verification evidence before commit and deployment

## Default Quality Bar

The result should be understandable by a future session with less context.

That means:

- explicit boundaries
- explicit state contracts
- repeatable verification steps
- deploy paths that do not rely on memory alone
