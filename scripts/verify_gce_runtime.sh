#!/usr/bin/env bash
set -euo pipefail

GCE_VM_NAME="${GCE_VM_NAME:-codex-factory-vm}"
GCE_ZONE="${GCE_ZONE:-europe-west3-b}"
GCE_PROJECT="${GCE_PROJECT:-project-dc0c78c5-4b4a-4ef1-9fe}"
GCE_REPO_PATH="${GCE_REPO_PATH:-/opt/codex-app-factory}"
GCE_ENV_FILE="${GCE_ENV_FILE:-/etc/codex-factory.env}"
GCE_APP_USER="${GCE_APP_USER:-codex}"
APP_ID="${APP_ID:-habit-tracker-pwa}"

REMOTE_CMD="cd ${GCE_REPO_PATH} && sudo /bin/bash -lc 'source ${GCE_ENV_FILE}; export BASE_URL=http://127.0.0.1:8787; export APP_ID=${APP_ID}; sudo -u ${GCE_APP_USER} env CODEX_FACTORY_API_KEY="\${CODEX_FACTORY_API_KEY}" BASE_URL="\${BASE_URL}" APP_ID="\${APP_ID}" /usr/bin/python3 ./scripts/remote_runtime_smoke_test.py /dev/null'"

gcloud compute ssh "${GCE_VM_NAME}" --zone="${GCE_ZONE}" --project="${GCE_PROJECT}" --command="${REMOTE_CMD}"
