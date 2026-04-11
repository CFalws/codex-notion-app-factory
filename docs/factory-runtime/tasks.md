# Factory Runtime Tasks

## Iteration 152

- [x] Derive the sticky active-session row directly from selected-thread session status, shell phase, and follow-control models.
- [x] Restrict the row to healthy selected-thread ownership and bounded handoff only.
- [x] Clear the row immediately on reconnect, polling fallback, switch, terminal idle, deselection, and other lost-authority paths.
- [x] Preserve compact owner, phase, and follow or unseen cues without introducing another state source.
- [x] Align focused static verification and proposal artifacts with the iteration-152 left-rail sticky-row contract.
