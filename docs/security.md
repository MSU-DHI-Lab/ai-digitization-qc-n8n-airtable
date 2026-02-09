# Security Guidance

## Deployment Baselines
- Keep `ALLOW_NO_TOKEN=false` in all non-local environments.
- Set a strong `MODEL_API_TOKEN` and configure n8n to pass `x-api-token` on every `/predict` call.
- Keep the model API behind trusted network boundaries and terminate TLS at the front door/reverse proxy.

## Workflow Command Execution Safety
- `USE_SHELL_MOVES=false` is the secure default.
- Enable shell moves only when required and only in trusted environments.
- If enabled, keep ingest and destination paths restricted to controlled directories.

## Upload and Parsing Safety
- Accepted upload formats are JPEG, PNG, and TIFF.
- The service enforces size and pixel limits (`MAX_UPLOAD_MB`, `MAX_PIXELS`) and rejects invalid or mismatched file types.
- Keep limits aligned with host capacity to reduce denial-of-service risk.

## API Hardening Controls
- The API sets baseline response headers:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Referrer-Policy: no-referrer`
  - `Cache-Control: no-store`

## Secrets Handling
- Store all credentials and tokens in environment variables or orchestrator secret stores.
- Do not commit credentials, tokens, or private keys to the repository.
- If a secret is exposed, rotate it out-of-band immediately.

## Supply Chain Hygiene
- CI workflow actions are pinned to immutable commit SHAs.
- Review dependency updates regularly and prefer deterministic builds where possible.

## Verification Commands
- `make test`
- `docker compose config`

## Operational Notes
- Some local tooling checks may fail in offline environments (for example, lint installs that require internet).
- Treat this file as operational security guidance; detailed audit evidence is in `SECURITY_REPORT.md` and `SECURITY_VERIFICATION.md`.
