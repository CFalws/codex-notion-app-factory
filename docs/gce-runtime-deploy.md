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
7. Verify `http://<vm-ip>/health`.

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

Example auth configuration for an IAP front door:

```bash
CODEX_FACTORY_AUTH_PROVIDERS=["loopback","iap"]
CODEX_FACTORY_IAP_AUDIENCE=/projects/PROJECT_NUMBER/global/backendServices/BACKEND_SERVICE_ID
CODEX_FACTORY_ALLOWED_USER_EMAILS=["you@example.com"]
```

## Security Notes

- The sample nginx config is only a bootstrap path, not the preferred long-term front door.
- For production on GCP, prefer an HTTPS load balancer plus Identity-Aware Proxy in front of the VM.
- Configure the runtime with `CODEX_FACTORY_AUTH_PROVIDERS=["loopback","iap"]` so server-local smoke tests continue to work while operator traffic is authenticated through IAP.
- Set `CODEX_FACTORY_IAP_AUDIENCE` and `CODEX_FACTORY_ALLOWED_USER_EMAILS` before exposing the runtime through the load balancer.
- Keep `CODEX_FACTORY_API_KEY` only as a compatibility path while migrating older tooling.

## Verification

Once the service is up and Codex is logged in:

```bash
cd /opt/codex-app-factory
API_KEY=your-runtime-key ./scripts/verify_deployed_runtime.sh
```

That verification hits the already running service, sends real authenticated HTTP requests, and confirms both a read-only Codex run and a file-edit Codex run.
