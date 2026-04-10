# Factory Runtime Tasks

- [x] Define an authoritative selected-thread append-stream boundary that treats healthy SSE `connecting` and `live` startup as realtime-owned.
- [x] Remove the eager healthy-path submit poll so session startup stays on local handoff plus append SSE.
- [x] Keep polling activation available only for degraded paths such as unavailable EventSource, reconnect, ownership loss, or downgraded transport.
- [x] Align the job controller with the same authoritative boundary so polling does not restart during healthy selected-thread SSE startup.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the degraded-only polling boundary contract.
