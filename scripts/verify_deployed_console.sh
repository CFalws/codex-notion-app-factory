#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-https://codex-factory-vm.tail1b6dd1.ts.net}"
APP_ID="${APP_ID:-habit-tracker-pwa}"
API_KEY="${API_KEY:-${CODEX_FACTORY_API_KEY:-}}"
POLL_INTERVAL="${POLL_INTERVAL:-2}"
MAX_POLLS="${MAX_POLLS:-120}"

api() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  local -a args=(-sS -X "$method" "$BASE_URL$path")
  if [[ -n "$API_KEY" ]]; then
    args+=(-H "X-API-Key: $API_KEY")
  fi
  if [[ -n "$body" ]]; then
    args+=(-H 'Content-Type: application/json' -d "$body")
  fi
  curl "${args[@]}"
}

health="$(curl -sS "$BASE_URL/health")"
echo "$health" | grep -q '"ok":true'

apps="$(api GET /api/apps)"
echo "$apps" | grep -q '"app_id"'

timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
conversation="$(api POST /api/conversations "{\"app_id\":\"$APP_ID\",\"source\":\"verify-deployed-console\"}")"
conversation_id="$(printf '%s' "$conversation" | python3 -c 'import json,sys; print(json.load(sys.stdin)["conversation_id"])')"

message_payload="$(python3 - <<PY
import json
print(json.dumps({
  "message_text": f"Reply with exactly one line: DEPLOYED_CONVERSATION_OK ({'$timestamp'}). Do not modify files.",
  "source": "verify-deployed-console"
}))
PY
)"

message_response="$(api POST "/api/conversations/$conversation_id/messages" "$message_payload")"
job_id="$(printf '%s' "$message_response" | python3 -c 'import json,sys; print(json.load(sys.stdin)["job"]["job_id"])')"

job=''
for _ in $(seq 1 "$MAX_POLLS"); do
  job="$(api GET "/api/jobs/$job_id")"
  status="$(printf '%s' "$job" | python3 -c 'import json,sys; print(json.load(sys.stdin)["status"])')"
  if [[ "$status" == "completed" || "$status" == "failed" ]]; then
    break
  fi
  sleep "$POLL_INTERVAL"
done

final_status="$(printf '%s' "$job" | python3 -c 'import json,sys; print(json.load(sys.stdin)["status"])')"
[[ "$final_status" == "completed" ]]

summary="$(printf '%s' "$job" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("result_summary", ""))')"
echo "$summary" | grep -q 'DEPLOYED_CONVERSATION_OK'

conversation_after="$(api GET "/api/conversations/$conversation_id")"
printf '%s' "$conversation_after" | python3 -c 'import json,sys
payload=json.load(sys.stdin)
events={event["type"] for event in payload.get("events", [])}
required={"conversation.created","message.accepted","job.queued","job.running","job.completed"}
missing=sorted(required-events)
if missing:
    raise SystemExit(f"missing conversation events: {missing}")
messages=payload.get("messages", [])
roles=[message["role"] for message in messages]
if roles[:2] != ["user", "assistant"]:
    raise SystemExit(f"unexpected message roles: {roles}")'

echo "conversation_id=$conversation_id"
echo "job_id=$job_id"
echo "status=completed"
echo "summary=$summary"
echo "verify_deployed_console=ok"
