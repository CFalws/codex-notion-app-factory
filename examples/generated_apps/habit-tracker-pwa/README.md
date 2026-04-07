# Habit Tracker PWA

이 앱은 하나의 아이디어 문장에서 생성된 모바일 우선 PWA 스캐폴드입니다.

## 무엇인가

Habit Tracker PWA는 당신의 아이디어를 바탕으로 생성된 모바일 중심 개인 트래커입니다. 노트북 런타임 없이도 휴대폰에서 습관을 추가하고, 빠르게 체크하고, 연속 기록을 확인할 수 있도록 설계되었습니다.

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
cd codex-notion-app-factory/examples/generated_apps/habit-tracker-pwa
python preview.py
```

그다음 `http://127.0.0.1:4173`를 엽니다.

## 휴대폰 설치

1. 저장소를 GitHub에 커밋하고 push합니다.
2. 저장소에서 GitHub Pages를 활성화하고 `Deploy Generated Apps To GitHub Pages` 워크플로를 실행합니다.
3. 휴대폰에서 생성된 Pages URL의 `/habit-tracker-pwa/` 경로를 엽니다.
4. 브라우저의 홈 화면 추가 기능을 사용합니다.

## 참고

이 스캐폴드는 로컬 우선 구조입니다. 나중에 기기 간 동기화가 필요해지면, 모바일 셸은 유지한 채 작은 인증 백엔드만 추가하면 됩니다.

## GitHub Pages

저장소에는 `.github/workflows/deploy-generated-apps-pages.yml` 워크플로가 포함되어 있으며, 생성된 앱들을 모아 Pages 사이트를 빌드합니다.
