# 배포 계획

## 기본 대상

`Habit Tracker PWA`를 정적 PWA로 배포합니다.

권장 순서:

1. GitHub Pages
2. Cloudflare Pages
3. Vercel

## 배포 단계

1. 저장소를 GitHub에 커밋하고 push합니다.
2. 저장소에서 GitHub Pages를 활성화합니다.
3. GitHub Actions 워크플로가 `examples/generated_apps`를 기준으로 `.pages-dist`를 생성하도록 합니다.
4. 휴대폰에서 배포된 `/habit-tracker-pwa/` URL을 엽니다.
5. 홈 화면에 추가합니다.

## When To Add A Backend

Add a backend only if one of these becomes necessary:

- authenticated sync across devices
- shared data between users
- notifications or scheduled jobs
- AI calls or secret-bearing APIs
