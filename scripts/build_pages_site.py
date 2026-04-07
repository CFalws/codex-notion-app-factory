#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GENERATED_APPS_DIR = REPO_ROOT / "examples" / "generated_apps"
OUTPUT_DIR = REPO_ROOT / ".pages-dist"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def app_entries() -> list[dict]:
    entries: list[dict] = []
    for app_dir in sorted(GENERATED_APPS_DIR.iterdir()):
        if not app_dir.is_dir():
            continue
        web_dir = app_dir / "web"
        spec_path = app_dir / "app_spec.json"
        if not web_dir.exists() or not spec_path.exists():
            continue
        spec = read_json(spec_path)
        entries.append(
            {
                "slug": spec["slug"],
                "name": spec["app_name"],
                "description": spec.get("idea", "").strip(),
                "delivery_target": spec.get("delivery_target", "installable-pwa"),
                "source_dir": app_dir,
                "web_dir": web_dir,
            }
        )
    return entries


def reset_output_dir() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def copy_app_web(entry: dict) -> None:
    destination = OUTPUT_DIR / entry["slug"]
    shutil.copytree(entry["web_dir"], destination)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_index(entries: list[dict]) -> str:
    cards = []
    for entry in entries:
        cards.append(
            f"""
            <a class="card" href="./{entry["slug"]}/">
              <p class="card-kicker">{entry["delivery_target"]}</p>
              <h2>{entry["name"]}</h2>
              <p>{entry["description"]}</p>
              <span>Open app</span>
            </a>
            """
        )

    return textwrap.dedent(
        f"""\
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Generated Apps</title>
            <style>
              :root {{
                --bg: #f7f1e8;
                --ink: #18222a;
                --muted: #5f6d77;
                --card: rgba(255, 251, 246, 0.86);
                --line: rgba(24, 34, 42, 0.08);
                --shadow: 0 18px 60px rgba(24, 34, 42, 0.12);
                font-family: ui-sans-serif, system-ui, sans-serif;
              }}
              * {{ box-sizing: border-box; }}
              body {{
                margin: 0;
                min-height: 100vh;
                color: var(--ink);
                background:
                  radial-gradient(circle at top left, rgba(243, 177, 74, 0.32), transparent 28%),
                  radial-gradient(circle at top right, rgba(59, 150, 171, 0.25), transparent 24%),
                  linear-gradient(180deg, #fbf7ef 0%, #eee6d7 100%);
              }}
              main {{
                width: min(100%, 72rem);
                margin: 0 auto;
                padding: 2rem 1rem 3rem;
              }}
              h1, h2, p {{ margin: 0; }}
              .hero {{
                max-width: 42rem;
                padding: 1rem 0 2rem;
              }}
              .hero h1 {{
                font-size: clamp(2.4rem, 7vw, 4.6rem);
                line-height: 0.94;
              }}
              .hero p {{
                margin-top: 0.85rem;
                line-height: 1.6;
                color: var(--muted);
              }}
              .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
                gap: 1rem;
              }}
              .card {{
                display: block;
                text-decoration: none;
                color: inherit;
                background: var(--card);
                border: 1px solid var(--line);
                border-radius: 1.5rem;
                padding: 1.1rem;
                box-shadow: var(--shadow);
              }}
              .card-kicker {{
                color: var(--muted);
                text-transform: uppercase;
                font-size: 0.78rem;
                letter-spacing: 0.08em;
              }}
              .card h2 {{
                margin-top: 0.5rem;
                font-size: 1.3rem;
              }}
              .card p {{
                margin-top: 0.65rem;
                line-height: 1.55;
                color: var(--muted);
              }}
              .card span {{
                display: inline-block;
                margin-top: 1rem;
                font-weight: 700;
              }}
            </style>
          </head>
          <body>
            <main>
              <section class="hero">
                <p>Codex Notion App Factory</p>
                <h1>Generated Apps</h1>
                <p>
                  This site is assembled from the repository's generated app outputs and deployed with GitHub Pages.
                  Each card links to a phone-usable app shell.
                </p>
              </section>
              <section class="grid">
                {"".join(cards)}
              </section>
            </main>
          </body>
        </html>
        """
    )


def main() -> None:
    entries = app_entries()
    reset_output_dir()
    for entry in entries:
        copy_app_web(entry)
    write_file(OUTPUT_DIR / "index.html", build_index(entries))
    write_file(OUTPUT_DIR / ".nojekyll", "")
    print(f"Built Pages site with {len(entries)} app(s) at {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
