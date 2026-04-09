# Factory Runtime Implementation Plan

1. Keep the scope inside the selected conversation workspace and reuse existing live append and event data rather than widening transport behavior.
2. Add one compact live-run row at the timeline/composer boundary that summarizes the active session as `thinking`, `running tool`, `waiting`, or `done`.
3. Drive that row from the selected conversation's live event path and expose machine-readable state or source attributes for browser verification.
4. Keep the row hidden when there is no active conversation and avoid duplicating full timeline content or restoring separate heavy status panels.
5. Extend the static verifier and docs so future sessions can prove the inline progress row is wired to the intended live path.
