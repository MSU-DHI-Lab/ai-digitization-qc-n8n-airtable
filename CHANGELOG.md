## Unreleased

### Stability
- Hardened `/predict` to reject spoofed MIME/format mismatches and to sanitize internal errors before returning to clients.
- Hardened env configuration handling so invalid `MAX_UPLOAD_MB` and `MAX_PIXELS` values fall back to safe defaults instead of disabling limits or rejecting all requests.
- Switched shared-secret auth token checking to constant-time comparison to reduce timing side-channel risk.

### Maintainability
- Centralized env parsing and image/size validation helpers to keep request handling small and predictable.
- Reduced `/predict` branching by extracting authorization and pixel-budget enforcement into focused helper functions.
- Reduced pytest setup duplication with reusable environment reload helpers.

### Testing/Verification
- Added regression tests for MIME mismatches, oversized uploads, and sanitized internal errors (`model-service/tests/test_app.py`).
- Added regression tests for invalid `MAX_UPLOAD_MB` and invalid `MAX_PIXELS` fallback behavior (`model-service/tests/test_app.py`).
- Added verification that auth codepath uses constant-time token comparison (`model-service/tests/test_app.py`).

### Notes / Deferred
- None.
