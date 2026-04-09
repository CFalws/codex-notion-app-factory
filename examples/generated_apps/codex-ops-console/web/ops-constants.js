export const STORAGE_KEY = "codex-ops-console";
export const FIXED_RUNTIME_URL = "https://codex-factory-vm.tail1b6dd1.ts.net";
export const DRAFTS_KEY = `${STORAGE_KEY}:drafts`;
export const DECISION_FIELDS = [
  ["goal", "문제"],
  ["system_area", "영향 범위"],
  ["decision", "선택"],
  ["why", "왜 이 방식인가"],
  ["tradeoff", "트레이드오프"],
  ["issue_encountered", "실제 문제"],
  ["verification", "검증"],
  ["follow_up", "다음 단계"],
];

export const QUICK_PROMPTS = [
  {
    id: "ship-fix",
    label: "버그 수정",
    hint: "문제, 기대 동작, 검증 경로를 한 번에 채웁니다.",
    template:
      "문제:\n\n기대 결과:\n\n변경 범위:\n\n폰에서 확인 방법:\n",
  },
  {
    id: "ux-polish",
    label: "UX 다듬기",
    hint: "사용성 개선 지시를 빠르게 시작합니다.",
    template:
      "현재 UX의 마찰:\n\n원하는 경험:\n\n반드시 유지할 제약:\n\n완료 후 확인 시나리오:\n",
  },
  {
    id: "review-latest",
    label: "최근 변경 점검",
    hint: "가장 최근 작업의 리스크와 후속 조치를 요청합니다.",
    template:
      "가장 최근 변경을 기준으로:\n- 위험 요소\n- 누락된 검증\n- 바로 이어서 할 일\n을 정리해줘.\n",
  },
  {
    id: "apply-check",
    label: "배포 전 확인",
    hint: "적용 전 검증과 체크리스트를 구조화합니다.",
    template:
      "이 제안을 적용하기 전에 확인해야 할 항목을 정리하고,\n가능한 검증은 먼저 실행해줘.\n",
  },
];
