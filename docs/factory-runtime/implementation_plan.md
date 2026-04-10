# Factory Runtime Implementation Plan

1. Reuse the existing selected-thread append SSE transport and healthy workspace datasets instead of adding a new rail-specific source.
2. Update the sticky active-session row so its chips mirror the canonical selected-thread owner, phase, and follow or unseen state instead of generic live wording.
3. Keep the rail row healthy-only: clear it immediately on reconnect downgrade, polling fallback, idle, terminal resolution, or thread switch.
4. Preserve non-selected rows as snapshot-only conversation chips.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the active-session SSE mirror contract.
