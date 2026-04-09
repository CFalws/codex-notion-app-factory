# State Contract

This repository relies on file-backed runtime state. Changes should preserve these contracts unless a migration is intentional and documented.

## App Registry

Path: `state/registry/apps/<app_id>.json`

Required fields:

- `app_id`
- `title`
- `workspace_path`
- `source_path`
- `status`
- `session_id`
- `deployment_url`
- `last_summary`
- `created_at`
- `updated_at`

Proposal-mode fields when applicable:

- `execution_mode`
- `base_branch`
- `allowed_paths`
- `restart_service`

## Request Record

Path: `state/requests/<app_id>/<request_id>.json`

Required fields:

- `request_id`
- `app_id`
- `conversation_id`
- `status`
- `title`
- `request_text`
- `source`
- `intent_summary`
- `ux_context`
- `created_at`
- `updated_at`

## Job Record

Path: `state/runtime/jobs/<job_id>.json`

Required fields:

- `job_id`
- `app_id`
- `request_id`
- `conversation_id`
- `title`
- `intent_summary`
- `ux_context`
- `status`
- `created_at`
- `updated_at`
- `started_at`
- `completed_at`
- `error`
- `result_summary`
- `decision_summary`

Optional fields:

- `proposal`
- `ux_review`
- `goal_review`

## Goal Record

Path: `state/runtime/goals/<goal_id>.json`

Required fields:

- `goal_id`
- `app_id`
- `conversation_id`
- `title`
- `objective`
- `source`
- `status`
- `created_at`
- `updated_at`
- `started_at`
- `completed_at`
- `max_iterations`
- `current_iteration`
- `last_job_id`
- `best_job_id`
- `best_summary`
- `stop_reason`
- `halt_requested`
- `policy`
- `iterations`

### Goal Iteration Shape

Required fields:

- `iteration`
- `request_id`
- `job_id`
- `status`
- `result_summary`
- `decision_summary`
- `goal_review`
- `completed_at`

## Proposal Record

Path: `state/runtime/proposals/<job_id>.json`

Required fields once proposal mode is used:

- `job_id`
- `app_id`
- `request_id`
- `status`
- `title`
- `branch_name`
- `base_branch`
- `head_commit`
- `worktree_path`
- `result_summary`
- `decision_summary`
- `created_at`
- `updated_at`

Apply-time fields when applicable:

- `applied_at`
- `push_status`
- `push_remote`
- `push_branch`
- `push_message`
- `pushed_at`

## Conversation Record

Path: `state/runtime/conversations/<conversation_id>.json`

Required fields:

- `conversation_id`
- `app_id`
- `title`
- `source`
- `status`
- `created_at`
- `updated_at`
- `latest_job_id`
- `messages`
- `events`

### Conversation Message Shape

Required fields:

- `message_id`
- `role`
- `type`
- `title`
- `body`
- `job_id`
- `created_at`
- `metadata`

Expected metadata fields when the message type is `request`:

- `source`
- `intent_summary`
- `ux_context`

### Conversation Event Shape

Required fields:

- `event_id`
- `type`
- `status`
- `body`
- `job_id`
- `created_at`
- `data`

## Engineering Log

Path: `state/engineering-log.md`

Each appended section should include:

- timestamp
- app id
- title
- job id
- request id
- goal
- system_area
- decision
- why
- tradeoff
- issue_encountered
- verification
- follow_up

## Compatibility Rule

If a change needs to alter one of these shapes:

1. update this document
2. update the code that creates the payload
3. update the verification contract if the shape is externally visible
4. document whether old state files remain readable

## Intent Summary Shape

`intent_summary` is the current persisted interpretation layer between raw user wording and implementation.

Required fields:

- `explicit_request`
- `interpreted_outcome`
- `assumptions`
- `ambiguity`
- `success_signal`

## UX Context Shape

`ux_context` is optional and is used only when the user is describing friction in the UI.

Expected fields:

- `affected_surface`
- `pain_points`
- `note`
- `desired_feel`

## UX Review Shape

`ux_review` is optional and should appear on jobs or proposals when the request touches UI or usability.

Expected fields:

- `primary_journey`
- `pain_interpretation`
- `friction_points`
- `simplification`
- `mobile_risk`
- `verification_steps`
