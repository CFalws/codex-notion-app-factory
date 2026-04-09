# AGENTS.md

## Purpose

This repository is a conversation-driven Codex app factory.

The active goal is not only to implement app changes, but to do so in a way that stays:

- sustainable across later sessions
- robust under deployment and self-edit flows
- usable from a phone
- inspectable through durable state and verification artifacts
- faithful to the user's intended outcome even when the request wording is incomplete

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

## Intent Fidelity Rule

The runtime should not treat the user's latest sentence as the whole task.

Before implementation, the agent should form a compact interpretation of:

- the explicit request
- the intended outcome
- the assumptions being made
- the remaining ambiguity
- the user-visible success signal

Reference: `docs/intent-contract.md`

If the request is underspecified, the default behavior is:

1. make the smallest reasonable assumption,
2. record that assumption in durable state,
3. implement toward the interpreted outcome,
4. verify against the likely user-visible success condition.

## UX Friction Rule

Technical correctness is not enough for UI work in this repository.

When a request mentions confusion, discomfort, clutter, discoverability, mobile awkwardness, or any other UX pain:

1. treat it as a real bug, not as a cosmetic preference
2. capture the specific friction signal in durable state when available
3. interpret the likely user journey that is breaking down
4. prefer simplifying the current flow over adding more controls
5. leave behind a structured UX review, not only a code summary

For UI-facing work, the agent should actively look for:

- navigation ambiguity
- hidden state
- too many competing actions
- poor mobile tap flow
- cognitive load from noisy summaries or overly technical language

## Autonomous Goal Loop Rule

Open-ended autonomy is allowed in this repository, but only through explicit goal-loop state and policy checks.

Reference: `docs/autonomy-contract.md`

That means:

- one bounded hypothesis per iteration
- explicit verification after each iteration
- explicit comparison to prior iterations
- explicit continuation, alignment, and safety review
- stop or pause when policy says to stop or pause

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

Passing the surface-level result is not enough.

The agent must also verify that the intended execution path was used.

Examples:

- session continuity should resume the existing Codex thread instead of silently falling back to a new one
- private operator access should arrive through the intended trusted network path instead of a weaker public path
- proposal-mode edits should stay inside proposal worktrees instead of mutating the running checkout directly
- apply should report whether push actually happened instead of treating local-only apply as full success

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

## Degraded Path Rule

The agent must treat fallback or degraded behavior as a first-class verification concern.

Do not report a change as fully successful if any of the following happened without being explicitly expected:

- retry or fallback execution path
- unexpected session rotation
- local-only success after remote push failure
- authentication fallback to a weaker provider
- direct mutation of a lane that should have stayed in proposal mode

If a degraded path occurs:

- record it explicitly
- explain why it happened
- verify whether it is acceptable
- prefer fixing the root cause before closing the task

## Verification Checklist

For runtime, auth, proposal, and deployment work, the agent should explicitly ask:

1. Did the system succeed through the intended path, not only through an eventual fallback?
2. Did any retry, degraded mode, or hidden exception occur?
3. Did state updates match the visible result?
4. Did a new session, new proposal, or new deployment happen only when expected?
5. Did the verification check both positive assertions and negative assertions?

Negative assertions matter in this repository.

Examples:

- `codex.exec.retrying` should not appear during a healthy session resume
- `runtime.exception` should not appear during a completed job
- public ingress should not remain reachable after a tailnet-only transition

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
