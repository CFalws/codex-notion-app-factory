#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://127.0.0.1:8787}"
APP_ID="${APP_ID:-habit-tracker-pwa}"
SCRATCH_FILE="${SCRATCH_FILE:-workspaces/habit-tracker-pwa/runtime-api-verification/remote-scratch.md}"
API_KEY="${API_KEY:-${CODEX_FACTORY_API_KEY:-}}"

mkdir -p "$(dirname "$SCRATCH_FILE")"
printf '# Remote Verification\n\nmarker: unchanged\n' > "$SCRATCH_FILE"

post_request() {
  local payload="$1"
  local -a headers=(-H 'Content-Type: application/json')
  if [[ -n "$API_KEY" ]]; then
    headers+=(-H "X-API-Key: $API_KEY")
  fi
  curl -s -X POST "$BASE_URL/api/requests" \
    "${headers[@]}" \
    -d "$payload"
}

get_job() {
  local job_id="$1"
  local -a headers=()
  if [[ -n "$API_KEY" ]]; then
    headers+=(-H "X-API-Key: $API_KEY")
  fi
  curl -s "${headers[@]}" "$BASE_URL/api/jobs/$job_id"
}

extract_field() {
  local key="$1"
  sed -n "s/.*\"$key\":\"\\([^\"]*\\)\".*/\\1/p"
}

wait_for_job() {
  local job_id="$1"
  local job status
  for _ in $(seq 1 120); do
    job="$(get_job "$job_id")"
    status="$(printf '%s' "$job" | extract_field status)"
    if [[ "$status" == "completed" || "$status" == "failed" ]]; then
      printf '%s' "$job"
      return 0
    fi
    sleep 2
  done
  echo "Timed out waiting for job $job_id" >&2
  exit 1
}

ping_payload='{"app_id":"'"$APP_ID"'","title":"Remote runtime ping","request_text":"Reply with exactly one line: REMOTE_RUNTIME_OK. Do not inspect files and do not make any changes.","source":"gce-remote-verification","execute_now":true}'
ping_response="$(post_request "$ping_payload")"
ping_job_id="$(printf '%s' "$ping_response" | extract_field job_id)"
ping_job="$(wait_for_job "$ping_job_id")"
printf '%s' "$ping_job" | grep -q '"result_summary":"REMOTE_RUNTIME_OK"'

edit_payload='{"app_id":"'"$APP_ID"'","title":"Remote runtime file edit","request_text":"Update only '"$SCRATCH_FILE"'. Replace marker: unchanged with marker: remote_runtime_verified. Do not modify any other file, and summarize the exact edit.","source":"gce-remote-verification","execute_now":true}'
edit_response="$(post_request "$edit_payload")"
edit_job_id="$(printf '%s' "$edit_response" | extract_field job_id)"
edit_job="$(wait_for_job "$edit_job_id")"
printf '%s' "$edit_job" | grep -q '"status":"completed"'
grep -q 'marker: remote_runtime_verified' "$SCRATCH_FILE"

app_headers=()
if [[ -n "$API_KEY" ]]; then
  app_headers+=(-H "X-API-Key: $API_KEY")
fi
app_response="$(curl -s "${app_headers[@]}" "$BASE_URL/api/apps/$APP_ID")"
session_id="$(printf '%s' "$app_response" | extract_field session_id)"

printf 'ping_job=%s\n' "$ping_job_id"
printf 'ping_result=%s\n' "REMOTE_RUNTIME_OK"
printf 'edit_job=%s\n' "$edit_job_id"
printf 'edit_status=%s\n' "completed"
printf 'session_id=%s\n' "$session_id"
printf 'scratch_file=%s\n' "$SCRATCH_FILE"
