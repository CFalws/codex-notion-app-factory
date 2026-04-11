# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread SSE-owned live-run model in `ops-render.js` instead of adding a new execution-state source.
2. Add one render-layer helper that decides whether the secondary execution-status card should stay in the side panel or be promoted into the center-lane contract.
3. Hide the secondary execution-status card on the healthy selected-thread path and mark its datasets as `center-lane` so the central session strip and transcript remain the only authoritative live session surface.
4. Preserve explicit degraded behavior by restoring the secondary execution-status card as `secondary-detail` whenever the selected-thread path downgrades, loses ownership, or stops being a live advancing run.
5. Extend focused browser-proof verifiers and iteration artifacts around the bounded single-surface execution-visibility contract.
