# Factory Runtime Tasks

- [x] Keep the current selected-conversation SSE path, session strip ownership, bottom follow control, footer composer, and non-selected snapshot rows unchanged.
- [x] Keep the center conversation shell and composer dock attached during intentional thread switches.
- [x] Reuse `threadTransition` so the newly selected thread shows exactly one compact transition placeholder while its snapshot binds.
- [x] Clear old-thread live ownership and follow state immediately on thread switch.
- [x] Replace the transition placeholder as soon as the new snapshot attaches instead of falling back to a generic empty state.
- [x] Align focused verification and iteration artifacts with the center-workspace thread-switch continuity contract.
