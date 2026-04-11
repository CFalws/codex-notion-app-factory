# Factory Runtime Tasks

- [x] Keep the existing conversation shell and bottom-fixed composer mounted during intentional selected-thread switch.
- [x] Preserve exactly one compact switching placeholder in the center timeline while the new selected-thread snapshot and SSE attach are pending.
- [x] Clear old-thread live ownership and reset switching phase datasets to non-authoritative `UNKNOWN` with `thread-transition` provenance.
- [x] Prove the switch path avoids generic empty-state fallback, avoids hidden attach-time `/api/jobs/` takeover, and uses existing selected-thread datasets rather than polling inference.
- [x] Align the focused verifier and iteration artifacts with the bounded switch continuity contract.
