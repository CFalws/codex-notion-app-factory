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
                "theme_color": spec.get("theme_color", "#177e89"),
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


def build_collection_icon() -> str:
    return textwrap.dedent(
        """\
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
          <rect width="512" height="512" rx="128" fill="#172127" />
          <defs>
            <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#f3b14a" />
              <stop offset="100%" stop-color="#177e89" />
            </linearGradient>
          </defs>
          <rect x="92" y="102" width="140" height="140" rx="42" fill="url(#g1)" />
          <rect x="280" y="102" width="140" height="140" rx="42" fill="#fff7e8" opacity="0.96" />
          <rect x="92" y="270" width="140" height="140" rx="42" fill="#fff7e8" opacity="0.96" />
          <rect x="280" y="270" width="140" height="140" rx="42" fill="url(#g1)" />
          <path d="M146 176h32l24 28 50-58" fill="none" stroke="#ffffff" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" />
          <circle cx="350" cy="172" r="20" fill="#172127" />
          <circle cx="162" cy="340" r="20" fill="#172127" />
          <path d="M320 338h58" stroke="#ffffff" stroke-width="22" stroke-linecap="round" />
          <path d="M349 309v58" stroke="#ffffff" stroke-width="22" stroke-linecap="round" />
          <title>앱 모음</title>
        </svg>
        """
    )


def build_root_manifest() -> str:
    payload = {
        "name": "앱 모음",
        "short_name": "앱 모음",
        "description": "생성된 개인용 앱들을 한곳에 모아 홈 화면에서 바로 여는 런처입니다.",
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#f7f1e8",
        "theme_color": "#172127",
        "icons": [
            {"src": "./collection-icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"},
            {"src": "./apple-touch-icon.svg", "sizes": "180x180", "type": "image/svg+xml"},
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def build_root_app_js() -> str:
    return textwrap.dedent(
        """\
        const installButton = document.getElementById("install-button");
        let deferredInstallPrompt = null;

        window.addEventListener("beforeinstallprompt", (event) => {
          event.preventDefault();
          deferredInstallPrompt = event;
          installButton.hidden = false;
        });

        installButton.addEventListener("click", async () => {
          if (!deferredInstallPrompt) {
            return;
          }

          deferredInstallPrompt.prompt();
          await deferredInstallPrompt.userChoice;
          deferredInstallPrompt = null;
          installButton.hidden = true;
        });

        if ("serviceWorker" in navigator) {
          window.addEventListener("load", () => {
            navigator.serviceWorker.register("./service-worker.js").catch(() => {});
          });
        }
        """
    )


def build_root_service_worker(entries: list[dict]) -> str:
    cached_paths = [
        "./",
        "./index.html",
        "./manifest.webmanifest",
        "./collection-icon.svg",
        "./apple-touch-icon.svg",
        "./app.js",
    ]
    cached_paths.extend(f"./{entry['slug']}/" for entry in entries)
    assets = ",\n".join(f'  "{path}"' for path in cached_paths)
    return textwrap.dedent(
        f"""\
        const CACHE_NAME = "generated-apps-launcher-v1";
        const ASSETS = [
        {assets}
        ];

        self.addEventListener("install", (event) => {{
          event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
          self.skipWaiting();
        }});

        self.addEventListener("activate", (event) => {{
          event.waitUntil(
            caches.keys().then((keys) =>
              Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))),
            ),
          );
          self.clients.claim();
        }});

        self.addEventListener("fetch", (event) => {{
          if (event.request.method !== "GET") {{
            return;
          }}

          event.respondWith(
            caches.match(event.request).then((cached) => {{
              if (cached) {{
                return cached;
              }}

              return fetch(event.request).catch(() => caches.match("./index.html"));
            }}),
          );
        }});
        """
    )


def build_index(entries: list[dict]) -> str:
    cards = []
    for entry in entries:
        card_icon = entry["name"][:2].upper()
        cards.append(
            f"""
            <a class="card" href="./{entry["slug"]}/">
              <div class="card-top">
                <div class="card-icon" style="--card-accent: {entry["theme_color"]};">{card_icon}</div>
                <p class="card-kicker">{entry["delivery_target"]}</p>
              </div>
              <h2>{entry["name"]}</h2>
              <p>{entry["description"]}</p>
              <span>앱 열기</span>
            </a>
            """
        )

    return textwrap.dedent(
        f"""\
        <!doctype html>
        <html lang="ko">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <meta name="theme-color" content="#172127" />
            <meta name="description" content="생성된 개인용 앱들을 한곳에 모아 홈 화면에서 바로 여는 런처입니다." />
            <title>생성된 앱 목록</title>
            <link rel="manifest" href="./manifest.webmanifest" />
            <link rel="apple-touch-icon" href="./apple-touch-icon.svg" />
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
              .install-button {{
                margin-top: 1rem;
                border: 0;
                border-radius: 999px;
                background: #172127;
                color: #ffffff;
                padding: 0.9rem 1.2rem;
                font: inherit;
                font-weight: 700;
                cursor: pointer;
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
              .card-top {{
                display: flex;
                align-items: center;
                gap: 0.8rem;
              }}
              .card-icon {{
                width: 3rem;
                height: 3rem;
                border-radius: 1rem;
                display: grid;
                place-items: center;
                font-weight: 800;
                color: #ffffff;
                background: var(--card-accent);
                flex-shrink: 0;
              }}
              .card-kicker {{
                color: var(--muted);
                text-transform: uppercase;
                font-size: 0.78rem;
                letter-spacing: 0.08em;
              }}
              .card h2 {{
                margin-top: 0.8rem;
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
                <h1>앱 모음</h1>
                <p>
                  생성된 개인용 앱들을 한곳에 모아 홈 화면에서 바로 여는 런처입니다.
                  자주 쓰는 앱을 빠르게 열 수 있도록 설치 가능한 컬렉션 페이지로 구성했습니다.
                </p>
                <button id="install-button" class="install-button" hidden>앱 모음 설치</button>
              </section>
              <section class="grid">
                {"".join(cards)}
              </section>
            </main>
            <script src="./app.js"></script>
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
    write_file(OUTPUT_DIR / "manifest.webmanifest", build_root_manifest())
    icon = build_collection_icon()
    write_file(OUTPUT_DIR / "collection-icon.svg", icon)
    write_file(OUTPUT_DIR / "apple-touch-icon.svg", icon)
    write_file(OUTPUT_DIR / "app.js", build_root_app_js())
    write_file(OUTPUT_DIR / "service-worker.js", build_root_service_worker(entries))
    write_file(OUTPUT_DIR / ".nojekyll", "")
    print(f"Built Pages site with {len(entries)} app(s) at {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
