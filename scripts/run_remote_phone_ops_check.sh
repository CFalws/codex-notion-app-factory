#!/usr/bin/env bash
set -euo pipefail

cd /opt/codex-app-factory

set -a
source /etc/codex-factory.env
set +a

export BASE_URL="${BASE_URL:-http://127.0.0.1}"
export API_KEY="${API_KEY:-$CODEX_FACTORY_API_KEY}"
export APP_ID="${APP_ID:-habit-tracker-pwa}"
export SCRATCH_FILE="${SCRATCH_FILE:-workspaces/habit-tracker-pwa/runtime-api-verification/phone-ops-check.md}"

bash /tmp/verify_deployed_runtime.sh
