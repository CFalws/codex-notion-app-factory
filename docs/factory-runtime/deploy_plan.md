# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend runtime verification evidence for autonomous goals. GitHub Pages assets are unchanged. The visible impact is in persisted verifier reviews, which now state whether the observed intended path was acceptable or disqualifying.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Verify that a healthy proposal-mode iteration records verifier reviews with `path_acceptability=acceptable`.
3. Verify that a degraded intended-path iteration records verifier reviews with `path_acceptability=disqualifying`.
4. Confirm operators can distinguish correct success from fallback-only success without reading verifier prose.
