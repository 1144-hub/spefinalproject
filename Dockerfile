# ---- Build Stage ----
# Uses a builder pattern to compile all C-extension dependencies (chromadb, torch)
# in a separate layer, keeping the final image lightweight and secure.
FROM python:3.11-slim AS builder

WORKDIR /app
# Step 1: Install uv, then install heavy ML dependencies (PyTorch) via the CPU-only index.
# This layer is ~1GB+ and cached independently of your code or requirements.txt.
RUN pip install --no-cache-dir uv && \
    uv pip install --system torch torchvision \
        --index-url https://download.pytorch.org/whl/cpu

# Step 2: Install application-specific requirements.
# Changing requirements.txt triggers only a small layer rebuild, NOT a re-download of torch.
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.11-slim

# Install curl for health checks (required by K8s liveness/readiness probes)
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create non-root user for security (Vault/K8s best practice)
RUN useradd -m -s /bin/bash appuser

# Copy installed packages from builder stage (entire local Python env)
COPY --from=builder /usr/local/lib /usr/local/lib
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code and automation scripts
COPY src/ ./src/
COPY data/ ./data/
COPY notebooks/ ./notebooks/
COPY scripts/ ./scripts/

# Models will be downloaded dynamically at runtime into the mounted HF_HOME volume
ENV HF_HOME=/app/.cache/huggingface

# Pre-create chroma_db directory and ensure script is executable
RUN mkdir -p /app/chroma_db && \
    chmod +x /app/scripts/start.sh && \
    chown -R appuser:appuser /app

# Health-check endpoint for K8s liveness probes and Docker healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Expose Streamlit default port
EXPOSE 8501

# Run as non-root user
USER appuser

# Use the startup wrapper script to handle auto-initialization
ENTRYPOINT ["/app/scripts/start.sh"]
