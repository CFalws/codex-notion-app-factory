# Factory Runtime Implementation Plan

1. Reuse the existing thread-transition and selected-thread ownership state as the authoritative switch path for the center workspace.
2. Prove the transition placeholder is the only transient center-pane surface during switch and that `.timeline-empty` remains reserved for true no-selection idle.
3. Prove the header live indicator clears immediately on switch instead of leaking prior healthy ownership.
4. Prove the composer remains bottom-fixed and targeted to the new thread through an explicit `SWITCHING` owner state and non-empty target label.
5. Align the focused verifier, deployed workspace gate, and iteration artifacts with the switch-continuity contract.
