#!/usr/bin/env bash
set -euo pipefail

GCE_VM_NAME="${GCE_VM_NAME:-codex-factory-vm}"
GCE_ZONE="${GCE_ZONE:-europe-west3-b}"
GCE_PROJECT="${GCE_PROJECT:-project-dc0c78c5-4b4a-4ef1-9fe}"
GCE_REPO_PATH="${GCE_REPO_PATH:-/opt/codex-app-factory}"
GCE_SERVICE_NAME="${GCE_SERVICE_NAME:-codex-factory}"
GCE_APP_USER="${GCE_APP_USER:-codex}"

REMOTE_CMD="sudo -u ${GCE_APP_USER} git config --global --add safe.directory ${GCE_REPO_PATH} && sudo -u ${GCE_APP_USER} git -C ${GCE_REPO_PATH} pull --ff-only origin main && sudo -u ${GCE_APP_USER} ${GCE_REPO_PATH}/.venv/bin/pip install -e ${GCE_REPO_PATH} >/tmp/codex-factory-pip.log && sudo systemctl restart ${GCE_SERVICE_NAME} && sudo systemctl is-active ${GCE_SERVICE_NAME} && sudo -u ${GCE_APP_USER} git -C ${GCE_REPO_PATH} rev-parse HEAD"

gcloud compute ssh "${GCE_VM_NAME}"   --zone="${GCE_ZONE}"   --project="${GCE_PROJECT}"   --command="${REMOTE_CMD}"
