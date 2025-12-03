.PHONY: run build test lint

run:
	cd model-service && uvicorn app:app --reload --host 0.0.0.0 --port 8000

build:
	cd model-service && docker build -t digitization-qc-model .

test:
	cd model-service && pytest tests/

lint:
	cd model-service && pip install flake8 && flake8 app.py
