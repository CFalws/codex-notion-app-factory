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
- a compact selected-conversation composer state row exposes machine-readable transport state, run state, source, proposal readiness, and append provenance derived from live conversation events rather than fragmented polling-only status surfaces
- the compact composer state row exposes machine-readable presentation and terminal-state markers so reconnecting visibility, explicit idle state, and immediate thread-switch clearing can be verified in the browser
- on phone widths, the selected-conversation session strip and composer should share one persistent footer dock so live state stays visible while the input remains reachable in the active thread
- on desktop widths, the thread rail should remain continuously accessible while prose-heavy operator content stays behind a collapsed secondary panel so the transcript remains the dominant workspace surface
- on desktop widths, the primary shell should remain a narrow left rail plus dominant center conversation workspace even when the secondary panel is available, and opening the secondary panel should not turn the desktop back into a three-column dashboard
- the left thread rail should expose compact selected-thread and live-run markers derived from the existing selected-conversation session state so users can identify the active or generating thread without opening secondary panels
- conversation-local autonomy and live-status detail should not render as separate header chrome above the transcript; fuller autonomy detail should stay reachable only in the secondary panel so message history remains the first visible content in the center pane
- the selected-thread live execution surface should appear as one compact composer-adjacent activity bar rather than separate strip and footer status elements, and it should remain driven by the existing selected-conversation SSE path
- after composer submit, the active transcript should show one temporary pending outbound message and the activity bar should expose a short sending handoff state until the accepted response or first live append arrives, with no duplicate or stale pending item after clear conditions
- after the local handoff is accepted, the transcript should show one temporary assistant placeholder until the first real assistant append arrives, and that placeholder should clear on assistant content, terminal failure, idle reset, or thread switch without leaving duplicate assistant turns
- the active-thread header should remain conversation-first, exposing selected-thread identity plus at most one compact live phase badge derived from the existing selected-thread state, with no return to app-centric header chrome or a second status path above the timeline
- the footer should still read as a compact chat-style composer with the textarea as the dominant input surface, send as the primary action, and proposal apply plus auto-open compressed into a compact secondary utility cluster so message entry no longer looks like an admin form
- the selected-thread composer-adjacent live strip should render as one inline chip-first activity bar, keeping transport, phase, proposal readiness, append provenance, and compact action cues visible without returning to a split explanatory strip
- the selected-thread composer-adjacent live rail should remain chip-first, with compact transport, phase, proposal, provenance, and action cues instead of sentence-level strip explanations, while still staying machine-readable from the healthy selected-conversation SSE path
- the selected-thread composer-adjacent live rail should expose append-stream health explicitly so healthy `LIVE` transport and degraded `RECONNECT`, `OPEN`, or `OFFLINE` transport are distinguishable in the same composer-adjacent surface, while polling-only fallback immediately clears live-owned treatment instead of pretending the selected thread is still on a healthy live path
- `make verify-deployed` should include a selected-thread workspace gate for `factory-runtime` that fetches the deployed `/ops/` assets, proves desktop and phone conversation-first layout markers, opens the selected-thread append SSE stream, requires ordered proposal, review, verify, proposal-ready, and terminal progression from captured SSE append frames, and fails on retry fallback, runtime exception, missing selected-thread SSE events, or unexpected session rotation
- on phone widths, the nav sheet should present the conversation list as the first actionable surface while app-level controls move behind a collapsed operator section that stays reachable without displacing thread switching
- on phone widths, opening the nav sheet should re-collapse the secondary operator section and focus the first thread action so the drawer behaves like a deliberate conversation switcher rather than a general control tray
- the selected transcript should stay pinned to the newest append only while the user is already near the bottom, and the bottom follow control should expose explicit `NEW` vs `PAUSED` state plus unseen-count metadata so off-screen selected-thread SSE appends are distinguishable from degraded reconnect or polling fallback before jump-to-latest or composer re-engagement restores follow mode
- the selected transcript should expose at most one compact transcript-tail live activity item that mirrors the current selected-thread SSE-derived phase and detail, updates in place during active execution, and stays hidden for non-selected threads and polling-only fallback
- the selected-conversation composer state row should stay compact in every state, render fixed transport, phase, and proposal chips, and avoid reintroducing a collapsible prose-heavy strip above the action area
- the selected conversation should expose at most one compact composer-adjacent live strip above the active composer, sourced only from the current selected-thread SSE-owned run, and that strip should disappear on terminal or polling-only fallback so it does not duplicate the transcript-tail contract
- after composer submit, the selected transcript and composer-adjacent handoff bar should resolve to one machine-readable handoff stage at a time with either exactly one pending outbound user turn or exactly one temporary assistant placeholder, never both at once, and the accepted placeholder should clear on first real assistant SSE append, terminal failure, idle reset, polling-only fallback, or thread switch
- conversation cards in the left navigation should expose one bounded recent preview line and a clearer compact state label vocabulary so live, reconnecting, done, failed, and idle threads are easier to distinguish without opening them, while non-selected threads remain snapshot-only
- the selected conversation row in the left rail should expose one compact session marker derived from the existing selected-thread state so the active or in-flight thread is recognizable at a glance without turning non-selected rows into live-owned status surfaces
- the selected conversation row should carry the strongest live-owner treatment in the rail so the actively streaming session is unmistakable at a glance, while non-selected rows keep only snapshot cues
- non-selected conversation rows should resolve to one fixed-priority snapshot label and one bounded preview line that prefers recent assistant or user message content over noisier event prose
- the selected-thread header and composer-adjacent live rail should expose explicit PROPOSAL, REVIEW, VERIFY, AUTO APPLY, READY, and APPLIED progression with phase-specific detail copy derived from the existing selected-thread SSE path instead of generic running wording
- the selected-thread header summary row, composer owner row, and composer-adjacent live strip should stay chip-first and target-first, reducing sentence-style helper copy while preserving the existing machine-readable ownership, path, state, transport, and phase datasets
- on phone widths, the navigation affordance should explicitly control a drawer or sheet and the active conversation shell should remain the default visible workspace surface until navigation is deliberately opened
- on phone widths, the active conversation should remain the first visible workspace surface and app or thread navigation should open through an explicit drawer or sheet rather than occupying the top of the reading flow
- on phone widths, closing the nav sheet or choosing a thread or app from it should return focus to the selected conversation surface so the transcript and composer resume as the default workspace owner
- the selected-thread live rail should map healthy SSE events such as `goal.proposal.phase.started`, `goal.review.phase.started`, `goal.verify.phase.started`, `goal.proposal.auto_apply.started`, `proposal.ready`, and `codex.exec.applied` into explicit machine-readable phase labels so the central workspace no longer collapses them into generic thinking or done wording
- the selected-thread center pane should expose one conversation-first workspace marker and one inline selected-thread session block that appears only for pending assistant handoff or active SSE-owned live progress, then clears on terminal resolution or thread switch without becoming a second multi-thread status surface
- the selected conversation row in the left navigation should mirror pending handoff and active live session state only for the currently selected thread, expose compact `HANDOFF`, `LIVE`, `NEW`, or `PAUSED` owner cues plus follow or unread chips, and clear those markers on terminal resolution, polling-only fallback, reconnect downgrade, or thread switch without making any non-selected row appear live-owned
- the left conversation navigation should expose at most one compact sticky active-session row above the conversation list that mirrors the currently selected thread's owner, phase, follow or unseen state, and switching status from the same selected-thread datasets, and that row should clear immediately on idle, terminal, reconnect downgrade, polling fallback, or thread switch
- the selected conversation row should not render helper-style live detail prose in the rail; selected-row session mirroring should stay finite and chip-first with owner and follow cues only
- intentional thread switches should keep the center conversation shell and composer dock in place, clear old-thread live ownership immediately, and render at most one compact selected-thread transition placeholder until the new snapshot attaches instead of dropping to a generic empty-state reset
- the selected-thread switch path should limit the generic empty-state view to true no-conversation idle state only, and should never flash that empty view during an intentional thread transition
- the selected-thread center header should expose one compact machine-readable session summary row for scope, path, and attach state so the main workspace no longer depends on prose-heavy side-panel summary copy to explain the current selected-thread context
- the secondary operator panel should remain collapsed by default, and deeper autonomy or workspace-summary prose should stay optional rather than competing with the transcript and composer as a primary workspace surface
- the composer should expose one compact target row naming the selected thread and showing `READY`, `SWITCHING`, or `HANDOFF` from existing selected-thread ownership state, and it should never advertise stale old-thread or polling-derived live ownership after a switch
- the selected transcript should expose exactly one compact bottom follow control only when the selected thread is detached from the tail and unseen selected-thread appends are present, and that control should publish explicit `NEW` vs `PAUSED` state plus unseen-count metadata
- the selected-thread follow control should clear immediately on jump-to-latest, thread switch, terminal idle, reconnect downgrade, or polling-only fallback, and no non-selected thread should ever gain a live-owned transcript follow affordance
- the left rail should remain conversation-first, with thread history rendered ahead of heavier app or operator controls and the selected app still identifiable through one compact always-visible summary near the rail header
- app and operator controls in the rail should stay collapsed by default and remain reachable without displacing thread history as the primary visible rail surface on desktop and phone widths
- the selected-thread footer should remain chat-first, with the textarea and primary send action visually dominant while apply and auto-open live behind one compact utility affordance rather than an always-expanded control cluster
- the footer utility affordance should expose machine-readable open or closed state, remain collapsed by default, and should not become a second live-status surface or re-expand into a form-like footer on phone widths

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
