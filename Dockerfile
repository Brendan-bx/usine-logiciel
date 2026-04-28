# ---- Stage 1 : dependencies ----
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2 : runtime ----
FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/OWNER/devops-taskmanager"
LABEL org.opencontainers.image.description="Task Manager Flask API"

WORKDIR /app

COPY --from=builder /install /usr/local
COPY app/ ./app/

RUN mkdir -p /var/log/app

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--workers", "1", "--threads", "4", \
     "--access-logfile", "-", \
     "app.main:app"]
