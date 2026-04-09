#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

printf '[verify-static] python compileall\n'
python3 -m compileall src scripts >/dev/null

printf '[verify-static] node syntax checks\n'
while IFS= read -r file; do
  node --check "$file" >/dev/null
  printf '  ok %s\n' "$file"
done < <(find examples/generated_apps/codex-ops-console/web -name '*.js' -type f | sort)

printf '[verify-static] ok\n'
