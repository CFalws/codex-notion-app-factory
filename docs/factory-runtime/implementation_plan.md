# Factory Runtime Implementation Plan

1. Reuse the existing `autonomy_summary` freshness envelope from conversation snapshot and `session.bootstrap` as the first selected-thread autonomy source.
2. Add one client-side fallback gate in `ops-conversations.js` that keeps healthy selected-thread attach, resume, and switch on the snapshot-plus-SSE path when `fallback_allowed=false`.
3. Allow `/api/apps/{app_id}/goals` polling fallback only when freshness is `stale-or-missing`, selected-thread SSE ownership drops, or reconnect degrades away from the healthy path.
4. Preserve append-driven autonomy updates and server-authored freshness fields while making the healthy versus degraded ownership boundary explicit in code.
5. Align focused browser-proof verifiers and iteration artifacts around the bounded polling-suppression contract.
