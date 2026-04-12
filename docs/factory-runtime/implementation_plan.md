# Factory Runtime Implementation Plan

## Iteration 238

Collapse the selected-thread center header into one compact session capsule.

1. Keep the change bounded to the existing header render seam, selected-thread authority model, and matching proposal artifacts.
2. Use the existing chip-first `thread-session-summary` as the only visible center-header session surface.
3. Force the legacy `thread-phase-chip` out of the visible header path so it can no longer act as a second live-status owner.
4. Preserve transcript inline session ownership, footer dock behavior, left-rail cues, and switch or restore continuity on the current intended path.
5. Keep degraded reconnect or polling fallback and terminal clear transitions explicit in the single header capsule.
6. Align static checks, browser checks, and proposal artifacts with the unified header capsule contract.
