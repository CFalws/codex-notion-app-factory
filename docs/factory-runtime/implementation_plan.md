# Factory Runtime Implementation Plan

## Iteration 145

Map explicit selected-thread SSE phase labels into the existing header indicator context and composer-adjacent session rail.

1. Reuse the current selected-thread shell-phase derivation for the healthy selected-thread SSE path so the header chip becomes phase-first instead of ownership-first.
2. Keep ownership provenance in the compact header copy rather than in a second chip or prose-heavy summary row.
3. Reuse the same explicit phase label in the composer-adjacent live-follow chip so detached follow states do not fall back to generic `LIVE` or `READY`.
4. Keep reconnect, polling fallback, restore, switch, deselection, and terminal idle clearing rules unchanged.
5. Publish machine-readable phase and detail datasets on the header chip so verification can prove those labels come from the intended selected-thread SSE path.
6. Extend focused static and deployed verification plus proposal artifacts so iteration 145 proves phase-specific selected-thread chrome without reintroducing a competing authority surface.
