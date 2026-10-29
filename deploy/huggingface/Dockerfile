# Vaultwise cloud image: the app + Ollama (CPU only) + the models, in one container.
# Built by Hugging Face Spaces (Docker SDK) and by the CI pipeline's end-to-end test.
# Spaces runs containers as uid 1000 and routes traffic to app_port 7860.
ARG OLLAMA_VERSION=latest

# ---- stage 1: the model engine, minus GPU libraries, plus the models ------------------------------
FROM ollama/ollama:${OLLAMA_VERSION} AS engine
# The official image ships ~4.7 GB of CUDA/Vulkan libraries; a CPU-only server needs none of them.
RUN rm -rf /usr/lib/ollama/cuda_* /usr/lib/ollama/mlx_cuda_* /usr/lib/ollama/rocm* /usr/lib/ollama/vulkan
ENV OLLAMA_MODELS=/opt/ollama/models OLLAMA_HOST=127.0.0.1:11434
# The 8B summary model is left out: on a shared 2-vCPU host it is too slow, so summaries use the 3B model.
RUN mkdir -p /opt/ollama/models \
 && (ollama serve >/tmp/ollama-build.log 2>&1 &) \
 && for i in $(seq 1 60); do ollama list >/dev/null 2>&1 && break; sleep 1; done \
 && ollama pull llama3.2:3b \
 && ollama pull nomic-embed-text

# ---- stage 2: the runtime image ------------------------------------------------------------------
FROM ubuntu:24.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
COPY --from=engine /usr/bin/ollama /usr/bin/ollama
COPY --from=engine /usr/lib/ollama /usr/lib/ollama
COPY --from=engine --chmod=755 /opt/ollama /opt/ollama

WORKDIR /app
COPY requirements.txt .
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY data/corpus ./data/corpus
COPY samples ./samples
COPY config.yaml start.sh ./
RUN chmod +x start.sh && mkdir -p /tmp/vaultwise && chmod 777 /tmp/vaultwise

ENV PATH=/opt/venv/bin:$PATH \
    HOME=/tmp \
    PYTHONUNBUFFERED=1 \
    OLLAMA_MODELS=/opt/ollama/models \
    OLLAMA_HOST=127.0.0.1:11434 \
    VAULTWISE_MODE=cloud \
    VAULTWISE_PRELOAD_SAMPLES=1 \
    VAULTWISE_DATA_DIR=/tmp/vaultwise \
    VAULTWISE_SUMMARY_MODEL=llama3.2:3b \
    PORT=7860
EXPOSE 7860
CMD ["./start.sh"]
