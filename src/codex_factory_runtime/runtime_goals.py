from __future__ import annotations

from typing import Any


class GoalRuntime:
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

    def next_goal_status(self, goal: dict[str, Any], job: dict[str, Any]) -> tuple[str, str]:
        iteration_number = int(goal.get("current_iteration") or 0)
        max_iterations = int(goal.get("max_iterations") or 0)
        goal_review = job.get("goal_review") or {}
        if job.get("status") != "completed":
            return "failed", "job_failed"
        if job.get("proposal"):
            return "paused", "proposal_ready"
        if str(goal_review.get("safety_assessment") or "").strip().lower().startswith("no"):
            return "paused", "safety_not_passed"
        if str(goal_review.get("alignment_assessment") or "").strip().lower().startswith("no"):
            return "paused", "alignment_not_passed"
        if str(goal_review.get("continue_recommended") or "").strip().lower() == "no":
            return "completed", "goal_review_stop"
        if max_iterations > 0 and iteration_number >= max_iterations:
            return "completed", "max_iterations_reached"
        return "running", ""
