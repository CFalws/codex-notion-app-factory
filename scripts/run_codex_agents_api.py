#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

import uvicorn


REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from codex_factory_runtime.config import load_settings
from codex_factory_runtime.main import create_app


def main() -> None:
    settings = load_settings()
    uvicorn.run(
        create_app(settings),
        host=settings.host,
        port=settings.port,
    )


if __name__ == "__main__":
    main()
