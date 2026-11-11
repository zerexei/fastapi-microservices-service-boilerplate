# ==========================================
# Stage 1: Build dependencies and virtual environment
# ==========================================
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS builder

WORKDIR /app

# Optimize uv settings for container builds
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Step 1: Install dependencies first (leveraging Docker cache layers)
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

# Step 2: Copy application source code and install the project itself
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# ==========================================
# Stage 2: Minimal production runtime image
# ==========================================
FROM python:3.12-slim-trixie

WORKDIR /app

# Install essential runtime utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root system user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Runtime environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Copy only the pre-built virtual environment and source code from builder stage
COPY --from=builder /app/.venv /app/.venv
COPY . /app

# Ensure non-root user owns the app directory
RUN chown -R appuser:appuser /app

USER appuser

# Run the app (production mode: no --reload)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]