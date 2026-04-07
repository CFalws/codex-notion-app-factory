from __future__ import annotations

import re
from dataclasses import dataclass


GENERIC_FALLBACK = (
    "Set a two-minute timer, open the place where this task happens, "
    "and do the smallest visible action."
)


@dataclass(frozen=True)
class LaunchResult:
    task: str
    first_action: str


def normalize_task(task: str) -> str:
    cleaned = " ".join(task.strip().split())
    return cleaned


def _prefix_for(task: str) -> str:
    lower = task.lower()
    if any(word in lower for word in ("clean", "kitchen", "laundry", "wash", "dish", "room")):
        return "Put one item back in place or clear one small surface."
    if any(word in lower for word in ("email", "inbox", "reply", "message")):
        return "Open your inbox and answer the shortest pending message."
    if any(word in lower for word in ("study", "learn", "read", "homework", "math")):
        return "Open your notes or book and finish just the first tiny item."
    if any(word in lower for word in ("workout", "exercise", "run", "stretch")):
        return "Put on your shoes or stand on the mat and start with one minute."
    if any(word in lower for word in ("code", "project", "build", "bug", "app")):
        return "Open the project and fix or write the smallest visible piece first."
    return ""


def _trimmed_fragment(task: str) -> str:
    lowered = task.lower().strip(" .,!?")
    lowered = re.sub(r"^(to|start|begin)\s+", "", lowered)
    return lowered


def generate_first_action(task: str) -> LaunchResult:
    cleaned = normalize_task(task)
    if not cleaned:
        return LaunchResult(task="", first_action="")

    prefix = _prefix_for(cleaned)
    fragment = _trimmed_fragment(cleaned)

    if prefix:
        action = prefix
    elif len(fragment.split()) <= 4:
        action = f"Open the place where you do '{fragment}' and do the first visible step."
    else:
        action = GENERIC_FALLBACK

    return LaunchResult(task=cleaned, first_action=action)
