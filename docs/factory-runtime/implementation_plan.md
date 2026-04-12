# Factory Runtime Implementation Plan

## Iteration 323

- Preserve the existing selected-thread transport and selected-session snapshot authority model.
- Keep restore, handoff, switching, and snapshot detail rendering unchanged.
- Suppress the secondary session-facts panel for selected-thread healthy and degraded paths so it no longer competes with the center timeline and footer dock.
- Tighten static and deployed verification so selected-thread healthy or degraded success fails if secondary-panel session facts remain visible.

## Iteration 322

- Preserve the existing selected-thread transport and selected-session snapshot authority model.
- Keep degraded, restore, provisional, handoff, and switching rendering unchanged.
- Remove the healthy title-row phase badge and healthy transcript live-activity card.
- Reuse the existing inline session timeline block and footer dock as the only healthy selected-thread phase and ownership surfaces in the center pane.
- Tighten static and deployed verification so healthy success fails if duplicate healthy header or helper-only status chrome remains.

## Iteration 321

- Preserve the existing selected-thread transport and selected-session snapshot authority model.
- Keep explicit top-of-thread detail for restore, degraded, handoff, and switching states.
- Collapse healthy header chrome to the conversation title row plus one phase badge backed by the selected-session snapshot.
- Suppress the separate healthy header summary row and count-heavy conversation meta prose on that path.
- Tighten static and deployed verification so healthy success fails if the second header status path remains visible.

## Iteration 320

- Preserve the existing selected-thread transport and snapshot authority model.
- Extend the selected-session snapshot to include the composer owner and readiness fields that were still being derived separately.
- Publish that snapshot on the merged composer owner row and send button datasets.
- Tighten malformed-append deployed verification so composer controls must downgrade through the same snapshot ordering as the transcript, summary, selected row, scroller, and strip.

## Iteration 318

- Re-land the malformed selected-thread append downgrade baseline if this proposal branch is behind the accepted lane.
- Add one store-level selected-session snapshot helper and reuse it across the header summary, selected row mirror, and composer dock.
- Tighten the deployed malformed-append browser assertions around that unified snapshot and its ordered degraded transition evidence.

## Iteration 312

Tighten static and deployed verification so provisional selected-thread attach or resume is explicitly proven as a session-owned no-poll lane.

1. Keep the iteration bounded to deployed-browser verification and static proof of the existing selected-thread provisional ownership contract.
2. Preserve the existing selected-thread transport, healthy promotion, transcript-primary ownership, switch continuity, and bottom-fixed composer continuity unchanged.
3. Prove initial bootstrap, send/bootstrap continuation, and restore/resume with ordered `session.bootstrap` evidence plus ATTACH or RESUME datasets on the selected-thread surfaces.
4. Prove zero `/api/jobs` and goals fetch takeover on those provisional paths before healthy SSE ownership settles.
5. Continue to allow degraded reconnect, retrying, session rotation, and explicit fallback paths to activate polling immediately when expected.
6. Avoid introducing any new authority source, primary live surface, or controller state.
7. Update proposal artifacts to record the landed verification-boundary result and the remaining deployed verification dependency.
Iteration 245 does not widen runtime or UI ownership. It records that the selected-thread center header already exposes the canonical ownership chip beside the session summary and that deployed verification already attributes healthy visibility to that selected-thread SSE-owned signal rather than to polling or side-panel inference.
Iteration 248 keeps transport and header ownership unchanged and restores the same selected-thread certainty directly at the input surface by keeping the composer owner row visible for healthy, handoff, switching, and restore states while preserving explicit degraded or idle clearing.
Iteration 249 does not widen runtime or UI ownership because the selected-thread rail mirror is already correct in this branch: the sticky active-session row is canonical on the healthy selected-thread SSE path, non-selected rows remain snapshot-only, and the deployed gate already attributes that rail marker to the intended selected-thread authority source.
Iteration 252 keeps the selected-thread runtime path unchanged because healthy SSE ownership was already correct in this branch, and tightens the deployed verification seam so that proof of success follows selected-thread SSE phase progression to `proposal.ready` rather than job polling.
Iteration 253 keeps transport and verifier ownership unchanged and merges the previously split footer owner row into the session strip so the selected-thread typing surface reads as one canonical session-composer bar.
Iteration 254 keeps runtime ownership unchanged because switch continuity is already correct in this branch: intentional thread changes already clear old ownership immediately, preserve the selected-thread shell and composer dock, render one compact switching placeholder, and explicitly reject empty-state flashes in the browser gate.
Iteration 259 does not widen runtime or verifier ownership because the one-owner healthy selected-thread timeline contract is already correct in this branch: the inline selected-thread live owner remains canonical during active SSE progress and active SSE session-event cards are already collapsed beneath it.
Iteration 260 does not widen runtime or verifier ownership because the restore path is already correct in this branch: reselecting a saved selected thread enters explicit restore state, mounts the selected-thread shell immediately, resolves healthy ownership through `session.bootstrap` or append SSE, and the deployed gate already rejects early current-thread job or goals polling.
Iteration 262 keeps transport and authority unchanged and narrows only the healthy presentation boundary: the composer-adjacent strip is now suppressed on the healthy selected-thread SSE-owned path so the center timeline remains the sole visible live session owner, while degraded, restore, handoff, terminal, and follow-only paths still retain explicit strip visibility.
Iteration 265 does not widen runtime or verifier ownership because intentional thread switch continuity is already correct in this branch: the selected-thread shell stays mounted, one compact switching placeholder remains visible, the composer dock stays present, stale ownership clears immediately, and the deployed gate already rejects generic empty-state flashes.
Iteration 266 does not widen runtime or verifier ownership because selected-thread session authority is already correct in this branch: healthy and restore paths already derive proposal and phase visibility from session-status plus append SSE, and polling-driven goals or job state remains gated behind explicit loss of selected-thread ownership.
Iteration 267 does not widen runtime or transport behavior because the deployed selected-thread scenario matrix is already correct in this branch: healthy, restore, degraded, switch, and cancelled-switch paths are already exercised together, and the browser gate already rejects polling-owned authority, stale ownership, hidden degraded recovery, and empty-state flashes before success is accepted.
Iteration 268 does not widen runtime or transport behavior because healthy selected-thread drill-down is already correct in this branch: the canonical timeline card already carries phase, milestones, verifier, blocker, and session metadata while healthy-path autonomy and execution detail cards are already suppressed and exception paths already retain explicit secondary-detail visibility.
Iteration 269 does not widen runtime or transport behavior because footer ownership is already correct in this branch: the selected-thread session strip already carries the live footer state, the composer-owner row already hides as merged state whenever that footer surface is active, and send readiness already derives from the same selected-thread authority model.
Iteration 272 keeps transport and ownership unchanged and narrows only the healthy footer presentation boundary: the canonical dock now stays visible on healthy selected-thread runs and exposes phase-led chips and detail copy directly from the existing selected-thread session surface instead of generic suppressed footer wording.
Iteration 273 does not widen runtime or transport behavior because selected-thread status ownership is already correct in this branch: healthy proposal readiness, verifier or blocker state, phase progression, and apply readiness already stay on selected-thread `sessionStatus` plus append SSE, while goals or job polling remain gated behind explicit degraded fallback.
Iteration 274 keeps transport and ownership unchanged and narrows only the remaining healthy duplicate chrome boundary: the healthy header session summary is now suppressed whenever the center timeline is already the authoritative selected-thread session surface, while restore and degraded paths still keep explicit top-level status visibility.
Iteration 282 keeps transport and provisional continuity unchanged and narrows only the final ownership-promotion boundary: once the selected thread is truly healthy, every selected-thread surface now derives healthy ownership from one shared store invariant instead of separately recomputing that promotion in multiple helpers.
Iteration 283 keeps transport and healthy promotion unchanged and narrows only the composer target-row boundary: the bottom-fixed composer now reflects the same canonical selected-thread authority as the other session surfaces and clears instead of surfacing stale restore or degraded ownership.
Iteration 286 keeps transport and ownership unchanged and narrows only the composer ergonomics boundary: the bottom-fixed composer now retains one stable shell and one bounded inline status region so live updates and terminal resolution do not reframe the input surface.
Iteration 288 keeps transport, ownership, and canonical rail authority unchanged and narrows only the selected-row visibility boundary: the currently selected conversation row now mirrors the healthy selected-thread owner cue as a compact shadow marker while the sticky active-session row remains canonical and non-selected rows stay snapshot-only.
Iteration 289 does not widen runtime or transport behavior because healthy selected-thread session convergence is already correct in this branch: the center timeline and bottom composer strip already remain canonical while the secondary execution surface is already suppressed on the healthy SSE-owned path and restored on non-healthy paths.
Iteration 291 keeps transport, ownership, and canonical rail authority unchanged and narrows only the selected-row phase boundary: the currently selected conversation row now mirrors one compact healthy selected-thread phase chip from the canonical session surface while non-selected rows remain snapshot-only.
Iteration 292 keeps transport, ownership, and canonical rail authority unchanged and narrows only the selected-row emphasis boundary: the currently selected healthy SSE-owned conversation row now receives stronger live-owner treatment while non-selected rows remain snapshot-only and `active-session-row` stays canonical.
Iteration 293 keeps transport, ownership, and canonical session surfaces unchanged and narrows only the remaining central authority seam: healthy proposal, verify, ready, applied, and apply-readiness cues now derive from selected-thread `session_status` SSE state instead of split healthy derivation between session-phase and session-strip helpers.
Iteration 296 keeps transport, ownership, switch rendering, and polling suppression unchanged because the current branch already satisfies the bounded switch-handoff contract; the work for this iteration is to record that intended-path result explicitly so a later apply decision is based on verified behavior rather than duplicated rewrites.
Iteration 297 keeps transport, ownership, switch rendering, and healthy-path authority unchanged because the current branch already satisfies the bounded polling-removal contract; the work for this iteration is to record that the selected-thread `session_status` path already owns those healthy cues before any degraded fallback polling is permitted.
Iteration 308 keeps the selected-thread authority path unchanged and narrows only the composer-adjacent rail wording boundary so the existing healthy live strip reads with explicit canonical phases instead of generic helper phrases.
Iteration 304 keeps transport, ownership, rail mirrors, and composer continuity unchanged and narrows only the primary live-phase presentation boundary: healthy selected-thread progression now renders through one transcript live item while the older healthy inline session block remains suppressed.
