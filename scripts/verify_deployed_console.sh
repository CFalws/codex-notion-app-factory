#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-https://codex-factory-vm.tail1b6dd1.ts.net}"
APP_ID="${APP_ID:-habit-tracker-pwa}"
API_KEY="${API_KEY:-${CODEX_FACTORY_API_KEY:-}}"
POLL_INTERVAL="${POLL_INTERVAL:-2}"
MAX_POLLS="${MAX_POLLS:-120}"
TMP_IMAGE="$(mktemp -t codex-ux-shot.XXXXXX.png)"

trap 'rm -f "$TMP_IMAGE"' EXIT

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

api_multipart() {
  local method="$1"
  local path="$2"
  local file_path="$3"
  local -a args=(-sS -X "$method" "$BASE_URL$path")
  if [[ -n "$API_KEY" ]]; then
    args+=(-H "X-API-Key: $API_KEY")
  fi
  args+=(-F "files=@${file_path};type=image/png")
  curl "${args[@]}"
}

health="$(curl -sS "$BASE_URL/health")"
echo "$health" | grep -q '"ok":true'

apps="$(api GET /api/apps)"
echo "$apps" | grep -q '"app_id"'

timestamp="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
python3 - <<PY
import base64
from pathlib import Path
Path("$TMP_IMAGE").write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO2Z3ioAAAAASUVORK5CYII="))
PY
conversation="$(api POST /api/conversations "{\"app_id\":\"$APP_ID\",\"source\":\"verify-deployed-console\"}")"
conversation_id="$(printf '%s' "$conversation" | python3 -c 'import json,sys; print(json.load(sys.stdin)["conversation_id"])')"
attachments_response="$(api_multipart POST "/api/conversations/$conversation_id/attachments" "$TMP_IMAGE")"
attachments_json="$(printf '%s' "$attachments_response" | python3 -c 'import json,sys; payload=json.load(sys.stdin); assert payload["attachments"]; print(json.dumps(payload["attachments"]))')"

message_payload="$(python3 - <<PY
import json
print(json.dumps({
  "message_text": f"Reply with exactly one line: DEPLOYED_CONVERSATION_OK ({'$timestamp'}). Use the attached screenshot only as visual context. Do not modify files.",
  "source": "verify-deployed-console",
  "ux_context": {
    "affected_surface": "deployed console smoke flow",
    "pain_points": ["상태가 안 보임"],
    "note": "Smoke test for screenshot-backed UX review.",
    "desired_feel": "more obvious"
  },
  "attachments": json.loads('''$attachments_json''')
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
required={"conversation.created","attachment.saved","message.accepted","job.queued","job.running","job.completed"}
missing=sorted(required-events)
if missing:
    raise SystemExit(f"missing conversation events: {missing}")
forbidden={"codex.exec.retrying","runtime.exception"}
unexpected=sorted(forbidden & events)
if unexpected:
    raise SystemExit(f"unexpected degraded events: {unexpected}")
messages=payload.get("messages", [])
roles=[message["role"] for message in messages]
if roles[:2] != ["user", "assistant"]:
    raise SystemExit(f"unexpected message roles: {roles}")
request_messages=[message for message in messages if message.get("role")=="user"]
if not request_messages or not request_messages[0].get("metadata", {}).get("attachments"):
    raise SystemExit("request message is missing persisted screenshot attachments")'

echo "conversation_id=$conversation_id"
echo "job_id=$job_id"
echo "status=completed"
echo "summary=$summary"
echo "verify_deployed_console=ok"
