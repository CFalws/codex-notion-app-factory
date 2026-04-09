# Factory Runtime Deploy Plan

## Deployment Impact

This changes backend runtime behavior for autonomous goal continuation. GitHub Pages assets are unchanged. The visible impact is in goal iteration state and finish events, which now expose whether the iteration succeeded through the intended path or through degraded fallback signals.

## Rollout Notes

1. Apply the proposal commit onto `main`.
2. Verify that a healthy autonomous iteration records `intended_path.verdict=expected` and can continue normally.
3. Verify that a fallback-only success records concrete degraded signals and pauses with `intended_path_degraded` instead of looking healthy.
4. Confirm deployed runtime checks still exercise the intended path rather than only eventual success.
