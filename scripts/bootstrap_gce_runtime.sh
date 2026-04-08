#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run this script as root on the target VM."
  exit 1
fi

REPO_SRC_DEFAULT="/tmp/codex-app-factory"
REPO_SRC="${1:-$REPO_SRC_DEFAULT}"
APP_ROOT="/opt/codex-app-factory"
SERVICE_FILE_SRC="$APP_ROOT/deploy/gce/codex-factory.service"
NGINX_CONF_SRC="$APP_ROOT/deploy/gce/nginx-codex-factory.conf"
ENV_FILE="/etc/codex-factory.env"

apt-get update
apt-get install -y git nginx python3 python3-venv python3-pip

if ! id -u codex >/dev/null 2>&1; then
  useradd --create-home --shell /bin/bash codex
fi

rm -rf "$APP_ROOT"
mkdir -p /opt
cp -R "$REPO_SRC" "$APP_ROOT"
chown -R codex:codex "$APP_ROOT"

sudo -u codex python3 -m venv "$APP_ROOT/.venv"
sudo -u codex "$APP_ROOT/.venv/bin/pip" install -e "$APP_ROOT"

cat > "$ENV_FILE" <<'EOF'
CODEX_COMMAND=codex
CODEX_FACTORY_HOST=127.0.0.1
CODEX_FACTORY_PORT=8787
CODEX_FACTORY_AUTO_EXECUTE=true
# Set this before exposing the runtime outside the VM.
# CODEX_FACTORY_API_KEY=replace-with-a-long-random-string
EOF

install -m 0644 "$SERVICE_FILE_SRC" /etc/systemd/system/codex-factory.service
install -m 0644 "$NGINX_CONF_SRC" /etc/nginx/sites-available/codex-factory
ln -sf /etc/nginx/sites-available/codex-factory /etc/nginx/sites-enabled/codex-factory
rm -f /etc/nginx/sites-enabled/default

nginx -t
systemctl daemon-reload
systemctl enable codex-factory
systemctl restart nginx

cat <<'EOF'

Bootstrap complete.

Next required manual step:
1. sudo -u codex -H bash
2. cd /opt/codex-app-factory
3. codex --login
4. exit
5. sudo systemctl start codex-factory
6. sudo systemctl status codex-factory

EOF
