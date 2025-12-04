FROM python:3.11-slim

# Create a non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install curl for health checks and debugging
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./

# Switch to non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
