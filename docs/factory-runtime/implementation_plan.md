# Factory Runtime Implementation Plan

## Iteration 156

Refine the selected-thread header badge so it carries both phase and live path state.

1. Reuse the existing selected-thread session ownership, transport, phase, and timeline-authority models to keep `#thread-phase-chip` as the only compact header badge.
2. Change the badge label so it combines current phase with selected-thread path state such as healthy SSE, reconnect, polling fallback, restore attach, or switching.
3. Preserve the title row as identity-first and keep the badge as the only status chrome above the transcript.
4. Mirror healthy, degraded, switching, restore, and idle selected-thread states through the same canonical badge datasets without introducing new state or transport sources.
5. Extend focused static and deployed verification so the badge must show both phase and path state while the removed summary strip stays absent.
6. Align proposal artifacts with the iteration-156 combined-phase-and-path badge contract.
