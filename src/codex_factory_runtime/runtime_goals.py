from __future__ import annotations

from typing import Any


class GoalRuntime:
    DEGRADED_EVENT_TYPES = {
        "codex.exec.retrying": "codex_exec_retrying",
        "runtime.exception": "runtime_exception",
    }

    def resolve_goal_title(self, app_title: str, explicit_title: str, objective: str) -> str:
        if explicit_title.strip():
            return explicit_title.strip()
        first_line = next((line.strip() for line in objective.splitlines() if line.strip()), "")
        compact = " ".join(first_line.split())
        if len(compact) > 64:
            compact = compact[:61].rstrip() + "..."
        return compact or f"{app_title} Improvement Goal"

    def build_iteration_request(self, goal: dict[str, Any], app_record: dict[str, Any]) -> tuple[str, str]:
        iteration_number = int(goal.get("current_iteration") or 0) + 1
        max_iterations = int(goal.get("max_iterations") or 0)
        prior_iterations = goal.get("iterations") or []
        app_title = str(app_record.get("title") or app_record.get("app_id") or "the app").strip()
        prior_lines: list[str] = []
        for item in prior_iterations[-3:]:
            prior_lines.append(
                f"- iteration {item.get('iteration')}: status={item.get('status')} summary={str(item.get('result_summary') or '').strip() or '(none)'}"
            )
        prior_text = "\n".join(prior_lines) if prior_lines else "- No prior iterations yet."
        title = f"{goal.get('title') or app_title} · Iteration {iteration_number}"
        request_text = f"""
Autonomous improvement goal for {app_title}

Goal:
{goal.get("objective", "").strip()}

Iteration:
- Current iteration: {iteration_number}
- Max iterations: {max_iterations}

Prior iteration results:
{prior_text}

Execution rules:
- Choose exactly one bounded hypothesis that most improves progress toward the goal.
- Implement only that hypothesis in this iteration.
- Verify the result before finishing.
- Compare the current result to the prior iteration results.
- If a next iteration is still worthwhile, say what the next best focus should be.
- If the goal is effectively satisfied or blocked, say so clearly.
""".strip()
        return title, request_text

    def assess_iteration_intended_path(
        self,
        *,
        job: dict[str, Any],
        conversation: dict[str, Any],
        proposal: dict[str, Any] | None = None,
        proposal_ready: bool = False,
        proposal_auto_applied: bool = False,
        push_required: bool = False,
    ) -> dict[str, Any]:
        job_id = str(job.get("job_id") or "").strip()
        events = [event for event in (conversation.get("events") or []) if str(event.get("job_id") or "").strip() == job_id]
        degraded_signals: list[str] = []
        for event in events:
            signal = self.DEGRADED_EVENT_TYPES.get(str(event.get("type") or "").strip())
            if signal and signal not in degraded_signals:
                degraded_signals.append(signal)

        resumed_session = any(
            str(event.get("type") or "").strip() == "codex.exec.started"
            and bool((event.get("data") or {}).get("resuming_session"))
            for event in events
        )
        rotated_session = any(str(event.get("type") or "").strip() == "codex.session.updated" for event in events)
        if resumed_session and rotated_session and "unexpected_session_rotation" not in degraded_signals:
            degraded_signals.append("unexpected_session_rotation")

        expected_path = "job_completed_without_degraded_signals"
        if proposal_auto_applied:
            expected_path = "proposal_auto_apply_completed_with_push"
            healthy_apply, degraded_reason = self.auto_apply_health(proposal or {}, push_required=push_required)
            if not healthy_apply and degraded_reason and degraded_reason not in degraded_signals:
                degraded_signals.append(degraded_reason)
        elif proposal_ready:
            expected_path = "proposal_created_and_waiting_for_review"

        verdict = "expected" if not degraded_signals else "degraded"
        return {
            "expected_path": expected_path,
            "degraded_signals": degraded_signals,
            "verdict": verdict,
        }

    def next_goal_status(
        self,
        goal: dict[str, Any],
        job: dict[str, Any],
        *,
        proposal_ready: bool | None = None,
        intended_path: dict[str, Any] | None = None,
    ) -> tuple[str, str]:
        iteration_number = int(goal.get("current_iteration") or 0)
        max_iterations = int(goal.get("max_iterations") or 0)
        goal_review = job.get("goal_review") or {}
        if proposal_ready is None:
            proposal_ready = bool(job.get("proposal"))
        path_verdict = str((intended_path or {}).get("verdict") or "").strip().lower()
        if job.get("status") != "completed":
            return "failed", "job_failed"
        if proposal_ready:
            return "paused", "proposal_ready"
        if not path_verdict:
            return "paused", "intended_path_incomplete"
        if path_verdict != "expected":
            return "paused", "intended_path_degraded"
        if str(goal_review.get("safety_assessment") or "").strip().lower().startswith("no"):
            return "paused", "safety_not_passed"
        if str(goal_review.get("alignment_assessment") or "").strip().lower().startswith("no"):
            return "paused", "alignment_not_passed"
        if str(goal_review.get("continue_recommended") or "").strip().lower() == "no":
            return "completed", "goal_review_stop"
        if max_iterations > 0 and iteration_number >= max_iterations:
            return "completed", "max_iterations_reached"
        return "running", ""

    def can_continue_after_iteration(self, goal: dict[str, Any], *, iteration_number: int) -> bool:
        max_iterations = int(goal.get("max_iterations") or 0)
        return max_iterations == 0 or iteration_number < max_iterations

    def auto_apply_health(self, proposal: dict[str, Any], *, push_required: bool) -> tuple[bool, str]:
        proposal_status = str(proposal.get("status") or "").strip()
        push_status = str(proposal.get("push_status") or "").strip()
        if proposal_status == "applied_local_push_failed" or push_status == "failed":
            return False, "auto_apply_push_failed"
        if proposal_status != "applied":
            return False, "auto_apply_degraded_status"
        if push_required and push_status != "pushed":
            return False, "auto_apply_push_not_confirmed"
        return True, ""
