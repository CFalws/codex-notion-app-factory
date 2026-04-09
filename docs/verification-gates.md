# Verification Gates

This repository should not treat an agent-generated code change as deployable only because the code looks reasonable.

The required standard is stronger:

1. the code must parse
2. the runtime contract must still hold
3. risky changes must be exercised against a deployed runtime before they are pushed live
4. the system must succeed through the intended path, not only through a fallback that happened to work

## Risk Levels

### Low Risk

Examples:

- copy changes
- documentation updates
- styling-only changes
- non-behavioral refactors

Required gate:

- `make verify-static`

### Medium Risk

Examples:

- operator console state changes
- API response shaping
- conversation rendering changes
- request intake changes that do not touch proposal apply or deployment behavior
- UX signal capture or UX review rendering changes

Required gates:

- `make verify-static`
- `make verify-contract`

### High Risk

Examples:

- runtime API changes
- proposal creation or apply flow
- self-edit behavior
- Git push after apply
- deployment scripts
- authentication or service worker behavior

Required gates:

- `make verify-static`
- `make verify-contract`
- `make verify-deployed` against the target runtime

## What Each Gate Proves

Verification in this repository has two kinds of assertions:

- positive assertions
  - something expected must happen
- negative assertions
  - something degraded or unintended must not happen

Both matter. A completed job is not enough if it completed through the wrong path.

### `make verify-static`

Fast local sanity checks.

It proves:

- Python files still compile
- JavaScript files used by the operator console still parse

It does not prove:

- runtime behavior
- background task wiring
- proposal lifecycle
- deployed environment behavior

### `make verify-contract`

Local runtime contract check using `FastAPI TestClient` and a simulated runtime execution layer.

It proves:

- API key enforcement still works
- apps can be listed
- conversations can be created
- conversation messages create jobs
- interpreted intent is persisted onto request, job, and conversation message state
- job completion updates the conversation timeline
- proposal-mode apps still emit proposals
- proposal apply still updates conversation state
- engineering-log entries are still written
- resume command construction preserves the intended session-resume path
- autonomous goals can continue to a new bounded iteration after recoverable review or verification rejection

It does not prove:

- real Codex CLI execution
- GitHub push credentials
- deployed browser behavior

### `make verify-deployed`

Smoke test against the actual deployed runtime.

It proves:

- the deployed runtime is healthy
- API authentication works in production
- a real conversation message can execute end to end
- the conversation timeline updates in the deployed environment
- degraded execution signals such as unexpected session-resume fallback can be detected

It should be run before a risky production deployment and after deployment if the change touched runtime or operator-console behavior.

## Degraded Path Checks

For high-risk runtime and deployment changes, verification should explicitly look for degraded paths.

Examples:

- `codex.exec.retrying`
  - acceptable only when the task explicitly expected a resume failure
- `runtime.exception`
  - should fail verification even if the UI later recovered
- unexpected new `thread_id`
  - should fail session continuity verification unless rotation was intended
- local-only apply after push failure
  - should not be reported as a full deployment success

The rule is simple:

`eventual success` is weaker than `correct success`.

For the autonomous goal loop, also distinguish:

- a degraded iteration that should continue with a different bounded hypothesis
- a goal-level pause or stop

When an autonomous iteration records a structured intended-path verdict, verification should assert both:

- the healthy path records `verdict=expected`
- the degraded path records the concrete degraded signals instead of looking like normal success

When autonomous verifier reviews are present, verification should also assert that:

- healthy iterations record `path_acceptability=acceptable`
- degraded iterations record `path_acceptability=disqualifying`

When continuation policy stores a canonical blocker reason, verification should also assert that:

- healthy iterations record `continuation_blocker_reason=none`
- degraded intended-path iterations record `continuation_blocker_reason=intended_path_degraded`
- verifier-disqualifying iterations record `continuation_blocker_reason=verifier_path_disqualifying`
- proposal-ready iterations with verifier `path_acceptability=disqualifying` still record `continuation_blocker_reason=verifier_path_disqualifying`
- healthy proposal-ready iterations keep `continuation_blocker_reason=proposal_ready`

Review or verification rejection should fail verification only if the loop incorrectly pauses, stops, or loses state when policy says it should continue exploring.

When proposer prompts are built from prior autonomous history, verification should also assert that:

- healthy prior iterations keep `blocker=none` and expected-path evidence visible in the proposer input
- degraded or rejected prior iterations keep their blocker and path evidence visible in the proposer input
- the next bounded hypothesis is not chosen from prose-only context when structured failure state already exists
- rejected-before-implementation iterations preserve reviewer `blocking_issue` and `suggested_adjustment` in proposer input

For the feature-flagged active-conversation append SSE path, verification should also assert that:

- healthy live appends arrive through `text/event-stream`
- browser resume relies on monotonic `append_id` and `Last-Event-ID`, not duplicate full-timeline polling
- non-active conversations never render into the active timeline
- polling-driven conversation refetch is not the path that makes healthy live appends appear while SSE is connected
- the workspace exposes machine-readable stream state and per-append provenance so browser verification can attribute visible appends to SSE rather than polling
- inline active-session status in the selected conversation exposes machine-readable state and source derived from live conversation events rather than a separate polling-only status surface
- conversation-local autonomy state should be visible outside the scrollable timeline body so message history remains the first visible content in the center pane

## Commit And Deploy Policy

### Before Commit

At minimum:

- run the gate that matches the risk level of the change
- record the exact commands that were run
- record any gaps that were not verified

### Before Deploy

For medium and high risk changes:

- the required local gates must already pass
- deployed smoke verification must pass for high risk changes
- if a gate is skipped, the reason must be written explicitly in the task summary

## Recommended Workflow

1. make the code change
2. run `make verify-static`
3. run `make verify-contract` if behavior changed
4. run `make verify-deployed` if the change touches runtime, proposal, auth, deployment, or operator-console behavior
5. only then commit and deploy

## Session Continuity Gate

Changes that touch Codex session reuse must prove all of the following:

- the stored session id is reused when valid
- no unexpected `codex.exec.retrying` event appears
- no forbidden resume-only CLI options are injected into `codex exec resume`
- a new session id is recorded only when the old one is genuinely invalid or missing
