# Overview
Hardened the FastAPI model-service upload pipeline against spoofed uploads, pixel-bomb abuse, and error leakage; added configuration visibility and regression tests.

# Changes by Severity
## Critical/High
- Enforced server-side image format/MIME validation and mismatch rejection. (SEC-001)
- Treated decompression-bomb and over-pixel images as 413 with consistent enforcement. (SEC-002)
- Sanitized internal model errors to prevent leaking stack traces to clients. (SEC-003)

## Medium
- Added startup warning when `ALLOW_NO_TOKEN` disables authentication to avoid accidental unauthenticated deployments. (SEC-004)

# Changes by Area
- **Validation**: Strict MIME/format checks; pixel and upload-size enforcement.
- **Errors**: Sanitized internal errors; mapped bomb detections to 413.
- **Config**: Warn on insecure auth configuration.
- **Testing**: Added regression coverage for MIME spoofing, oversized uploads, pixel budget violations, and error masking.

# File-by-File Change List
- `model-service/app.py`: Added secure env parsing warnings, MIME/format validation, decompression-bomb handling to 413, sanitized prediction error handling, and auth-disable warning.
- `model-service/tests/test_app.py`: Added tests for content-type mismatch, oversized uploads, pixel-limit enforcement, and sanitized internal errors.
- `SECURITY_REPORT.md`: Recorded system map, findings, OWASP matrix, and commands run.
- `SECURITY_VERIFICATION.md`: Documented executed verification commands.
- `SECURITY_CHANGES.md`: This changelog.
- `docs/security.md`: Added operational security guidance for deployment and configuration.

# Verification Evidence
- `cd model-service && pytest` → pass (13 tests)

# Commands Executed
- `git status --short`
- `cd model-service && pytest`

# README Pending Items
- None; README.* left unchanged per protection rule.
