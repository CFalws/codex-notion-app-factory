from __future__ import annotations

import json
import re
from typing import Any

from .config import RuntimeSettings

ENGINEERING_LOG_START = "ENGINEERING_LOG_JSON_START"
ENGINEERING_LOG_END = "ENGINEERING_LOG_JSON_END"
ENGINEERING_LOG_FIELDS = (
    "goal",
    "system_area",
    "decision",
    "why",
    "tradeoff",
    "issue_encountered",
    "verification",
    "follow_up",
)
INTENT_SUMMARY_FIELDS = (
    "explicit_request",
    "interpreted_outcome",
    "assumptions",
    "ambiguity",
    "success_signal",
)
GOAL_REVIEW_START = "GOAL_REVIEW_JSON_START"
GOAL_REVIEW_END = "GOAL_REVIEW_JSON_END"
GOAL_REVIEW_FIELDS = (
    "hypothesis",
    "verification_result",
    "comparison_to_previous",
    "continue_recommended",
    "alignment_assessment",
    "safety_assessment",
    "next_focus",
)


def is_proposal_mode(record: dict[str, Any]) -> bool:
    return str(record.get("execution_mode", "")).strip() == "proposal"


def allowed_paths_text(record: dict[str, Any]) -> str:
    allowed_paths = record.get("allowed_paths") or []
    if not allowed_paths:
        return "- No explicit path allowlist was provided."
    return "\n".join(f"- {path}" for path in allowed_paths)


def build_instructions(
    settings: RuntimeSettings,
    record: dict[str, Any],
    *,
    job_context: dict[str, str] | None = None,
) -> str:
    source_path = record.get("source_path") or "(not set)"
    workspace_path = record.get("workspace_path") or "(not set)"
    deployment_url = record.get("deployment_url") or "(not deployed yet)"
    summary = record.get("last_summary") or "No prior summary."
    proposal_lines = ""
    if is_proposal_mode(record) and job_context is not None:
        proposal_lines = f"""
Proposal mode context:
- Worktree path: {job_context["worktree_path"]}
- Proposal branch: {job_context["branch_name"]}
- Base branch: {job_context["base_branch"]}
- Allowed paths:
{allowed_paths_text(record)}

Proposal rules:
- Work only inside the proposal worktree.
- Restrict edits to the allowed paths when they are provided.
- Create a git commit on the proposal branch before finishing.
- Do not deploy, merge, or restart services yourself.
""".strip()
    return f"""
You are maintaining one app inside a stateful personal app factory repository.

Repository root: {settings.repo_root}
Target app id: {record["app_id"]}
Target app title: {record["title"]}
Source path: {source_path}
Workspace path: {workspace_path}
Deployment URL: {deployment_url}
Last summary: {summary}

Rules:
- Work only inside this repository.
- Prefer continuity with the existing app instead of rebuilding from scratch.
- Keep the web app deployable through GitHub Pages after code changes.
- If the request is ambiguous, make the smallest reasonable assumption and proceed.
- Summarize exactly what changed and any follow-up needed.
{proposal_lines if proposal_lines else ""}
""".strip()


def build_prompt(
    settings: RuntimeSettings,
    record: dict[str, Any],
    request_payload: dict[str, Any],
    *,
    job_context: dict[str, str] | None = None,
) -> str:
    intent_summary = request_payload.get("intent_summary") or {}
    interpreted_intent = ""
    if intent_summary:
        interpreted_intent = f"""
Interpreted intent:
- Explicit request: {intent_summary.get("explicit_request", "(not set)")}
- Interpreted outcome: {intent_summary.get("interpreted_outcome", "(not set)")}
- Assumptions: {intent_summary.get("assumptions", "(not set)")}
- Ambiguity: {intent_summary.get("ambiguity", "(not set)")}
- Success signal: {intent_summary.get("success_signal", "(not set)")}
""".strip()
    proposal_tail = ""
    if is_proposal_mode(record):
        proposal_tail = """
Before finishing:
1. stage your changes,
2. create exactly one commit on the proposal branch,
3. include the final commit hash in the summary,
4. mention whether the proposal is ready to apply.
""".strip()
    goal_loop = request_payload.get("goal_loop") or {}
    goal_tail = ""
    if goal_loop:
        goal_tail = f"""
Because this request is part of an autonomous goal loop, also append a machine-readable goal review block before the engineering log.
Rules for the goal review block:
- Use the exact marker line {GOAL_REVIEW_START}
- Follow it with a valid JSON object
- Use only these keys: hypothesis, verification_result, comparison_to_previous, continue_recommended, alignment_assessment, safety_assessment, next_focus
- Put plain strings in every field
- `continue_recommended` must be either `yes` or `no`
- Close with the exact marker line {GOAL_REVIEW_END}
""".strip()
    return f"""
{build_instructions(settings, record, job_context=job_context)}

Continue work on the existing app lane.

App id: {record["app_id"]}
App title: {record["title"]}
Request source: {request_payload["source"]}
Conversation id: {request_payload.get("conversation_id", "") or "(new conversation)"}

Request:
{request_payload["request_text"]}

{interpreted_intent if interpreted_intent else ""}

After completing the work, provide:
1. the key code changes,
2. any deployment-impacting notes,
3. the next best follow-up action if the work should continue.

{goal_tail if goal_tail else ""}

Then append a machine-readable engineering log block at the very end of your final answer.
Rules for the block:
- Use the exact marker line {ENGINEERING_LOG_START}
- Follow it with a valid JSON object
- Use only these keys: goal, system_area, decision, why, tradeoff, issue_encountered, verification, follow_up
- Put plain strings in every field
- Do not wrap the JSON in markdown fences
- Close with the exact marker line {ENGINEERING_LOG_END}
{proposal_tail if proposal_tail else ""}
""".strip()


_ABSOLUTE_PATH_PREFIXES = (
    "/var/lib/codex-factory/state/runtime/worktrees/",
    "/opt/codex-app-factory/",
    "/Users/emil/emil/python/codex-app-factory/",
    "/Users/emil/emil/python/codex-notion-app-factory/",
)


def sanitize_user_facing_text(text: str) -> str:
    cleaned = str(text or "").strip()
    if not cleaned:
        return ""

    cleaned = re.sub(
        r"\[([^\]]+)\]\((/var/lib/codex-factory/state/runtime/worktrees/[^)]+|/opt/codex-app-factory/[^)]+|/Users/emil/emil/python/codex-(?:notion-)?app-factory/[^)]+)\)",
        r"\1",
        cleaned,
    )
    cleaned = re.sub(r"`([^`]+)`", r"\1", cleaned)
    cleaned = cleaned.replace("**", "")
    cleaned = cleaned.replace("### ", "").replace("## ", "").replace("# ", "")
    cleaned = re.sub(r"/var/lib/codex-factory/state/runtime/worktrees/[0-9a-f]+/", "", cleaned)
    for prefix in _ABSOLUTE_PATH_PREFIXES[1:]:
        cleaned = cleaned.replace(prefix, "")
    cleaned = cleaned.replace(
        "https://cfalws.github.io/codex-notion-app-factory/examples/generated_apps/",
        "https://cfalws.github.io/codex-app-factory/",
    )
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def infer_intent_summary(record: dict[str, Any], request_payload: dict[str, Any]) -> dict[str, str]:
    request_text = str(request_payload.get("request_text") or "").strip()
    explicit_title = str(request_payload.get("title") or "").strip()
    first_line = next((line.strip() for line in request_text.splitlines() if line.strip()), "")
    explicit_request = explicit_title or first_line or "Continue the current app lane."
    compact_request = " ".join(explicit_request.split())
    if len(compact_request) > 96:
        compact_request = compact_request[:93].rstrip() + "..."

    app_title = str(record.get("title") or record.get("app_id") or "the current app").strip()
    interpreted_outcome = (
        f"Update {app_title} so the requested behavior is reflected without breaking the existing app lane."
    )

    lower_text = request_text.lower()
    assumptions = (
        "Treat this as continuation work in the existing app lane, preserve phone usability, and prefer the smallest "
        "change that satisfies the request."
    )
    if any(word in lower_text for word in ("backend", "server", "database", "auth", "login")):
        assumptions = (
            "Treat this as continuation work, but allow backend or auth changes if the request clearly requires them. "
            "Preserve deployability and existing operator flow."
        )

    ambiguity = "Low: the request names a concrete change and target lane."
    if len(request_text.split()) < 8:
        ambiguity = "High: the request is short and may hide unstated acceptance criteria."
    elif not any(token in lower_text for token in ("when", "after", "so that", "because", "verify", "show", "open")):
        ambiguity = "Medium: the change is clear enough to start, but acceptance criteria are still partly implicit."

    success_signal = (
        "The visible app or operator flow should match the requested outcome, and the result summary should explain "
        "what changed plus how to verify it from the user side."
    )
    if any(word in lower_text for word in ("do not modify", "no file", "summarize", "explain")):
        success_signal = (
            "The response should satisfy the request without unnecessary file edits, and the result summary should stay "
            "aligned with the no-change intent."
        )

    return {
        "explicit_request": compact_request or "Continue the current app lane.",
        "interpreted_outcome": interpreted_outcome,
        "assumptions": assumptions,
        "ambiguity": ambiguity,
        "success_signal": success_signal,
    }


def extract_engineering_log_json(final_output: str) -> tuple[str, dict[str, Any] | None]:
    start = final_output.find(ENGINEERING_LOG_START)
    if start == -1:
        return final_output.strip(), None
    end = final_output.find(ENGINEERING_LOG_END, start)
    if end == -1:
        return final_output.strip(), None

    json_text = final_output[start + len(ENGINEERING_LOG_START) : end].strip()
    prefix = final_output[:start].rstrip()
    suffix = final_output[end + len(ENGINEERING_LOG_END) :].strip()
    clean_output = prefix if not suffix else f"{prefix}\n\n{suffix}".strip()

    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError:
        return clean_output, None
    if not isinstance(payload, dict):
        return clean_output, None
    return clean_output, payload


def extract_goal_review_json(final_output: str) -> tuple[str, dict[str, Any] | None]:
    start = final_output.find(GOAL_REVIEW_START)
    if start == -1:
        return final_output.strip(), None
    end = final_output.find(GOAL_REVIEW_END, start)
    if end == -1:
        return final_output.strip(), None

    json_text = final_output[start + len(GOAL_REVIEW_START) : end].strip()
    prefix = final_output[:start].rstrip()
    suffix = final_output[end + len(GOAL_REVIEW_END) :].strip()
    clean_output = prefix if not suffix else f"{prefix}\n\n{suffix}".strip()

    try:
        payload = json.loads(json_text)
    except json.JSONDecodeError:
        return clean_output, None
    if not isinstance(payload, dict):
        return clean_output, None
    return clean_output, payload


def normalize_goal_review(parsed: dict[str, Any] | None) -> dict[str, str]:
    review = {field: "" for field in GOAL_REVIEW_FIELDS}
    if not parsed:
        return review
    for field in GOAL_REVIEW_FIELDS:
        value = parsed.get(field, "")
        text = str(value).strip()
        if text:
            review[field] = text
    if review["continue_recommended"].lower() not in {"yes", "no"}:
        review["continue_recommended"] = ""
    return review


def default_decision_summary(
    request_payload: dict[str, Any],
    *,
    clean_summary: str = "",
    error_message: str = "",
    system_area: str = "execution",
    decision: str = "",
    why: str = "",
    verification: str = "",
    follow_up: str = "",
) -> dict[str, str]:
    sanitized_summary = sanitize_user_facing_text(clean_summary)
    summary_first_line = next((line.strip() for line in sanitized_summary.splitlines() if line.strip()), "")
    return {
        "goal": str(request_payload.get("title") or request_payload.get("request_text") or "Continue the requested app work.").strip(),
        "system_area": system_area,
        "decision": decision or summary_first_line or ("Run failed before a final summary." if error_message else "Applied the requested change."),
        "why": why or "Keep the app lane moving with the smallest reasonable change.",
        "tradeoff": "",
        "issue_encountered": error_message,
        "verification": verification or ("job failed" if error_message else "job completed"),
        "follow_up": follow_up,
    }


def normalize_decision_summary(
    request_payload: dict[str, Any],
    parsed: dict[str, Any] | None,
    *,
    clean_summary: str,
    error_message: str = "",
    system_area: str = "execution",
    decision: str = "",
    why: str = "",
    verification: str = "",
    follow_up: str = "",
) -> dict[str, str]:
    summary = default_decision_summary(
        request_payload,
        clean_summary=clean_summary,
        error_message=error_message,
        system_area=system_area,
        decision=decision,
        why=why,
        verification=verification,
        follow_up=follow_up,
    )
    if not parsed:
        return summary
    for field in ENGINEERING_LOG_FIELDS:
        value = parsed.get(field, "")
        if isinstance(value, list):
            text = ", ".join(str(item).strip() for item in value if str(item).strip())
        else:
            text = str(value).strip()
        if text:
            summary[field] = text
    return summary


def build_failure_message(returncode: int, stdout_text: str, stderr_text: str) -> str:
    for source in (stderr_text, stdout_text):
        for line in reversed(source.splitlines()):
            line = line.strip()
            if line:
                return f"codex exec failed with exit code {returncode}: {line}"
    return f"codex exec failed with exit code {returncode}."
