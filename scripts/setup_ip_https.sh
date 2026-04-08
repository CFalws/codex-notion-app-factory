#!/usr/bin/env bash
set -euo pipefail

IP_ADDRESS="${1:-34.40.112.33}"
LE_ROOT="/var/www/letsencrypt"
CERTBOT_ROOT="/opt/certbot"
NGINX_SITE="/etc/nginx/sites-available/codex-factory"

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root."
  exit 1
fi

mkdir -p "$LE_ROOT/.well-known/acme-challenge"

cat > "$NGINX_SITE" <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name _;

    client_max_body_size 2m;

    location ^~ /.well-known/acme-challenge/ {
        root $LE_ROOT;
        default_type text/plain;
        try_files \$uri =404;
    }

    location = /ops {
        return 302 /ops/;
    }

    location /ops/ {
        alias /opt/codex-app-factory/examples/generated_apps/codex-ops-console/web/;
        try_files \$uri \$uri/ /ops/index.html;
    }

    location / {
        proxy_pass http://127.0.0.1:8787;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

nginx -t
systemctl reload nginx

python3 -m venv "$CERTBOT_ROOT"
"$CERTBOT_ROOT/bin/pip" install --upgrade pip
"$CERTBOT_ROOT/bin/pip" install "certbot>=5.4"
"$CERTBOT_ROOT/bin/certbot" --version

"$CERTBOT_ROOT/bin/certbot" certonly \
  --non-interactive \
  --agree-tos \
  --register-unsafely-without-email \
  --preferred-profile shortlived \
  --webroot \
  --webroot-path "$LE_ROOT" \
  --ip-address "$IP_ADDRESS"

cat > "$NGINX_SITE" <<EOF
server {
    listen 80;
    listen [::]:80;
    server_name _;

    client_max_body_size 2m;

    location ^~ /.well-known/acme-challenge/ {
        root $LE_ROOT;
        default_type text/plain;
        try_files \$uri =404;
    }

    location / {
        return 301 https://$IP_ADDRESS\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name _;

    client_max_body_size 2m;

    ssl_certificate /etc/letsencrypt/live/$IP_ADDRESS/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$IP_ADDRESS/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;

    location = /ops {
        return 302 /ops/;
    }

    location /ops/ {
        alias /opt/codex-app-factory/examples/generated_apps/codex-ops-console/web/;
        try_files \$uri \$uri/ /ops/index.html;
    }

    location / {
        proxy_pass http://127.0.0.1:8787;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

nginx -t

mkdir -p /etc/letsencrypt/renewal-hooks/deploy
cat > /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
systemctl reload nginx
EOF
chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh

cat > /etc/systemd/system/certbot-ip-renew.service <<EOF
[Unit]
Description=Renew Let's Encrypt IP certificate
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=$CERTBOT_ROOT/bin/certbot renew -q
EOF

cat > /etc/systemd/system/certbot-ip-renew.timer <<'EOF'
[Unit]
Description=Twice-daily Certbot renewal for short-lived IP certificate

[Timer]
OnCalendar=*-*-* 00,12:00:00
RandomizedDelaySec=15m
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload
systemctl enable --now certbot-ip-renew.timer
systemctl reload nginx
systemctl status certbot-ip-renew.timer --no-pager | sed -n '1,12p'
