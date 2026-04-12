# Factory Runtime Deploy Plan

## Iteration 329

- Run the deployed first-load selected-thread bootstrap scenario and confirm the verifier records ordered target-selection, bootstrap-event, and bootstrap-marker evidence for the same conversation id.
- Treat deployment readiness as blocked if the first-load selected-thread bootstrap path depends on polling-owned refetch, attaches to a mismatched conversation, regresses the bootstrap cursor, shows retry fallback, shows unexpected session rotation, or emits an EventSource error before bootstrap stabilizes.

## Iteration 323

- Run the deployed healthy and degraded selected-thread scenarios and confirm the center timeline plus footer dock remain the only visible live-session status surfaces.
- Treat deployment readiness as blocked if the secondary session-facts drawer becomes visible or authoritative on selected-thread healthy or degraded paths.

## Iteration 322

- Run the deployed healthy selected-thread scenario and confirm the header shows only conversation identity, with the inline session timeline block and footer dock carrying healthy live phase visibility.
- Treat deployment readiness as blocked if the healthy path still shows a visible header phase badge or a separate healthy transcript live-activity card alongside the inline session block.

## Iteration 321

- Run the deployed healthy selected-thread scenario and confirm the center pane starts with conversation identity plus one phase badge, with the separate healthy header summary row hidden and the conversation-meta prose cleared.
- Treat deployment readiness as blocked if the healthy path still shows a second visible header status surface or helper-only meta prose above the transcript.

## Iteration 320

- Run the deployed malformed-append browser scenario and confirm the merged composer owner row and send button datasets degrade through the same selected-session snapshot as the transcript, summary, selected row, scroller, and strip.
- Treat deployment readiness as blocked if the composer controls still expose `READY`, `SSE OWNER`, or any other healthy owner cue before the degraded selected-session reason appears.

## Iteration 318

- Run the deployed malformed-append browser scenario and confirm the selected-session snapshot downgrades first across thread summary, selected row, thread scroller, and composer dock.
- Treat deployment readiness as blocked if any of those surfaces still requires poll inference or retains stale healthy ownership before the snapshot degrades.

## Iteration 312

This deploy plan validates that the deployed browser gate explicitly proves selected-thread send/bootstrap and restore/resume stay on one provisional session-owned lane with no poll-driven transient takeover before healthy SSE ownership arrives.

## Deployment Impact

This iteration keeps transport, provisional continuity, healthy promotion, composer targeting, selected-row rail parity, freshness, phase mirrors, switch continuity, and central `session_status` authority convergence intact. The gate should pass only when the deployed verifier shows ordered `session.bootstrap` evidence plus ATTACH or RESUME datasets on selected-thread surfaces and no `/api/jobs` or goals takeover before healthy SSE ownership settles.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with a selected thread that can enter healthy live progress and separate paths that can exercise restore, switch, handoff, and degraded fallback.
4. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh`.
5. Confirm selected-thread attach or resume keeps the center timeline and footer dock mounted as one provisional session lane with only ATTACH or RESUME plus one carried-forward phase chip and no duplicate restore-only chrome.
6. Confirm the first healthy selected-thread promotion appears only after selected-thread session state and append-stream session-status agree on the same conversation in authoritative `sse-live` state.
7. Confirm initial selected-thread bootstrap records ordered `session.bootstrap` evidence and ATTACH datasets with zero `/api/jobs` and goals takeover before healthy SSE ownership arrives.
8. Confirm selected-thread send/bootstrap continuation and restore/resume do the same, including resumed append-stream URLs where expected.
9. Confirm reconnect, polling fallback, restore failure, switch, terminal, and other non-healthy paths still activate degraded fallback immediately and visibly when expected.
10. Confirm `active-session-row` remains canonical, selected-row owner and freshness mirrors remain unchanged, and non-selected rows stay snapshot-only.
11. Treat the proposal as ready only after the deployed verifier passes and the runtime contract check is rerun in an environment with the missing dependencies.
Iteration 245 deploy gate expectation: healthy selected-thread runs are acceptable only when the center-header session summary itself reports `SSE OWNER`, degraded runs visibly downgrade to `RECONNECT` or `POLLING`, and switch or terminal idle clears the header ownership signal immediately.
Iteration 248 deploy gate expectation: the bottom-fixed composer owner row remains visible for the selected thread on healthy and transition paths, shows `READY` only on the healthy selected-thread SSE path, and downgrades or clears immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249 deploy gate expectation: the selected-thread left-rail active-session row remains canonical only on the healthy SSE-owned path and downgrades or clears immediately on reconnect, polling fallback, terminal idle, or thread switch without granting live-owned treatment to non-selected rows.
Iteration 252 deploy gate expectation: healthy selected-thread success is attributed to SSE phase ordering through `proposal.ready`, with no deployed verifier dependence on `/api/jobs/{id}` or `latest_job_id` to prove the healthy selected-thread path.
Iteration 253 deploy gate expectation: the selected-thread footer dock is a single merged session-composer surface, with the session strip carrying the live footer state and the composer owner row remaining hidden as merged state.
Iteration 254 deploy gate expectation: an intentional thread switch preserves one mounted selected-thread workspace with exactly one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and no generic empty-state flash before the incoming snapshot binds.
Iteration 259 deploy gate expectation: healthy selected-thread proposal, review, verify, auto-apply, ready, and applied progress remain on one canonical inline session owner, while duplicate active-phase SSE session-event cards are suppressed until degraded or terminal resolution.
Iteration 260 deploy gate expectation: reopening or reselecting a selected thread enters explicit restore state, keeps the selected-thread shell and composer mounted, resolves healthy ownership through `session.bootstrap` or append SSE, and records zero early current-thread `/api/jobs/{id}` or goals authority before degraded fallback is required.
Iteration 262 deploy gate expectation: the healthy selected-thread SSE-owned path suppresses duplicate composer-adjacent strip chrome so the center timeline remains the sole visible live session owner, while degraded, restore, handoff, terminal, and follow-only exception paths retain explicit strip visibility.
Iteration 265 deploy gate expectation: intentional selected-thread switches already preserve one mounted selected-thread workspace with one compact switching placeholder, a still-mounted composer dock, immediate stale-owner clearing, and explicit negative assertions against generic empty-state or reset flashes.
Iteration 266 deploy gate expectation: healthy and restore selected-thread proposal and phase visibility already remain session-status plus append-SSE owned in this branch, while job-poll and goals-poll authority remain absent until an explicit degraded fallback boundary is crossed.
Iteration 267 deploy gate expectation: the deployed browser verifier already covers healthy, restore, degraded, switch, and cancelled-switch selected-thread scenarios together and accepts success only when the selected-thread session stays authoritative through the intended path without silent polling-owned recovery, stale ownership, or empty-state flashes.
Iteration 268 deploy gate expectation: the healthy selected-thread timeline card already serves as the sole visible live drill-down surface in this branch, while autonomy and execution detail remain suppressed on that healthy path and explicit secondary-detail visibility returns only on degraded, restore, handoff, switching, and exception paths.
Iteration 269 deploy gate expectation: the footer already behaves as one canonical selected-thread live dock in this branch, with the session strip carrying footer state, the composer-owner row staying hidden as merged state, and send readiness remaining tied to selected-thread authority instead of any polling-owned fallback.
Iteration 272 deploy gate expectation: the canonical footer dock stays visible on healthy selected-thread runs in this branch, leads with explicit phase progression labels from the selected-thread SSE or session bootstrap path, and still downgrades or clears through the same authority model on restore, switch, handoff, reconnect, polling fallback, or terminal paths.
Iteration 273 deploy gate expectation: healthy selected-thread proposal readiness, verifier acceptability, blocker reason, phase progression, and apply readiness already remain selected-thread `sessionStatus` plus append-SSE owned in this branch, while goals and job polling remain absent from healthy ownership until an explicit degraded fallback boundary is crossed.
Iteration 274 deploy gate expectation: healthy selected-thread runs now keep the header session summary hidden in this branch while the center timeline and footer dock remain authoritative; restore and degraded paths still restore explicit top-level status visibility and continue to reject polling-owned healthy success.
Iteration 282 deploy gate expectation: once the selected thread becomes truly healthy in this branch, healthy ownership is promoted exactly once through one shared selected-thread invariant, every healthy selected-thread surface agrees on that owner state, and jobs or goals polling remain absent until an explicit degraded fallback boundary is crossed.
Iteration 283 deploy gate expectation: the bottom-fixed composer target row now derives only from canonical selected-thread authority in this branch, exposes `READY`, `SWITCHING`, or `HANDOFF` only for the current selected thread, and clears immediately on restore, reconnect, degraded fallback, or stale-thread loss without regaining healthy ownership from polling.
Iteration 286 deploy gate expectation: the bottom-fixed composer shell now keeps one stable session-dock frame in this branch, the inline status strip remains bounded on healthy live updates, the textarea-first layout persists through terminal resolution, and no second status strip appears during selected-thread updates.
Iteration 288 deploy gate expectation: `active-session-row` remains canonical in this branch while the currently selected conversation row mirrors the healthy selected-thread owner cue as one compact shadow marker, and that selected-row marker clears immediately on reconnect, degraded fallback, terminal resolution, or thread switch without granting live-owned treatment to any non-selected row.
Iteration 289 deploy gate expectation: the healthy selected-thread path already keeps the center session timeline and bottom composer strip as the canonical live status surfaces in this branch, while the secondary execution surface remains suppressed until degraded, reconnect, restore, switch, terminal, or other non-healthy paths require it again.
Iteration 291 deploy gate expectation: the currently selected conversation row now mirrors one compact live phase chip from the canonical selected-thread session surface in this branch, updating immediately on the healthy SSE-owned path and clearing back to snapshot-only rendering on reconnect, degraded fallback, restore, switch, terminal, and other non-healthy paths.
Iteration 292 deploy gate expectation: the currently selected healthy SSE-owned conversation row now carries the strongest live-owner treatment in this branch through the existing selected-thread mirror datasets, and that stronger treatment clears immediately on reconnect, degraded fallback, restore, switch, terminal, and other non-healthy paths while `active-session-row` remains canonical.
Iteration 293 deploy gate expectation: healthy selected-thread proposal, review, verify, ready, applied, and apply-readiness state now remain `session_status` plus append-SSE owned in this branch, and polling never mutates those central controls until an explicit degraded fallback boundary is crossed.
Iteration 296 deploy gate expectation: an intentional selected-thread switch already behaves as one continuous session handoff in this branch, with one compact target placeholder, immediate stale-owner clearing, a still-mounted composer dock, no generic empty-state flash, and no polling-owned healthy reclaim while the placeholder is active.
Iteration 297 deploy gate expectation: healthy selected-thread autonomy, proposal, verifier, blocker, apply-readiness, and live job identity already remain append-SSE `session_status` owned in this branch, and `/api/jobs` plus goals polling stay absent from healthy selected-thread authority until an explicit degraded fallback boundary is crossed.
Iteration 304 deploy gate expectation: the healthy selected-thread path now renders exactly one primary transcript live activity item in this branch, the older healthy inline session block remains absent there, and reconnect, restore, switch, polling fallback, handoff, and terminal paths clear or downgrade that primary live treatment immediately.
Iteration 305 deploy gate expectation: the deployed browser verifier now accepts success only when healthy selected-thread workspace ownership remains exclusive to the intended transcript and composer surfaces and clears in the same render frame on restore, degraded reconnect, switch, polling fallback, handoff, and terminal-adjacent transitions.
Iteration 307 deploy gate expectation: the healthy selected-thread path now also keeps one compact contextual header summary row visible with selected-thread scope, path, owner, and explicit phase from the intended SSE-owned authority, while the transcript live item remains primary and reconnect, restore downgrade, switch, polling fallback, idle, handoff loss, and terminal paths clear or downgrade the header row immediately.
Iteration 308 deploy gate expectation: the healthy selected-thread path now keeps explicit canonical phase wording in the composer-adjacent live rail, the transcript live item remains primary, and reconnect downgrade, polling fallback, switch, idle, restore downgrade, handoff loss, and terminal paths clear or downgrade that rail without leaving stale generic healthy wording behind.
