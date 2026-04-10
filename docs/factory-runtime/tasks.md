# Factory Runtime Tasks

- [x] Reuse the existing selected-thread append SSE transport as the only healthy-path session authority.
- [x] Promote live append job identity into selected-thread state so healthy session surfaces no longer wait for snapshot-backed `latest_job_id`.
- [x] Update `liveRun`, the header summary row, the transcript live activity, the composer owner row, and the composer-adjacent strip to prefer the latest selected-thread SSE session event.
- [x] Preserve degraded and switched states as non-owned transport states instead of healthy live progression.
- [x] Align the focused verifier, deployed workspace gate, and iteration artifacts with the selected-thread SSE session-authority contract.
