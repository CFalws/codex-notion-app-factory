# Factory Runtime Spec

## Iteration 323

- Selected-thread healthy and degraded session facts must not render as a visible secondary-panel authority path when the center timeline and footer dock already expose the current session state.
- The secondary session-facts drawer may stay available for restore, handoff, switching, and snapshot-only detail, but it must stay suppressed on the selected-thread healthy and degraded paths.
- Deployed verification must fail if secondary-panel session facts appear before or alongside the main selected-thread live-session surfaces on those paths.

## Iteration 322

- The healthy selected-thread center pane must not show a separate header phase badge when the selected-session snapshot is already rendering authoritative live phase visibility in the inline session timeline block and footer dock.
- The healthy transcript live-activity card must stay suppressed on that path so the conversation surface reads as one realtime session instead of parallel status chrome.
- Restore, degraded, provisional, handoff, and switching paths must keep their explicit cues unchanged.

## Iteration 321

- The healthy selected-thread center header must collapse to conversation identity plus at most one compact phase badge driven by the selected-session snapshot.
- The separate healthy header summary row and count-heavy conversation meta prose must stay suppressed on the healthy selected-thread SSE-owned path.
- Restore, degraded, handoff, and switching paths must continue to expose explicit top-of-thread detail, and deployed verification must fail if healthy header duplication remains.

## Iteration 320

- The bottom composer controls must publish the same selected-session snapshot authority as the transcript live activity, header summary, selected rail row, thread scroller, and session strip.
- Malformed selected-thread append downgrade must clear or degrade composer readiness and ownership through that snapshot before any polling-owned recovery evidence appears.
- Deployed verification must fail if the composer controls retain helper-only `READY`, `SSE OWNER`, or other healthy ownership cues after the selected-session snapshot has already degraded.

## Iteration 318

- Selected-thread healthy, degraded, and handoff ownership must be representable through one compact selected-session snapshot derived from the existing realtime transport path.
- The transcript summary, selected rail row, and composer dock must expose that same snapshot through stable DOM datasets.
- Deployed malformed-append verification must assert ordering through the snapshot seam instead of inferring state transitions from separate surface-specific fields.

## Iteration

- current iteration: `312`
- bounded focus: `prove provisional selected-thread attach or resume stays on one session-owned lane in the deployed browser`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, strict rail mirroring, the selected-thread session-stream contract, deployed single-authority proof, the selected-thread handoff path, streamed autonomy identity, merged footer session-composer status, explicit attach authority, restore continuity, switch continuity, central `session_status` authority convergence, and degraded-path timeline ownership are already present. The bounded question for this iteration is proving in deployed-browser verification that selected-thread attach or resume already stays on one session-owned path instead of briefly splitting into poll-driven job state.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting selected-thread attach or resume to feel continuous, with the center timeline, footer dock, and bottom composer staying on one session lane during bootstrap instead of splitting into a restore-only surface that forces inference.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the change bounded to deployed-browser verification and static proof for the existing selected-thread transport ownership boundary between provisional attach or resume and job polling fallback.
- Preserve runtime behavior, degraded fallback behavior, healthy rail mirrors, transcript primary ownership, header summary continuity, switch continuity, and fixed-composer continuity unchanged.
- Prove attach, resume, and send flows stay on the selected-thread session-status plus bootstrap path until healthy SSE ownership settles or an explicit degraded reason appears.
- Avoid introducing a second status source, new polling-owned healthy readiness, or new exception-path regressions.

## Deliverable

Keep selected-thread attach or resume on one canonical provisional session lane as soon as the intended EventSource is open. During that bootstrap window, the center timeline and composer-adjacent footer dock stay mounted with only ATTACH or RESUME plus one carried-forward phase chip, and healthy ownership remains withheld until the selected-thread store models agree on the same conversation in authoritative `sse-live` state. For iteration 312 specifically, prove in the deployed browser that send/bootstrap and restore/resume flows already stay on that provisional session-owned lane with ordered `session.bootstrap` evidence and zero `/api/jobs` or goals takeovers before healthy SSE ownership arrives.
Iteration 245: the dominant selected-thread header summary is already the machine-readable live-session ownership signal, carrying owner, path, and phase from canonical session_status plus SSE authority while degrading or clearing immediately on reconnect, polling fallback, switch, or idle completion.
Iteration 248: the bottom-fixed composer keeps a visible selected-thread target row during healthy and transition states, rendering `READY`, `SWITCHING`, or `HANDOFF` from canonical selected-thread session authority and downgrading or clearing immediately on reconnect, polling fallback, switch, or idle resolution.
Iteration 249: the left-rail active-session row is already the canonical mirror of the currently selected healthy SSE-owned session, exposing owned and canonical cues only for the selected thread and clearing or downgrading immediately on reconnect, polling fallback, idle, terminal, or switch paths.
Iteration 252: the healthy selected-thread runtime path is already session-scoped; deployed verification now terminates on selected-thread `proposal.ready` and SSE phase ordering instead of waiting on `/api/jobs/{id}` or `latest_job_id`.
Iteration 253: the selected-thread footer dock now exposes one merged session-composer bar, with the session strip carrying target, transport, phase, proposal, and follow cues while the separate composer owner row stays hidden as merged state.
Iteration 254: intentional thread switches already keep the selected-thread workspace mounted in this branch, using one compact transition placeholder, preserved composer dock continuity, immediate old-owner clearing, and explicit browser assertions that no generic empty-state flash occurs.
Iteration 259: healthy selected-thread phase progression is already collapsed onto one canonical inline session owner in the transcript timeline, and active SSE session-event cards for those phases are already suppressed while that owner is present.
Iteration 260: selected-thread restore and reselect are already session-scoped in this branch; restore enters explicit `awaiting-bootstrap` or `sse-resume`, keeps the selected-thread shell and composer mounted, resolves healthy ownership through `session.bootstrap` or append SSE, and already rejects early current-thread job or goals polling in the deployed browser gate.
Iteration 262: healthy selected-thread composer-adjacent session chrome is now suppressed in this branch; the fixed composer remains attached to the selected session, but the adjacent strip no longer renders duplicate healthy ownership, transport, phase, or detail state while degraded, restore, handoff, terminal, and follow-only exception paths still retain explicit strip visibility.
Iteration 265: intentional thread switches are already preserved in this branch as one compact selected-thread switching placeholder with a mounted composer dock, immediate stale-owner clearing, and explicit deployed negative assertions against generic empty-state flashes or hidden composer continuity loss.
Iteration 266: selected-thread session-status and append SSE already remain authoritative in this branch for healthy and restore paths; job polling and goals polling are already gated behind explicit loss of selected-thread ownership, and deployed/static verification already asserts that polling-owned authority does not silently reappear before degradation is explicit.
Iteration 267: the deployed browser gate already exercises healthy streaming, restore or resume, degraded fallback, intentional switch, and cancelled switch as one selected-thread scenario matrix, and already rejects early polling authority, stale ownership, hidden degraded recovery, or generic empty-state flashes before they can qualify as correct success.
Iteration 268: healthy selected-thread drill-down is already collapsed in this branch into the canonical timeline session card; autonomy and execution detail surfaces are already suppressed on the healthy path while degraded, restore, handoff, switching, and exception paths keep explicit secondary-panel visibility.
Iteration 269: the bottom footer is already unified in this branch as one selected-thread live dock; the session strip carries footer state and datasets, the composer-owner row stays hidden as merged state whenever that dock is active, and send readiness already derives from the same selected-thread authority model without a parallel footer path.
Iteration 272: the canonical footer dock now exposes healthy selected-thread phase progression directly in this branch; the dock leads with the current SSE-owned phase, keeps explicit proposal-ready or applied cues beside it, and stays on the same selected-thread authority path instead of falling back to generic suppressed footer wording.
Iteration 273: selected-thread `sessionStatus` plus append SSE already remain the only healthy-path authority in this branch for proposal readiness, verifier acceptability, blocker reason, phase progression, and apply readiness; job or goals polling stay gated behind explicit degraded fallback and already cannot claim healthy selected-thread session ownership.
Iteration 274: healthy selected-thread header summary chrome is now suppressed in this branch whenever the center timeline is already the authoritative healthy session surface; the timeline and footer dock remain the only healthy session-owned status surfaces, while restore, degraded, handoff, and other non-healthy paths still restore explicit top-level status visibility.
Iteration 282: healthy selected-thread ownership in this branch is now promoted through one explicit store-level invariant; provisional continuity still appears before bootstrap, but healthy ownership becomes visible only when selected-thread session state and append-stream session-status agree on the same conversation in authoritative `sse-live` state, which keeps polling suppression and healthy ownership aligned.
Iteration 283: the bottom-fixed composer target row now derives only from the canonical selected-thread authority model in this branch; it reports `READY`, `SWITCHING`, or `HANDOFF` for the current selected thread, clears immediately on restore or degraded fallback, and no longer permits stale old-thread or polling-owned live ownership cues.
Iteration 286: the bottom-fixed composer shell now keeps one stable session-dock frame in this branch, with the inline status strip constrained to a single bounded region, the primary textarea and send action retaining their layout, and live selected-thread status chips mutating in place across healthy updates and terminal resolution.
Iteration 288: the currently selected conversation row now mirrors the canonical healthy selected-thread owner cue as a compact shadow-rendered chip row while `active-session-row` remains the only canonical rail authority surface, and that shadow cue clears immediately on reconnect, polling fallback, terminal resolution, or thread switch.
Iteration 289: the healthy selected-thread path already keeps the center session timeline and the bottom composer strip as the canonical live status surfaces in this branch; the secondary execution status surface is already suppressed while healthy SSE authority is present and already returns on degraded, reconnect, restore, switch, and other non-healthy paths.
Iteration 291: the currently selected conversation row now mirrors one compact live phase chip from the canonical selected-thread session surface in this branch; the chip updates immediately on the healthy SSE-owned path and clears back to snapshot-only rendering on reconnect, polling fallback, restore, switch, or terminal paths.
Iteration 292: the currently selected healthy SSE-owned conversation row now carries the strongest live-owner treatment in the rail in this branch while `active-session-row` remains canonical; that stronger treatment clears immediately on reconnect, polling fallback, restore, switch, or terminal paths.
Iteration 293: healthy selected-thread proposal, review, verify, ready, applied, and apply-readiness state now derive from the selected-thread `session_status` SSE payload in this branch; the central live session surface no longer needs a parallel healthy phase path to decide those cues, and jobs polling remains gated behind explicit loss of selected-thread ownership.
Iteration 296: the intentional selected-thread switch contract was already satisfied in this branch before implementation. The controller already starts a thread-transition model, clears old-thread healthy owner cues in the same render path, keeps the composer dock mounted, renders one compact switching placeholder instead of a generic empty state, and the deployed verifier already checks the negative assertions that would disqualify fallback-owned success.
Iteration 297: the healthy selected-thread polling-removal contract was already satisfied in this branch before implementation. The console already derives autonomy summary, healthy proposal and verifier state, blocker reason, apply readiness, and live job identity from append-SSE `session_status`, while `/api/jobs` and `/api/apps/:id/goals` polling stay gated behind explicit loss of selected-thread healthy ownership.
Iteration 304: healthy selected-thread progression now renders through the transcript live activity item as the primary center-timeline live surface in this branch, while the older healthy inline session block stays suppressed and compact header, rail, and composer surfaces remain secondary mirrors.
Iteration 305: the deployed browser gate now proves healthy owner exclusivity and same-render clearing across restore, degraded reconnect, switch, polling fallback, handoff, and terminal-adjacent transition paths in this branch without requiring further UI changes.
Iteration 307: the previously missed healthy selected-thread header summary contract now lands in this branch. One compact machine-readable header row stays visible on the healthy SSE-owned path with selected-thread scope, path, owner, and explicit phase context, while the transcript live activity item remains the only primary center-timeline live surface and degraded or terminal transitions clear the header row in the same render pass.
Iteration 308: the composer-adjacent live rail now reads healthy selected-thread phase progression directly from the selected-thread SSE-owned authority path in this branch. The strip keeps explicit PROPOSAL, REVIEW, VERIFY, AUTO APPLY, READY, and APPLIED wording instead of the older generic helper phrases, while degraded or terminal transitions still clear or downgrade the rail in the same render pass.
