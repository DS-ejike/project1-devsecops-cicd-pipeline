# ============================================================
# HARDENED MULTI-STAGE DOCKERFILE
# Follows CIS Docker Benchmark recommendations
# ============================================================

# Stage 1: Builder (install dependencies, compile)
FROM python:3.12-slim AS builder

WORKDIR /build

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime (minimal, hardened)
FROM python:3.12-slim AS runtime

# CIS 4.1: Create non-root user
RUN groupadd -r appgroup && \
    useradd -r -g appgroup -d /app -s /sbin/nologin appuser

# CIS 4.6: Add HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Copy only the virtual environment from builder (no build tools)
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
WORKDIR /app
COPY . .

# CIS 4.1: Run as non-root
USER appuser

# CIS 4.9: Use EXPOSE to document the port
EXPOSE 8080

# CIS 4.7: Do not use ADD, use COPY
# CIS 4.10: Do not store secrets in Dockerfile

# Use exec form for proper signal handling
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
