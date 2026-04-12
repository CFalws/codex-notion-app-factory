# Factory Runtime Tasks

## Iteration 242

- [x] Keep the change bounded to left-rail active-session row ownership attribution in `ops-store.js` and verifier artifacts.
- [x] Preserve the existing selected-thread `session_status` plus SSE authority path unchanged.
- [x] Mark healthy selected-thread active-session visibility as canonical and owned.
- [x] Preserve switching, handoff, degraded, and idle clear behavior unchanged.
- [x] Keep non-selected rows snapshot-only.
- [x] Align proposal artifacts with the canonical left-rail active-session mirror contract.
- Iteration 245: confirm the selected-thread center header already exposes the canonical ownership chip and keep deployed verification bound to that machine-readable selected-thread signal without adding another live-status surface.
- Iteration 248: keep the selected-thread composer owner row visible on healthy and transition paths, render `READY` only on healthy SSE-owned state, and assert degraded paths never retain stale ready ownership.
