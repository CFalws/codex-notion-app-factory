# GCE Runtime Deploy

## Goal

Deploy the stateful Codex CLI runtime to a low-cost Google Compute Engine VM.

This runtime is a better fit for a VM than Cloud Run because:

- Codex CLI login state lives in the runtime user's home directory
- session continuity benefits from a stable filesystem
- job execution can outlive the HTTP request that created it

## Recommended VM

- machine type: `e2-micro`
- region: `us-central1`, `us-west1`, or `us-east1`
- image: Ubuntu LTS
- disk: standard persistent disk, 20 to 30 GB

This is intended to stay within free-tier or free-credit testing limits where possible.

## Files

- [bootstrap_gce_runtime.sh](/Users/emil/emil/python/codex-app-factory/scripts/bootstrap_gce_runtime.sh)
- [codex-factory.service](/Users/emil/emil/python/codex-app-factory/deploy/gce/codex-factory.service)
- [nginx-codex-factory.conf](/Users/emil/emil/python/codex-app-factory/deploy/gce/nginx-codex-factory.conf)

## Bootstrap Flow

1. Create the VM.
2. Copy the repository onto the VM.
3. Run the bootstrap script as root.
4. Configure runtime auth in `/etc/codex-factory.env`.
5. Log in to Codex once as the `codex` user.
6. Start the `codex-factory` systemd service.
7. Verify `http://127.0.0.1:8787/health` from the VM.

## Minimal Manual Commands

From the VM:

```bash
sudo bash /opt/codex-app-factory/scripts/bootstrap_gce_runtime.sh /opt/codex-app-factory
sudoedit /etc/codex-factory.env
sudo -u codex -H bash
cd /opt/codex-app-factory
codex --login
exit
sudo systemctl start codex-factory
curl http://127.0.0.1:8787/health
```

Example auth configuration for a Tailscale-only front door:

```bash
CODEX_FACTORY_AUTH_PROVIDERS=["loopback","tailscale"]
CODEX_FACTORY_ALLOWED_USER_EMAILS=["akdlzmf1123@gmail.com"]
```

## Security Notes

- The sample nginx config is only a bootstrap path, not the preferred long-term front door.
- For private personal use, prefer Tailscale on the VM and operator devices, plus `tailscale serve` pointing at `http://127.0.0.1:8787`.
- Configure the runtime with `CODEX_FACTORY_AUTH_PROVIDERS=["loopback","tailscale"]` so server-local smoke tests continue to work while operator traffic is authenticated through the tailnet.
- Set `CODEX_FACTORY_ALLOWED_USER_EMAILS` to your Tailscale login email.
- Remove the VM `http-server` tag or otherwise close public 80/443 ingress so tailnet headers cannot be spoofed through a public reverse proxy.

## Verification

Once the service is up and Codex is logged in:

```bash
cd /opt/codex-app-factory
./scripts/verify_gce_runtime.sh
```

That verification hits the already running service through loopback on the VM, sends real HTTP requests, and confirms both a read-only Codex run and a file-edit Codex run.
