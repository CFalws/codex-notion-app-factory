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

- [bootstrap_gce_runtime.sh](/Users/emil/emil/python/codex-notion-app-factory/scripts/bootstrap_gce_runtime.sh)
- [codex-factory.service](/Users/emil/emil/python/codex-notion-app-factory/deploy/gce/codex-factory.service)
- [nginx-codex-factory.conf](/Users/emil/emil/python/codex-notion-app-factory/deploy/gce/nginx-codex-factory.conf)

## Bootstrap Flow

1. Create the VM.
2. Copy the repository onto the VM.
3. Run the bootstrap script as root.
4. Set `CODEX_FACTORY_API_KEY` in `/etc/codex-factory.env`.
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

## Security Notes

- The sample nginx config exposes the runtime publicly on port 80.
- Set `CODEX_FACTORY_API_KEY` before opening the VM to the internet. The runtime now rejects `/api/*` requests that do not send the matching `X-API-Key` header.
- For real use, still add at least one of:
  - IP allowlisting
  - a VPN or private network path
  - HTTPS with a real hostname
  - another front-door auth layer if multiple humans will operate it

## Verification

Once the service is up and Codex is logged in:

```bash
cd /opt/codex-app-factory
API_KEY=your-runtime-key ./scripts/verify_deployed_runtime.sh
```

That verification hits the already running service, sends real authenticated HTTP requests, and confirms both a read-only Codex run and a file-edit Codex run.
