# Repo Profile
- Stack: Python 3 / FastAPI service in `model-service`; n8n workflow JSON; Airtable schema/docs in repo.
- Entry points: `make run` (uvicorn dev), `docker-compose up` (model-service + n8n), API at `/predict` and `/health`.
- Tests: Pytest suite in `model-service/tests`.
- Key deps: fastapi, uvicorn, pillow, python-multipart.
- Config: `.env` consumed by Docker Compose and FastAPI (MODEL_API_TOKEN, size limits).
- Security: optional shared-secret header `x-api-token`; ALLOW_NO_TOKEN for local.
- Data flow: Upload image -> validate -> placeholder model scoring -> structured JSON (quality/defects/report).
- Operational concerns: image size limits via env; Pixel bomb guard via Pillow MAX_IMAGE_PIXELS.
- Observations: error handling mixes JSONResponse/HTTPException; MIME relies on client-provided content type.

# Findings
- [P1][Fixed] Predict endpoint trusted client-declared MIME types, allowing spoofed uploads. (model-service/app.py)
- [P1][Fixed] Internal exceptions were returned in API responses, leaking stack details and skipping model error trapping. (model-service/app.py)
- [P1][Fixed] Misconfigured size/env inputs could crash startup or return 500s during size checks. Added guarded parsing and size handling. (model-service/app.py)

# Fixes Applied
- Enforced safe env parsing for upload/pixel limits and preserved fast failure semantics without crashes. (model-service/app.py)
- Added bounded size validation and hardened image open path with true format checks plus content-type mismatch handling. (model-service/app.py)
- Wrapped model inference errors with sanitized 500 responses and logging; added MIME/size/error coverage tests. (model-service/app.py, model-service/tests/test_app.py)

# How to Validate
- `cd model-service && pytest`
- `make run` (local dev server)
- `docker-compose up` (model-service + n8n; requires .env)
