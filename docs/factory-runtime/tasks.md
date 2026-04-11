# Factory Runtime Tasks

## Iteration 148

- [x] Add one store-owned selected-thread active-session row model for owned, handoff, switching, and cleared states.
- [x] Route the active-session row through that store model instead of mirroring rendered header datasets.
- [x] Keep the row compact while exposing `HANDOFF`, `LIVE`, `NEW`, `PAUSED`, and `SWITCHING` cues from selected-thread session state.
- [x] Require switching to keep the rail row visible with `SWITCHING` and `ATTACH` cues instead of clearing to idle.
- [x] Align focused static verification and proposal artifacts with the iteration-148 left-rail session-mirroring contract.
