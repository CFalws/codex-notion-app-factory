from __future__ import annotations

import json
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
    proposal_tail = ""
    if is_proposal_mode(record):
        proposal_tail = """
Before finishing:
1. stage your changes,
2. create exactly one commit on the proposal branch,
3. include the final commit hash in the summary,
4. mention whether the proposal is ready to apply.
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

After completing the work, provide:
1. the key code changes,
2. any deployment-impacting notes,
3. the next best follow-up action if the work should continue.

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
    summary_first_line = next((line.strip() for line in clean_summary.splitlines() if line.strip()), "")
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
