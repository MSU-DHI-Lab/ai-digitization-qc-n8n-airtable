# Baseline
- Git status at start: dirty (pre-existing changes to README.md, model-service/app.py, model-service/tests/test_app.py; new files pending add: CHANGELOG.md, QUALITY_AUDIT.md).
- README.* unchanged during this audit (protected).

# System Map
- **model-service (FastAPI)**: `/predict` file-upload endpoint with shared-secret header `x-api-token`; `/health` unauthenticated. Processes images in-memory; applies size/pixel limits; returns structured QC results.
- **n8n workflow** (`n8n/workflow-digitization-qc.json`): monitors incoming folder, posts binaries to model-service with `$env.MODEL_API_TOKEN`, retries, writes to Airtable.
- **Airtable base/docs**: schema/interface guidance in `docs/` and repo root files; tokens expected via environment.
- **Trust boundaries**: incoming file share -> n8n -> model-service; API token boundary between n8n/clients and model-service; outbound to Airtable via API credentials (not in repo).
- **Critical assets**: uploaded images, QC results (defect flags/metadata), API tokens, Airtable credentials.

# Findings (post-remediation)
- [SEC-001][High][A05/A06] `/predict` accepted client-declared MIME without verifying actual format, allowing spoofed uploads. Fixed by server-side format/MIME verification and mismatch rejection. (model-service/app.py)
- [SEC-002][High][A06/A10] Oversized or pixel-bomb images returned generic 400 and could bypass configured pixel limit. Fixed with explicit decompression bomb handling to 413 and enforced pixel budget test. (model-service/app.py)
- [SEC-003][High][A10] Uncaught model errors surfaced raw exceptions to clients. Fixed with sanitized 500 handling and logging. (model-service/app.py)
- [SEC-004][Med][A09] Lack of visibility when API auth disabled. Added startup warning if `ALLOW_NO_TOKEN` is true. (model-service/app.py)

# Commands Run
| Command | Purpose | Result |
| --- | --- | --- |
| `git status --short` | Baseline working tree state | pass |
| `cd model-service && pytest` | Run FastAPI service tests incl. new security regressions | pass (13 passed) |

# OWASP Top 10:2025 Matrix
| OWASP | Applicable | Status | Evidence | Findings | Remediation |
| --- | --- | --- | --- | --- | --- |
| A01 Broken Access Control | Y | Partial | Token header on `/predict`; `/health` open | SEC-004 (logging only) | Warned on unauthenticated mode; token enforced unless ALLOW_NO_TOKEN |
| A02 Security Misconfiguration | Y | Partial | docker-compose, env parsing | SEC-004 | Warning for insecure config; defaults require token |
| A03 Software Supply Chain Failures | Y | Unknown | requirements ranges, no lock | – | No change (unpinned deps remain) |
| A04 Cryptographic Failures | N | – | No crypto in scope | – | – |
| A05 Injection | Y | Partial | Upload handling | SEC-001 | MIME/format validation added |
| A06 Insecure Design | Y | Partial | Image limits, error handling | SEC-001/002 | Added format/pixel guards |
| A07 Authentication Failures | Y | Partial | Shared secret optional in local mode | SEC-004 | Added warning; auth required by default |
| A08 Software/Data Integrity Failures | Y | Partial | n8n workflow, no signing | – | Not addressed this pass |
| A09 Security Logging & Alerting Failures | Y | Partial | Structured logging | SEC-004 | Added configuration warning; errors logged |
| A10 Mishandling of Exceptional Conditions | Y | Pass | Error handling in `/predict` | SEC-002/003 | Sanitized 413/500 responses |

# OWASP Mobile Top 10:2024
- No mobile components detected (Not Applicable).
