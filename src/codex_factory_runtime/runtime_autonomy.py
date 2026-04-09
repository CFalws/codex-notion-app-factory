from __future__ import annotations

import json
from typing import Any

AUTONOMY_PROPOSAL_START = "AUTONOMY_PROPOSAL_JSON_START"
AUTONOMY_PROPOSAL_END = "AUTONOMY_PROPOSAL_JSON_END"
AUTONOMY_REVIEW_START = "AUTONOMY_REVIEW_JSON_START"
AUTONOMY_REVIEW_END = "AUTONOMY_REVIEW_JSON_END"
AUTONOMY_VERIFY_START = "AUTONOMY_VERIFY_JSON_START"
AUTONOMY_VERIFY_END = "AUTONOMY_VERIFY_JSON_END"

AUTONOMY_PROPOSAL_FIELDS = (
    "hypothesis",
    "target_area",
    "change_outline",
    "success_criteria",
    "why_now",
)
AUTONOMY_REVIEW_FIELDS = (
    "verdict",
    "rationale",
    "blocking_issue",
    "suggested_adjustment",
)
AUTONOMY_VERIFY_FIELDS = (
    "verdict",
    "path_acceptability",
    "evidence",
    "residual_risk",
    "follow_up",
)


def _extract_json_block(text: str, start: str, end: str) -> tuple[str, dict[str, Any] | None]:
    source = str(text or "")
    start_index = source.find(start)
    end_index = source.find(end)
    if start_index == -1 or end_index == -1 or end_index < start_index:
        return source.strip(), None
    json_payload = source[start_index + len(start) : end_index].strip()
    cleaned = (source[:start_index] + source[end_index + len(end) :]).strip()
    try:
        parsed = json.loads(json_payload)
    except json.JSONDecodeError:
        return cleaned, None
    if not isinstance(parsed, dict):
        return cleaned, None
    return cleaned, parsed


def normalize_fields(parsed: dict[str, Any] | None, fields: tuple[str, ...]) -> dict[str, str]:
    return {field: str((parsed or {}).get(field) or "").strip() for field in fields}


def extract_proposal_json(text: str) -> tuple[str, dict[str, Any] | None]:
    return _extract_json_block(text, AUTONOMY_PROPOSAL_START, AUTONOMY_PROPOSAL_END)


def extract_review_json(text: str) -> tuple[str, dict[str, Any] | None]:
    return _extract_json_block(text, AUTONOMY_REVIEW_START, AUTONOMY_REVIEW_END)


def extract_verify_json(text: str) -> tuple[str, dict[str, Any] | None]:
    return _extract_json_block(text, AUTONOMY_VERIFY_START, AUTONOMY_VERIFY_END)


def normalize_proposal_json(parsed: dict[str, Any] | None) -> dict[str, str]:
    normalized = normalize_fields(parsed, AUTONOMY_PROPOSAL_FIELDS)
    if not normalized["hypothesis"]:
        normalized["hypothesis"] = "No bounded hypothesis was provided."
    if not normalized["success_criteria"]:
        normalized["success_criteria"] = "No explicit success criteria were provided."
    return normalized


def normalize_review_json(parsed: dict[str, Any] | None) -> dict[str, str]:
    normalized = normalize_fields(parsed, AUTONOMY_REVIEW_FIELDS)
    verdict = normalized["verdict"].lower()
    normalized["verdict"] = "approve" if verdict == "approve" else "reject"
    return normalized


def normalize_verify_json(parsed: dict[str, Any] | None) -> dict[str, str]:
    normalized = normalize_fields(parsed, AUTONOMY_VERIFY_FIELDS)
    verdict = normalized["verdict"].lower()
    normalized["verdict"] = "pass" if verdict == "pass" else "fail"
    acceptability = normalized["path_acceptability"].lower()
    normalized["path_acceptability"] = acceptability if acceptability in {"acceptable", "disqualifying"} else ""
    return normalized


class AutonomyRuntime:
    def _summarize_iteration_for_proposer(self, item: dict[str, Any]) -> str:
        review = item.get("goal_review") or {}
        intended_path = item.get("intended_path") or {}
        verifier_reviews = item.get("verification_reviews") or []
        degraded_signals = ", ".join(str(signal).strip() for signal in (intended_path.get("degraded_signals") or []) if str(signal).strip()) or "(none)"
        verifier_verdicts = ", ".join(
            sorted({str(review.get("verdict") or "").strip() for review in verifier_reviews if str(review.get("verdict") or "").strip()})
        ) or "(none)"
        verifier_acceptability = ", ".join(
            sorted(
                {
                    str(review.get("path_acceptability") or "").strip()
                    for review in verifier_reviews
                    if str(review.get("path_acceptability") or "").strip()
                }
            )
        ) or "(none)"
        return (
            f"- iteration {item.get('iteration')}: "
            f"status={str(item.get('status') or '').strip() or '(unknown)'} | "
            f"blocker={str(item.get('continuation_blocker_reason') or 'none').strip() or 'none'} | "
            f"intended_path={str(intended_path.get('verdict') or '').strip() or '(missing)'} | "
            f"degraded_signals={degraded_signals} | "
            f"verifier_verdicts={verifier_verdicts} | "
            f"verifier_path_acceptability={verifier_acceptability} | "
            f"next_focus={str(review.get('next_focus') or '').strip() or '(none)'} | "
            f"summary={str(item.get('result_summary') or '').strip() or '(no summary)'}"
        )

    def build_proposer_prompt(self, goal: dict[str, Any], app_record: dict[str, Any]) -> str:
        app_title = str(app_record.get("title") or app_record.get("app_id") or "the app").strip()
        prior_iterations = goal.get("iterations") or []
        prior_lines: list[str] = []
        for item in prior_iterations[-3:]:
            prior_lines.append(self._summarize_iteration_for_proposer(item))
        prior_text = "\n".join(prior_lines) if prior_lines else "- No prior iterations yet."
        return f"""
You are the proposer in an autonomous software-improvement pipeline.

Target app: {app_title}
Goal title: {goal.get("title") or app_title}
Goal objective:
{str(goal.get("objective") or "").strip()}

Prior iterations:
{prior_text}

Use the latest structured blocker, intended-path, and verifier evidence when choosing the next bounded hypothesis. If the last iteration paused, degraded, or was rejected, ground the next proposal in that explicit failure signal rather than only in prose summary.

Your task:
- Choose exactly one bounded change hypothesis that most improves progress toward the goal.
- Prefer a small, verifiable change over a broad refactor.
- Do not modify files.
- Do not stage, commit, deploy, or restart anything.

Return a concise human summary followed by a machine-readable proposal block.

Proposal block rules:
- Use the exact marker line {AUTONOMY_PROPOSAL_START}
- Follow it with a valid JSON object
- Use only these keys: hypothesis, target_area, change_outline, success_criteria, why_now
- Put plain strings in every field
- Close with the exact marker line {AUTONOMY_PROPOSAL_END}
""".strip()

    def build_reviewer_prompt(
        self,
        goal: dict[str, Any],
        app_record: dict[str, Any],
        proposal: dict[str, str],
        *,
        reviewer_name: str,
    ) -> str:
        return f"""
You are {reviewer_name} in an autonomous software-improvement pipeline.

Target app: {app_record.get("title") or app_record.get("app_id")}
Goal objective: {str(goal.get("objective") or "").strip()}

Review this bounded proposal:
Hypothesis: {proposal.get("hypothesis", "")}
Target area: {proposal.get("target_area", "")}
Change outline: {proposal.get("change_outline", "")}
Success criteria: {proposal.get("success_criteria", "")}
Why now: {proposal.get("why_now", "")}

Rules:
- Approve only if the proposal is bounded, useful, and low risk.
- Reject if it is too broad, vague, or likely to degrade the app.
- Do not modify files.
- Reply with one short summary sentence.
- Then output a JSON review block.

JSON review block:
{AUTONOMY_REVIEW_START}
{{"verdict":"approve or reject","rationale":"...","blocking_issue":"...","suggested_adjustment":"..."}}
{AUTONOMY_REVIEW_END}
""".strip()

    def build_implementation_request(
        self,
        goal: dict[str, Any],
        app_record: dict[str, Any],
        proposal: dict[str, str],
        *,
        iteration_number: int,
    ) -> tuple[str, str]:
        app_title = str(app_record.get("title") or app_record.get("app_id") or "the app").strip()
        title = f"{goal.get('title') or app_title} · Iteration {iteration_number}"
        request = f"""
Autonomous improvement goal for {app_title}

Goal:
{goal.get("objective", "").strip()}

Iteration:
- Current iteration: {iteration_number}
- Max iterations: {int(goal.get("max_iterations") or 0)}

Approved bounded hypothesis:
- Hypothesis: {proposal.get("hypothesis", "")}
- Target area: {proposal.get("target_area", "")}
- Change outline: {proposal.get("change_outline", "")}
- Success criteria: {proposal.get("success_criteria", "")}
- Why now: {proposal.get("why_now", "")}

Execution rules:
- Implement only this approved bounded hypothesis.
- Verify the result against the success criteria before finishing.
- If the hypothesis proves wrong, explain why instead of broadening scope.
- If a next iteration is still worthwhile, say what the next best focus should be.
- If the goal is effectively satisfied or blocked, say so clearly.
""".strip()
        return title, request

    def build_verifier_prompt(
        self,
        goal: dict[str, Any],
        app_record: dict[str, Any],
        proposal: dict[str, str],
        implementation_summary: str,
        *,
        verifier_name: str,
        intended_path: dict[str, Any] | None = None,
    ) -> str:
        path = intended_path or {}
        degraded_signals = ", ".join(path.get("degraded_signals") or []) or "(none)"
        return f"""
You are {verifier_name} in an autonomous software-improvement pipeline.

Target app: {app_record.get("title") or app_record.get("app_id")}
Goal objective: {str(goal.get("objective") or "").strip()}

Verify this implementation against the approved hypothesis:
Hypothesis: {proposal.get("hypothesis", "")}
Target area: {proposal.get("target_area", "")}
Change outline: {proposal.get("change_outline", "")}
Success criteria: {proposal.get("success_criteria", "")}

Implementation summary:
{implementation_summary.strip() or "(no summary)"}

Structured intended-path verdict:
- expected_path: {str(path.get("expected_path") or "").strip() or "(missing)"}
- degraded_signals: {degraded_signals}
- verdict: {str(path.get("verdict") or "").strip() or "(missing)"}

Rules:
- Inspect the current proposal worktree.
- Pass only if the approved hypothesis is actually satisfied.
- Explicitly judge whether the observed execution path was acceptable or disqualifying.
- Fail if the change is incomplete, too broad, or risky.
- Do not modify files.
- Reply with one short summary sentence.
- Then output a JSON verification block.

JSON verification block:
{AUTONOMY_VERIFY_START}
{{"verdict":"pass or fail","path_acceptability":"acceptable or disqualifying","evidence":"...","residual_risk":"...","follow_up":"..."}}
{AUTONOMY_VERIFY_END}
""".strip()
