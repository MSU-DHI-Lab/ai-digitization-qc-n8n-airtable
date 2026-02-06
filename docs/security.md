# Security Guidance

- **Authentication**: Keep `ALLOW_NO_TOKEN=false` in all non-local environments. Provide a strong `MODEL_API_TOKEN` and configure clients (n8n) to pass it via `x-api-token`.
- **Upload Limits**: Set `MAX_UPLOAD_MB` and `MAX_PIXELS` to your environment’s safe limits; defaults guard against large scans but should match available resources. Oversized images now return 413.
- **Accepted Formats**: Only JPEG, PNG, and TIFF are allowed. Server-side validation rejects MIME/format mismatches.
- **Secrets Handling**: Store tokens and Airtable credentials in environment variables or orchestrator secrets, not in files or images. Rotate if exposed.
- **Deployment**: Run behind trusted network/front door; do not expose `/predict` publicly without authentication and transport security (TLS termination).
- **Logging**: Errors are sanitized for clients but logged server-side. Forward logs to centralized monitoring for alerting on repeated failures.
- **n8n Workflow**: Ensure `$env.MODEL_API_TOKEN` is set in n8n environment. Review file-watching paths to limit scope to intended ingest folders.
