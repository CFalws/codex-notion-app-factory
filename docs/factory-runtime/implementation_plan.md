# Factory Runtime Implementation Plan

## Iteration 96

Project the selected-thread live session into one transcript-tail timeline item without changing transport or polling behavior.

1. Keep the iteration-95 canonical selected-thread helpers intact and reuse them as the only ownership boundary.
2. Retire the separate inline live block as an owning selected-thread surface and make the transcript live item render handoff, healthy phase progression, and degraded reconnect or polling states.
3. Keep the header and composer strip in compact supporting roles only, preserving the machine-readable datasets needed by the rail and verifiers.
4. Preserve immediate thread-switch clearing and terminal clearing so stale session ownership never survives outside the active transcript tail item.
5. Extend the focused verifier layer and proposal artifacts to assert that the transcript timeline now owns the selected-thread live session surface.
