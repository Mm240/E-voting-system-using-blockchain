# Backend image. Build context is the repo root (the API reads frontend/src/abi/Voting.json).
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake git ffmpeg libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY backend/requirements-prod.txt backend/requirements-prod.txt
RUN pip install --no-cache-dir -r backend/requirements-prod.txt

COPY backend backend
COPY frontend/src/abi frontend/src/abi

WORKDIR /app/backend
ENV PYTHONUNBUFFERED=1
CMD gunicorn "app:create_app()" --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 4 --timeout 120
