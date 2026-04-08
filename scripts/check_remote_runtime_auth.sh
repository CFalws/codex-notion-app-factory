#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-/tmp/codex-factory.env}"

set -a
source "$ENV_FILE"
set +a

printf 'health=%s\n' "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/health)"
printf 'apps_no_key=%s\n' "$(curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1/api/apps)"
printf 'apps_with_key=%s\n' "$(curl -s -o /dev/null -w '%{http_code}' -H "X-API-Key: $CODEX_FACTORY_API_KEY" http://127.0.0.1/api/apps)"
