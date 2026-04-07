# Focus Launcher Implementation Plan

## Architecture

Use a minimal local web app with a tiny server and a single-page interface.

## Main Modules

- input handling
- task normalization
- first-action generation
- persistence for recent history

## Data Flow

Input task -> normalize text -> generate first action -> save output -> render history

## Suggested Stack

- Python backend
- lightweight templating
- SQLite or JSON persistence

## Risks

- generated action may still be too vague
- history can become cluttered without clear limits

## Build Order

1. create input/output loop
2. add first-action generation
3. persist recent history
4. simplify UI
