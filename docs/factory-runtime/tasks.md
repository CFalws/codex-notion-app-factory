# Factory Runtime Tasks

## Iteration 335

- [x] Keep transport, switching, rail ownership, and composer layout unchanged.
- [x] Mark healthy selected-thread job phase and apply readiness as explicit selected-thread SSE authority instead of polling-owned fallback.
- [x] Preserve polling as a degraded or non-selected fallback path with explicit polling authority markers.
- [x] Tighten static and deployed verification so healthy selected-thread proposal or apply visibility fails if it is still polling-owned.
- Iteration 335: make healthy selected-thread proposal and apply authority machine-readable as SSE-owned while keeping polling explicit as fallback only.

## Iteration 334

- [x] Keep transport, selected-session authority, switch continuity, center conversation shell, and bottom-fixed composer unchanged.
- [x] Make the selected conversation row the sole healthy and handoff live-owner rail surface.
- [x] Repurpose the sticky active-session row as an explicit fallback cue only for degraded, restore, reconnect, polling fallback, and switching states.
- [x] Tighten static and deployed verification so healthy selected-thread success fails if both rail surfaces remain visible together.
- Iteration 334: remove duplicate healthy rail chrome so the selected row becomes the only healthy left-rail realtime owner cue.

## Iteration 333

- [x] Keep transport, polling fallback precedence, and the current switch runtime model unchanged unless a real switch authority gap appears.
- [x] Make intentional selected-thread switching machine-verifiable through the selected-session snapshot rather than placeholder timing alone.
- [x] Prove the `switching` snapshot clears on target attach resolution without empty-state reset, hidden composer dock, or poll-owned takeover.
- [x] Record the result as a bounded switch-continuity proof iteration.
- Iteration 333: treat selected-thread switching as an explicit session-scoped snapshot state in verification and prove it resolves cleanly through the mounted workspace shell.

## Iteration 329

- [x] Keep the iteration verification-only and scoped to first-load selected-thread bootstrap authority.
- [x] Add one ordered deployed-browser evidence gate for selected-thread target selection, bootstrap event arrival, and selected-thread bootstrap markers.
- [x] Fail the gate on polling-owned refetch, mismatched conversation attachment, regressing bootstrap cursor, retry fallback, unexpected session rotation, or early EventSource error.
- [x] Keep composer ergonomics, proposal and apply rendering, malformed shadow cases, and broader authority promotion out of scope.
- Iteration 329: define one low-risk deployed verification artifact for ordered selected-thread bootstrap authority on first load.

## Iteration 323

- [x] Keep transport and selected-session ownership unchanged while removing the remaining selected-thread secondary-panel session-facts duplication.
- [x] Suppress the secondary session-facts drawer for selected-thread healthy and degraded paths so the center timeline and footer dock stay authoritative.
- [x] Preserve restore, handoff, switching, and snapshot detail on their existing explicit paths.
- [x] Tighten static and deployed verification so selected-thread healthy or degraded success fails if secondary-panel session facts remain visible.
- Iteration 323: suppress selected-thread secondary-panel session facts so the center timeline plus footer dock remain the only live-session status surfaces on healthy and degraded paths.

## Iteration 322

- [x] Keep transport and selected-session ownership unchanged while removing the last healthy header status surface.
- [x] Enable the healthy selected-thread inline session timeline block as the center-pane live phase surface.
- [x] Suppress the healthy transcript live-activity card and healthy title-row phase badge so healthy status remains visible only through the inline session block and footer dock.
- [x] Tighten static and deployed verification so healthy success fails if duplicate healthy status chrome remains above the transcript.
- Iteration 322: converge healthy selected-thread live phase visibility onto the inline session block plus footer dock and remove the last duplicate header badge.

## Iteration 321

- [x] Keep transport and selected-session ownership unchanged while simplifying the healthy selected-thread header chrome.
- [x] Move healthy header status to the conversation-first title row plus one phase badge sourced from the selected-session snapshot.
- [x] Suppress the separate healthy header summary row and count-heavy conversation meta prose while preserving explicit top-of-thread detail for restore, degraded, handoff, and switching states.
- [x] Tighten static and deployed verification so healthy success fails if the extra healthy header status path remains visible.
- Iteration 321: collapse healthy selected-thread header duplication into one compact phase badge on the conversation-first title row.

## Iteration 320

- [x] Keep transport and selected-session ownership unchanged while extending the snapshot seam to the bottom composer controls.
- [x] Make the merged composer owner row and send button publish selected-session snapshot datasets instead of relying only on helper-local owner state.
- [x] Tighten malformed-append deployed verification so stale composer READY or SSE-owner cues fail before any poll-led recovery can explain the downgrade.
- Iteration 320: converge composer control readiness and ownership onto the same selected-session snapshot used by the transcript, summary, rail row, scroller, and strip.

## Iteration 318

- [x] Restore the missing malformed selected-thread append downgrade seam in this proposal branch so the unified snapshot reflects a real degraded transition.
- [x] Introduce one unified selected-thread session snapshot in store state derivation.
- [x] Make the header summary, selected rail row, and bottom composer publish that same selected-session snapshot through stable DOM datasets.
- [x] Extend the deployed malformed-append verifier path to assert ordered downgrade through the unified snapshot instead of mixed per-surface inference.
- Iteration 318: converge malformed selected-thread downgrade proof on one authoritative selected-session snapshot seam.

## Iteration 312

- [x] Keep the iteration bounded to deployed-browser verification and static proof of the existing provisional selected-thread ownership contract.
- [x] Preserve the existing selected-thread `session_status` plus append SSE transport, promotion, and degraded fallback contract.
- [x] Prove initial bootstrap, send/bootstrap continuation, and restore/resume with explicit `session.bootstrap` evidence and ATTACH or RESUME datasets.
- [x] Prove that `/api/jobs` and goals fetches do not take over selected-thread authority on those provisional paths before healthy SSE ownership arrives.
- [x] Continue allowing immediate polling fallback on explicit degraded paths only.
- [x] Update proposal artifacts to record the intended-path verifier result.
- Iteration 312: prove provisional selected-thread attach or resume stays on one deployed session-owned lane with no poll takeover.
- Iteration 245: confirm the selected-thread center header already exposes the canonical ownership chip and keep deployed verification bound to that machine-readable selected-thread signal without adding another live-status surface.
- Iteration 248: keep the selected-thread composer owner row visible on healthy and transition paths, render `READY` only on healthy SSE-owned state, and assert degraded paths never retain stale ready ownership.
- Iteration 249: record that the sticky left-rail active-session row is already the canonical selected-thread SSE mirror and keep non-selected rows snapshot-only with immediate clear or downgrade on degraded paths.
- Iteration 252: record that healthy selected-thread runtime transport was already session-scoped and move the remaining deployed proof path off job polling and onto `proposal.ready`.
- Iteration 253: collapse the split footer owner-row plus strip presentation into one canonical selected-thread session-composer bar.
- Iteration 254: record that intentional thread switches already preserve one mounted selected-thread workspace with a single switching placeholder, mounted composer dock, and no generic empty-state flash.
- Iteration 259: record that healthy selected-thread progress already uses one canonical in-timeline live owner and collapses duplicate active-phase SSE session-event cards while that owner is present.
- Iteration 260: record that reopening or reselecting a saved selected thread already uses explicit restore state, resolves healthy ownership through `session.bootstrap` or append SSE, and rejects early current-thread job or goals polling on the healthy path.
- Iteration 262: suppress duplicate healthy composer-adjacent session-strip chrome so the center timeline remains the sole visible live session owner while exception-path strip visibility remains explicit.
- Iteration 265: record that intentional selected-thread switches already keep one compact center placeholder, a mounted composer dock, immediate stale-owner clearing, and explicit browser assertions against empty-state or reset flashes.
- Iteration 266: record that selected-thread proposal and phase authority already remain session-status plus append-SSE owned across healthy and restore paths, while goals-poll and job-poll visibility remain gated behind explicit degraded fallback.
- Iteration 267: record that the deployed browser verifier already proves the selected thread as one session-scoped realtime owner across healthy, restore, degraded, switch, and cancelled-switch scenarios with negative assertions against polling-owned success, stale ownership, hidden degraded recovery, and empty-state flashes.
- Iteration 268: record that healthy selected-thread autonomy and execution drill-down already live on the canonical timeline card while the secondary autonomy and execution surfaces are already suppressed on the healthy path and remain explicit only on exception paths.
- Iteration 269: record that the selected-thread footer is already unified as one canonical live dock, with the session strip carrying footer state, the composer-owner row hidden as merged state, and send readiness driven by the same authority model.
- Iteration 272: keep the selected-thread footer dock canonical, but make it phase-led and healthy-visible so the bottom composer surface itself exposes current proposal, review, verify, auto-apply, ready, or applied state without relying on generic suppressed footer wording.
- Iteration 273: record that healthy selected-thread proposal readiness, verifier or blocker state, phase progression, and apply readiness already remain sessionStatus-plus-append-SSE owned, while goals and job polling stay demoted to explicit degraded fallback only.
- Iteration 274: suppress the remaining healthy top-level header session summary so the center timeline and footer dock are the only healthy selected-thread status surfaces, while non-healthy paths keep explicit duplicate-free status visibility.
- Iteration 282: promote healthy selected-thread ownership exactly once through one canonical store-level gate so provisional continuity remains intact before bootstrap, but every healthy selected-thread surface and polling suppression decision now shares the same promotion invariant.
- Iteration 283: bind the bottom-fixed composer target row to canonical selected-thread authority so it exposes only `READY`, `SWITCHING`, or `HANDOFF` for the selected thread and clears immediately on restore, reconnect, or polling fallback.
- Iteration 286: keep the bottom-fixed composer as one invariant selected-thread session dock so live status and proposal cues update in place without shifting, detaching, or reframing the input surface during healthy live updates or terminal resolution.
- Iteration 288: keep `active-session-row` canonical but mirror its healthy selected-thread owner cue onto the currently selected conversation row as a compact shadow marker that clears immediately on degrade, reconnect, polling fallback, terminal resolution, or thread switch.
- Iteration 289: record that healthy selected-thread job, phase, proposal, verifier, and apply visibility already remain collapsed onto the center session timeline plus bottom composer strip, while the secondary execution surface already stays suppressed on the healthy path and returns only on non-healthy paths.
- Iteration 291: mirror one compact healthy selected-thread live phase chip into the currently selected conversation row so the rail reflects current session stage immediately while non-selected rows remain snapshot-only.
- Iteration 292: make the healthy selected conversation row visually dominant in the rail through stronger live-owner treatment derived from the existing selected-thread mirror, while `active-session-row` remains canonical and non-selected rows stay snapshot-only.
- Iteration 293: promote healthy selected-thread proposal, verify, ready, applied, and apply-readiness cues to a single `session_status` SSE authority path in the central session surface while jobs polling remains explicit degraded fallback only.
- Iteration 296: record that intentional selected-thread switch continuity is already correct in this branch, with one compact placeholder, immediate stale-owner clearing, mounted composer continuity, and no generic empty-state flash or polling-owned healthy reclaim.
- Iteration 297: record that healthy selected-thread autonomy, proposal, verifier, blocker, apply-readiness, and live job identity are already append-SSE `session_status` owned in this branch, while `/api/jobs` and goals polling remain explicit non-healthy fallbacks only.
- Iteration 305: tighten the deployed selected-thread workspace gate so it proves healthy owner exclusivity and same-render clearing on restore, degraded reconnect, switch, polling fallback, handoff, and terminal-adjacent transitions.
- Iteration 304: promote healthy selected-thread progression into one primary transcript live item while suppressing the older healthy inline session block and keeping header, rail, and composer as compact secondary mirrors.
- Iteration 338: move restore, reconnect, and polling-fallback selected-thread truth into the primary center timeline session block and suppress secondary autonomy and execution cards whenever a selected-session state is already present.
- Iteration 337: keep review quorum, verify quorum, and ready progression on one selected-thread `session_status` authority helper and clear or downgrade those cues immediately on reconnect, switch, deselection, missing iteration data, or polling fallback.
- Iteration 339: collapse healthy and provisional selected-thread phase progression into one canonical inline session item and suppress duplicate selected-thread SSE session-event rows while that canonical item owns the center timeline.
- Iteration 340: collapse selected-thread send, accepted, and generating handoff into the same canonical inline session item and suppress pending placeholders plus composer-adjacent handoff copy while that item owns the handoff seam.
- Iteration 344: inline healthy selected-thread blocker, intended-path, verifier, quorum, and ready state into the bottom strip as well as the canonical center session block so the healthy autonomy lane stays session-owned and duplicate secondary autonomy chrome remains suppressed.
- Iteration 343: suppress the sticky active-session rail on intentional thread switches so switching appears only in the center selected-session lane plus bottom composer, while degraded reconnect and polling fallback remain explicit rail-only exception cues.
