## Unreleased

### Stability
- Hardened `/predict` to reject spoofed MIME/format mismatches and to sanitize internal errors before returning to clients.

### Maintainability
- Centralized env parsing and image/size validation helpers to keep request handling small and predictable.

### Testing/Verification
- Added regression tests for MIME mismatches, oversized uploads, and sanitized internal errors (`model-service/tests/test_app.py`).

### Notes / Deferred
- None.
