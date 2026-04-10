# Factory Runtime Implementation Plan

1. Keep the existing selected-thread session rendering and ownership rules unchanged.
2. Extend the deployed workspace gate with one browser-runtime probe that drives the actual ops console DOM.
3. Submit the proposal-lane request through the browser composer so the verifier proves the bottom-docked workspace control and selected-thread session surface together.
4. Force one bounded downgrade transition in the browser runtime and assert the selected-thread inline degraded marker replaces stale healthy ownership.
5. Trigger one intentional thread switch in the browser and assert the switch placeholder plus composer switching datasets appear immediately.
