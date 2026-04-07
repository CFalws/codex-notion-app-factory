from __future__ import annotations

import re
from dataclasses import dataclass


DEFAULT_TIMER_SECONDS = 180


@dataclass(frozen=True)
class MomentumResult:
    task: str
    first_action: str
    timer_seconds: int


def normalize_task(task: str) -> str:
    return " ".join(task.strip().split())


def _category_action(task: str) -> str:
    lower = task.lower()
    if any(word in lower for word in ("clean", "kitchen", "laundry", "room", "dish")):
        return "Clear one small surface or put one item back where it belongs."
    if any(word in lower for word in ("email", "reply", "message", "inbox")):
        return "Open your inbox and answer the shortest pending message first."
    if any(word in lower for word in ("study", "math", "read", "learn", "homework")):
        return "Open your notes and complete just the first tiny item you see."
    if any(word in lower for word in ("code", "bug", "app", "project", "landing")):
        return "Open the project and finish the smallest visible code change first."
    if any(word in lower for word in ("workout", "exercise", "run", "stretch")):
        return "Stand up, get into position, and do the first minute only."
    return ""


def generate_momentum(task: str) -> MomentumResult:
    cleaned = normalize_task(task)
    if not cleaned:
        return MomentumResult(task="", first_action="", timer_seconds=DEFAULT_TIMER_SECONDS)

    action = _category_action(cleaned)
    if not action:
        fragment = re.sub(r"^(to|start|begin)\s+", "", cleaned.lower().strip(" .,!?:;"))
        action = f"Open the place where '{fragment}' happens and do the first visible action only."

    return MomentumResult(
        task=cleaned,
        first_action=action,
        timer_seconds=DEFAULT_TIMER_SECONDS,
    )
