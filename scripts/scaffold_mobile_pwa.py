#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "examples" / "generated_apps"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "mobile-app"


def title_case(value: str) -> str:
    return " ".join(part.capitalize() for part in re.split(r"[-_\s]+", value) if part)


def infer_name(name: str | None, idea: str) -> str:
    if name:
        return name.strip()
    candidate = idea.split(".")[0].split(",")[0].strip()
    return title_case(candidate[:48]) or "Mobile App"


def build_index_html(app_name: str, short_name: str, description: str, theme_color: str) -> str:
    return textwrap.dedent(
        f"""\
        <!doctype html>
        <html lang="ko">
          <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <meta name="theme-color" content="{theme_color}" />
            <meta name="description" content="{description}" />
            <title>{app_name}</title>
            <link rel="manifest" href="./manifest.webmanifest" />
            <link rel="apple-touch-icon" href="./apple-touch-icon.svg" />
            <link rel="stylesheet" href="./styles.css" />
          </head>
          <body>
            <main class="shell">
              <header class="hero">
                <p class="eyebrow">설치 가능한 개인 도구</p>
                <h1>{app_name}</h1>
                <p class="lede">{description}</p>
                <button id="install-button" class="install-button" hidden>{short_name} 설치</button>
              </header>

              <section class="panel panel--primary">
                <div class="panel-header">
                  <div>
                    <p class="panel-kicker">오늘</p>
                    <h2>내 습관</h2>
                  </div>
                  <p id="today-label" class="today-label"></p>
                </div>

                <form id="habit-form" class="habit-form">
                  <label class="sr-only" for="habit-name">습관 이름</label>
                  <input
                    id="habit-name"
                    name="habit-name"
                    type="text"
                    maxlength="60"
                    placeholder="추적할 습관을 추가하세요"
                    autocomplete="off"
                    required
                  />
                  <button type="submit">추가</button>
                </form>

                <ul id="habit-list" class="habit-list"></ul>
              </section>

              <section class="panel panel--secondary">
                <div class="panel-header">
                  <div>
                    <p class="panel-kicker">개요</p>
                    <h2>진행 현황</h2>
                  </div>
                </div>
                <div class="stats">
                  <article class="stat-card">
                    <p class="stat-label">오늘 완료</p>
                    <p id="completed-count" class="stat-value">0</p>
                  </article>
                  <article class="stat-card">
                    <p class="stat-label">최고 연속 기록</p>
                    <p id="best-streak" class="stat-value">0</p>
                  </article>
                </div>
              </section>
            </main>

            <template id="habit-item-template">
              <li class="habit-item">
                <div class="habit-copy">
                  <p class="habit-name"></p>
                  <p class="habit-meta"></p>
                </div>
                <div class="habit-actions">
                  <button class="check-button" type="button">체크</button>
                  <button class="delete-button" type="button" aria-label="습관 삭제">삭제</button>
                </div>
              </li>
            </template>

            <script src="./app.js"></script>
          </body>
        </html>
        """
    )


def build_styles(theme_color: str) -> str:
    return textwrap.dedent(
        f"""\
        :root {{
          --bg: #f4efe6;
          --ink: #172127;
          --muted: #5a6872;
          --panel: rgba(255, 252, 247, 0.88);
          --line: rgba(23, 33, 39, 0.08);
          --accent: {theme_color};
          --accent-strong: #0e5e6f;
          --success: #1d8f5f;
          --shadow: 0 18px 60px rgba(23, 33, 39, 0.12);
          font-family: "ui-sans-serif", "system-ui", sans-serif;
        }}

        * {{
          box-sizing: border-box;
        }}

        body {{
          margin: 0;
          min-height: 100vh;
          color: var(--ink);
          background:
            radial-gradient(circle at top left, rgba(243, 177, 74, 0.35), transparent 32%),
            radial-gradient(circle at top right, rgba(59, 150, 171, 0.32), transparent 28%),
            linear-gradient(180deg, #f9f5ed 0%, #ede7dc 100%);
        }}

        button,
        input {{
          font: inherit;
        }}

        .shell {{
          width: min(100%, 42rem);
          margin: 0 auto;
          padding: 1.25rem 1rem 2rem;
        }}

        .hero {{
          padding: 1rem 0 1.5rem;
        }}

        .eyebrow,
        .panel-kicker,
        .habit-meta,
        .today-label,
        .stat-label {{
          color: var(--muted);
          letter-spacing: 0.02em;
        }}

        h1,
        h2,
        p {{
          margin: 0;
        }}

        h1 {{
          font-size: clamp(2.3rem, 9vw, 4rem);
          line-height: 0.94;
          margin-top: 0.35rem;
        }}

        .lede {{
          margin-top: 0.85rem;
          font-size: 1rem;
          line-height: 1.5;
          max-width: 34rem;
        }}

        .install-button,
        .habit-form button,
        .check-button,
        .delete-button {{
          border: 0;
          border-radius: 999px;
          cursor: pointer;
        }}

        .install-button,
        .habit-form button,
        .check-button {{
          background: var(--accent);
          color: white;
          padding: 0.85rem 1.1rem;
          font-weight: 700;
        }}

        .install-button {{
          margin-top: 1rem;
        }}

        .delete-button {{
          background: rgba(23, 33, 39, 0.08);
          color: var(--ink);
          padding: 0.75rem 0.95rem;
        }}

        .panel {{
          background: var(--panel);
          backdrop-filter: blur(18px);
          border: 1px solid var(--line);
          border-radius: 1.6rem;
          box-shadow: var(--shadow);
          padding: 1rem;
        }}

        .panel + .panel {{
          margin-top: 1rem;
        }}

        .panel-header,
        .habit-item,
        .stats {{
          display: flex;
          gap: 0.9rem;
        }}

        .panel-header,
        .habit-item {{
          align-items: center;
          justify-content: space-between;
        }}

        .habit-form {{
          display: grid;
          grid-template-columns: 1fr auto;
          gap: 0.75rem;
          margin-top: 1rem;
        }}

        .habit-form input {{
          width: 100%;
          border-radius: 1rem;
          border: 1px solid var(--line);
          background: rgba(255, 255, 255, 0.72);
          padding: 0.95rem 1rem;
          color: var(--ink);
        }}

        .habit-list {{
          list-style: none;
          padding: 0;
          margin: 1rem 0 0;
          display: grid;
          gap: 0.75rem;
        }}

        .habit-item {{
          padding: 0.95rem;
          border-radius: 1.15rem;
          background: rgba(255, 255, 255, 0.74);
          border: 1px solid var(--line);
        }}

        .habit-copy {{
          min-width: 0;
        }}

        .habit-name {{
          font-weight: 700;
          font-size: 1rem;
        }}

        .habit-meta {{
          margin-top: 0.25rem;
          font-size: 0.92rem;
        }}

        .habit-actions {{
          display: flex;
          gap: 0.55rem;
          flex-shrink: 0;
        }}

        .check-button.is-complete {{
          background: var(--success);
        }}

        .stats {{
          margin-top: 1rem;
        }}

        .stat-card {{
          flex: 1;
          border-radius: 1.2rem;
          background: rgba(255, 255, 255, 0.78);
          border: 1px solid var(--line);
          padding: 1rem;
        }}

        .stat-value {{
          margin-top: 0.35rem;
          font-size: 2rem;
          font-weight: 800;
        }}

        .sr-only {{
          position: absolute;
          width: 1px;
          height: 1px;
          padding: 0;
          margin: -1px;
          overflow: hidden;
          clip: rect(0, 0, 0, 0);
          border: 0;
        }}

        @media (max-width: 640px) {{
          .habit-form,
          .stats {{
            grid-template-columns: 1fr;
          }}

          .habit-item,
          .habit-actions {{
            flex-direction: column;
            align-items: stretch;
          }}

          .habit-actions {{
            width: 100%;
          }}

          .habit-actions button {{
            width: 100%;
          }}
        }}
        """
    )


APP_JS = """\
const STORAGE_KEY = "mobile-habit-tracker-state-v1";
const habitForm = document.getElementById("habit-form");
const habitNameInput = document.getElementById("habit-name");
const habitList = document.getElementById("habit-list");
const completedCount = document.getElementById("completed-count");
const bestStreak = document.getElementById("best-streak");
const todayLabel = document.getElementById("today-label");
const template = document.getElementById("habit-item-template");
const installButton = document.getElementById("install-button");

let deferredInstallPrompt = null;

function todayKey() {
  return new Date().toISOString().slice(0, 10);
}

function formatToday() {
  return new Intl.DateTimeFormat(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
  }).format(new Date());
}

function readState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const parsed = raw ? JSON.parse(raw) : null;
    if (!parsed || !Array.isArray(parsed.habits)) {
      return { habits: [] };
    }
    return parsed;
  } catch (error) {
    return { habits: [] };
  }
}

function writeState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function streakFromDates(entries) {
  const unique = [...new Set(entries)].sort().reverse();
  let streak = 0;
  const cursor = new Date();
  cursor.setHours(0, 0, 0, 0);

  for (const entry of unique) {
    const key = cursor.toISOString().slice(0, 10);
    if (entry !== key) {
      break;
    }
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }

  return streak;
}

function bestStreakFromDates(entries) {
  const unique = [...new Set(entries)].sort();
  if (!unique.length) {
    return 0;
  }

  let best = 1;
  let current = 1;

  for (let index = 1; index < unique.length; index += 1) {
    const previous = new Date(unique[index - 1]);
    const currentDate = new Date(unique[index]);
    const diff = Math.round((currentDate - previous) / 86400000);
    if (diff === 1) {
      current += 1;
      best = Math.max(best, current);
    } else {
      current = 1;
    }
  }

  return best;
}

function render() {
  const state = readState();
  const today = todayKey();
  todayLabel.textContent = formatToday();
  habitList.innerHTML = "";

  if (!state.habits.length) {
    const empty = document.createElement("li");
    empty.className = "habit-item";
    empty.innerHTML = `
      <div class="habit-copy">
        <p class="habit-name">아직 습관이 없습니다</p>
        <p class="habit-meta">작은 일상 습관 하나를 추가하고 홈 화면에서 바로 체크하세요.</p>
      </div>
    `;
    habitList.appendChild(empty);
  }

  let completedToday = 0;
  let best = 0;

  state.habits.forEach((habit) => {
    const fragment = template.content.cloneNode(true);
    const item = fragment.querySelector(".habit-item");
    const name = fragment.querySelector(".habit-name");
    const meta = fragment.querySelector(".habit-meta");
    const checkButton = fragment.querySelector(".check-button");
    const deleteButton = fragment.querySelector(".delete-button");
    const checkedToday = habit.completed_dates.includes(today);
    const streak = streakFromDates(habit.completed_dates);
    const personalBest = bestStreakFromDates(habit.completed_dates);

    best = Math.max(best, personalBest);
    if (checkedToday) {
      completedToday += 1;
      checkButton.classList.add("is-complete");
      checkButton.textContent = "오늘 완료";
    }

    name.textContent = habit.name;
    meta.textContent = `현재 ${streak}일 연속 · 최고 ${personalBest}일`;

    checkButton.addEventListener("click", () => {
      const nextState = readState();
      const target = nextState.habits.find((entry) => entry.id === habit.id);
      if (!target) {
        return;
      }

      if (target.completed_dates.includes(today)) {
        target.completed_dates = target.completed_dates.filter((entry) => entry !== today);
      } else {
        target.completed_dates.push(today);
      }

      writeState(nextState);
      render();
    });

    deleteButton.addEventListener("click", () => {
      const nextState = readState();
      nextState.habits = nextState.habits.filter((entry) => entry.id !== habit.id);
      writeState(nextState);
      render();
    });

    item.dataset.habitId = habit.id;
    habitList.appendChild(fragment);
  });

  completedCount.textContent = String(completedToday);
  bestStreak.textContent = String(best);
}

habitForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const value = habitNameInput.value.trim();
  if (!value) {
    return;
  }

  const state = readState();
  state.habits.unshift({
    id: crypto.randomUUID(),
    name: value,
    completed_dates: [],
  });
  writeState(state);
  habitNameInput.value = "";
  render();
});

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

render();
"""


SERVICE_WORKER = """\
const CACHE_NAME = "mobile-habit-tracker-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./styles.css",
  "./app.js",
  "./manifest.webmanifest",
  "./icon.svg",
  "./apple-touch-icon.svg",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))),
    ),
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => {
      if (cached) {
        return cached;
      }

      return fetch(event.request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match("./index.html"));
    }),
  );
});
"""


PREVIEW_SERVER = """\
from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import functools


HOST = "0.0.0.0"
PORT = 4173
WEB_DIR = Path(__file__).resolve().parent / "web"


def main() -> None:
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(WEB_DIR))
    server = ThreadingHTTPServer((HOST, PORT), handler)
    print(f"Preview running at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
"""


def build_icon(app_name: str, short_name: str, theme_color: str) -> str:
    return textwrap.dedent(
        f"""\
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
          <rect width="512" height="512" rx="124" fill="{theme_color}" />
          <rect x="96" y="88" width="320" height="336" rx="92" fill="rgba(255,255,255,0.14)" />
          <rect x="138" y="138" width="236" height="236" rx="68" fill="#ffffff" />
          <circle cx="196" cy="198" r="18" fill="{theme_color}" />
          <circle cx="256" cy="198" r="18" fill="{theme_color}" opacity="0.75" />
          <circle cx="316" cy="198" r="18" fill="{theme_color}" opacity="0.45" />
          <path d="M184 276l42 42 100-108" fill="none" stroke="{theme_color}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round" />
          <title>{app_name}</title>
        </svg>
        """
    )


def build_manifest(app_name: str, short_name: str, description: str, theme_color: str) -> str:
    manifest = {
        "name": app_name,
        "short_name": short_name,
        "description": description,
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#f4efe6",
        "theme_color": theme_color,
        "icons": [
            {"src": "./icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"},
            {"src": "./apple-touch-icon.svg", "sizes": "180x180", "type": "image/svg+xml"},
        ],
    }
    return json.dumps(manifest, indent=2) + "\n"


def build_readme(app_name: str, slug: str, description: str) -> str:
    return textwrap.dedent(
        f"""\
        # {app_name}

        이 앱은 하나의 아이디어 문장에서 생성된 모바일 우선 PWA 스캐폴드입니다.

        ## 무엇인가

        {description}

        ## 왜 이런 형태인가

        - 휴대폰 홈 화면에 설치 가능
        - 정적 배포로 동작
        - 기본적으로 로컬에 데이터 저장
        - 개발용 PC가 켜져 있을 필요 없음

        ## 파일

        - `web/index.html`
        - `web/styles.css`
        - `web/app.js`
        - `web/manifest.webmanifest`
        - `web/service-worker.js`
        - `preview.py`
        - `deploy_plan.md`

        ## 로컬 미리보기

        ```bash
        cd codex-notion-app-factory/examples/generated_apps/{slug}
        python preview.py
        ```

        그다음 `http://127.0.0.1:4173`를 엽니다.

        ## 휴대폰 설치

        1. 저장소를 GitHub에 커밋하고 push합니다.
        2. 저장소에서 GitHub Pages를 활성화하고 Pages 워크플로가 생성된 앱을 배포하도록 합니다.
        3. 휴대폰에서 배포된 `/{slug}/` URL을 엽니다.
        4. 브라우저의 홈 화면 추가 기능을 사용합니다.

        ## 참고

        이 스캐폴드는 로컬 우선 구조입니다. 나중에 기기 간 동기화가 필요해지면, 모바일 셸은 유지한 채 작은 인증 백엔드만 추가하면 됩니다.
        """
    )


def build_deploy_plan(app_name: str, slug: str) -> str:
    return textwrap.dedent(
        f"""\
        # 배포 계획

        ## 기본 대상

        `{app_name}`를 정적 PWA로 배포합니다.

        권장 순서:

        1. GitHub Pages
        2. Cloudflare Pages
        3. Vercel

        ## 배포 단계

        1. 저장소를 GitHub에 커밋하고 push합니다.
        2. 저장소에서 GitHub Pages를 활성화합니다.
        3. GitHub Actions 워크플로가 `examples/generated_apps`를 기준으로 `.pages-dist`를 생성하도록 합니다.
        4. 휴대폰에서 배포된 `/{slug}/` URL을 엽니다.
        5. 홈 화면에 추가합니다.

        ## 백엔드가 필요한 경우

        아래 조건이 생길 때만 백엔드를 추가합니다.

        - authenticated sync across devices
        - shared data between users
        - notifications or scheduled jobs
        - AI calls or secret-bearing APIs
        """
    )


def build_brief(app_name: str, idea: str) -> str:
    return textwrap.dedent(
        f"""\
        # 개요

        ## 앱 이름

        {app_name}

        ## 아이디어

        {idea}

        ## 전달 방식 결정

        데스크톱 런타임 없이 휴대폰 홈 화면에서 바로 실행할 수 있도록 우선 설치 가능한 PWA로 만듭니다.

        ## 저장 방식

        브라우저 로컬 우선 저장소.
        """
    )


def build_spec(app_name: str, idea: str) -> str:
    return textwrap.dedent(
        f"""\
        # Spec

        ## Product

        {app_name}

        ## Source Idea

        {idea}

        ## Delivery Target

        Installable PWA.

        ## Core User Stories

        - As the primary user, I can add a habit from my phone in a few seconds.
        - As the primary user, I can mark a habit complete for today with one tap.
        - As the primary user, I can see my streaks without opening my laptop.

        ## Functional Requirements

        - add and delete habits
        - persist habits locally on the device
        - track daily completion by date
        - show completed count for today
        - show best streak per habit summary
        - expose installability metadata through a manifest and service worker

        ## Non-Functional Requirements

        - mobile-first layout
        - static hosting compatible
        - local-first data model
        - fast load on mobile
        """
    )


def build_implementation_plan() -> str:
    return textwrap.dedent(
        """\
        # Implementation Plan

        1. Generate a static PWA shell with manifest and service worker.
        2. Implement a local-first habit tracking model in browser storage.
        3. Build a tap-friendly mobile UI for add, check-in, and delete flows.
        4. Add a local preview server for quick testing before deployment.
        5. Publish the `web/` directory to static hosting and install from the phone browser.
        """
    )


def build_tasks() -> str:
    return textwrap.dedent(
        """\
        # Tasks

        - [x] Create app brief
        - [x] Create product spec
        - [x] Create implementation plan
        - [x] Scaffold installable PWA shell
        - [x] Implement local habit tracking logic
        - [x] Add deployment notes
        - [ ] Add cross-device sync if needed later
        """
    )


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a mobile-first personal app PWA.")
    parser.add_argument("--idea", required=True, help="Short idea statement for the app.")
    parser.add_argument("--name", help="Optional explicit app name.")
    parser.add_argument("--slug", help="Optional directory slug.")
    parser.add_argument(
        "--output-root",
        default=str(DEFAULT_OUTPUT_ROOT),
        help="Directory that will contain the generated app folder.",
    )
    parser.add_argument("--theme-color", default="#177e89", help="Primary theme color for the scaffold.")
    args = parser.parse_args()

    app_name = infer_name(args.name, args.idea)
    slug = args.slug or slugify(app_name)
    short_name = app_name if len(app_name) <= 12 else app_name[:12]
    description = f"{app_name} is a phone-ready personal tracker generated from your idea: {args.idea.strip()}"
    output_dir = Path(args.output_root).expanduser().resolve() / slug

    if output_dir.exists() and any(output_dir.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty directory: {output_dir}")

    web_dir = output_dir / "web"
    output_dir.mkdir(parents=True, exist_ok=True)
    web_dir.mkdir(parents=True, exist_ok=True)

    write_file(output_dir / "README.md", build_readme(app_name, slug, description))
    write_file(output_dir / "brief.md", build_brief(app_name, args.idea))
    write_file(output_dir / "spec.md", build_spec(app_name, args.idea))
    write_file(output_dir / "implementation_plan.md", build_implementation_plan())
    write_file(output_dir / "tasks.md", build_tasks())
    write_file(output_dir / "deploy_plan.md", build_deploy_plan(app_name, slug))
    write_file(
        output_dir / "app_spec.json",
        json.dumps(
            {
                "app_name": app_name,
                "slug": slug,
                "delivery_target": "installable-pwa",
                "storage": "local-first",
                "idea": args.idea.strip(),
                "theme_color": args.theme_color,
            },
            indent=2,
        )
        + "\n",
    )
    write_file(output_dir / "preview.py", PREVIEW_SERVER)
    write_file(web_dir / "index.html", build_index_html(app_name, short_name, description, args.theme_color))
    write_file(web_dir / "styles.css", build_styles(args.theme_color))
    write_file(web_dir / "app.js", APP_JS)
    write_file(web_dir / "service-worker.js", SERVICE_WORKER)
    write_file(web_dir / "manifest.webmanifest", build_manifest(app_name, short_name, description, args.theme_color))
    icon = build_icon(app_name, short_name, args.theme_color)
    write_file(web_dir / "icon.svg", icon)
    write_file(web_dir / "apple-touch-icon.svg", icon)

    print(f"Generated mobile PWA scaffold at {output_dir}")


if __name__ == "__main__":
    main()
