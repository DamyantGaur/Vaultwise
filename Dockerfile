# Vaultwise web app image. Started together with the model container by docker-compose.yml:
#   docker compose up -d
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY data/corpus ./data/corpus
COPY config.yaml ./

# private documents, index and logs live in /data (a Docker volume, never in the project folder)
RUN useradd --create-home --uid 1000 vaultwise && mkdir -p /data && chown vaultwise /data
USER vaultwise
ENV PYTHONPATH=/app/src \
    PYTHONUNBUFFERED=1 \
    VAULTWISE_DATA_DIR=/data \
    OLLAMA_BASE_URL=http://ollama:11434

EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4)"
CMD ["python", "-m", "uvicorn", "vaultwise.api:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
