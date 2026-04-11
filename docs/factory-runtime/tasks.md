# Factory Runtime Tasks

## Iteration 102

- [x] Use canonical selected-thread switch state from `threadTransition` plus `deriveSelectedThreadSessionStatus(...)` instead of ad hoc switching mirrors.
- [x] Keep the center conversation shell mounted and render exactly one compact switching placeholder while the new thread attaches.
- [x] Make the composer strip show `SWITCHING` instead of generic `TARGET` during intentional thread attach.
- [x] Clear switching mirrors from the recent-thread rail so old-thread live ownership does not compete during the switch.
- [x] Align focused verifiers and proposal artifacts with the iteration-102 switch-continuity contract.
