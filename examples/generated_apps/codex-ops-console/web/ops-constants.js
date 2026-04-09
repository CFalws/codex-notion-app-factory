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
export const UX_REVIEW_FIELDS = [
  ["primary_journey", "핵심 사용자 흐름"],
  ["pain_interpretation", "해석한 불편"],
  ["friction_points", "마찰 지점"],
  ["simplification", "단순화 방향"],
  ["mobile_risk", "모바일 리스크"],
  ["verification_steps", "UX 검증 방법"],
];
export const UX_PAIN_POINT_OPTIONS = [
  "길 찾기 어려움",
  "상태가 안 보임",
  "버튼 위치 불편",
  "정보가 너무 많음",
  "입력 흐름이 답답함",
  "모바일에서 누르기 불편",
];
