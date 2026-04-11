# Factory Runtime Spec

## Iteration

- current iteration: `214`
- bounded focus: `make the sticky rail row a strict mirror of selected-thread session authority`

## Request

- title: `Fully Realtime Session UX Like Codex Desktop`
- source: `goal-loop`
- execution mode: `proposal`

## Problem

Healthy selected-thread ownership, explicit autonomy milestones, switch continuity, and the one-item transcript owner contract are already present, but the durable contract still needs to state that the sticky left-rail row is only a mirror of the same selected-thread authority rather than a separate session owner. The remaining bounded risk is contract drift: future sessions could let the rail row disagree with the transcript or composer state unless that strict mirroring rule is recorded explicitly.

## Target User

The primary user is the operator or developer using the phone-friendly realtime workspace and expecting the navigation rail to reflect the current live session without becoming a competing authority surface.

## Constraints

- Preserve continuity of the existing `factory-runtime` proposal lane.
- Keep the change inside the allowed proposal paths.
- Keep the iteration bounded to the sticky active-session row in the left rail and its browser verification coverage.
- Reuse the current selected-thread session authority, inline transcript block, and composer dock datasets; do not change backend transport, polling, or broader ownership rules.
- Keep exactly one sticky rail row as a compact mirror of the selected-thread conversation id, phase, and follow state on healthy SSE or intentional switch states.
- Keep the rail row non-authoritative and chip-first, and suppress any duplicate selected-card live-owner row while it is present.
- Clear or downgrade the rail row immediately on reconnect, polling fallback, deselection, or terminal completion.
- Keep degraded fallback, switch placeholders, and restore behavior on the existing fail-open path.

## Deliverable

Expose one conversation-first selected-thread workspace where the left rail shows one compact sticky mirror of the same selected-thread live session already owning the transcript and composer, without introducing duplicate rail ownership surfaces.
