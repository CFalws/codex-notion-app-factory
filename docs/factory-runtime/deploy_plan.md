# Factory Runtime Deploy Plan

## Deployment Impact

This iteration keeps the GitHub Pages operator workspace render layer contract centered on compact selected-thread session chrome. The bounded expectation is that the selected conversation exposes target, attach, handoff, and live transport through chip-first header and footer surfaces without relying on sentence-style helper copy or introducing a second status surface.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Enable `CODEX_FACTORY_ENABLE_INTERNAL_APPEND_SSE=1` only in the internal runtime where the workspace should consume live append frames.
3. Open the operator console on desktop and phone widths with one selected conversation connected through the internal append SSE path.
4. Confirm the selected-thread header summary shows a compact target chip plus compact path, state, and hint chips instead of a sentence-style summary row.
5. Confirm the composer owner row exposes one compact owner chip, one compact target chip, and one compact attach hint without any paragraph-style helper copy.
6. Confirm the composer-adjacent live strip keeps its existing machine-readable transport and phase chips while reducing detail copy to compact chip-like wording.
7. Confirm switching, handoff, live, degraded transport, and idle states remain distinguishable in the same surfaces on desktop and phone widths.
8. Confirm no new status surface appears and the transcript remains the dominant workspace surface.
9. Run `BASE_URL=... API_KEY=... WORKSPACE_APP_ID=factory-runtime ./scripts/verify_deployed_console.sh` and confirm the compact selected-thread session chrome proof still passes without degraded-path signals.
