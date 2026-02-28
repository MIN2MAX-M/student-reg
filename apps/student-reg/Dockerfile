# ---------- BUILDER STAGE ----------
FROM python:3.12-slim AS builder

WORKDIR /build

# Build tooling for any packages that need compilation (safe to keep in builder only)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Requirements moved to src/
COPY src/requirements.txt .

# Build wheels for *ALL* deps (important: no --no-deps)
RUN python -m pip install --upgrade pip \
 && pip wheel --no-cache-dir -r requirements.txt -w /wheels

# ---------- RUNTIME STAGE ----------
FROM python:3.12-slim

WORKDIR /app

# Runtime libs (libpq5 helps psycopg + is useful even if you later change driver)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 10001 appuser

# Install from wheelhouse (offline install)
COPY --from=builder /wheels /wheels
RUN python -m pip install --no-cache-dir /wheels/* \
 && rm -rf /wheels

# App code moved under src/app
COPY src/app ./app

USER appuser
EXPOSE 8000

CMD ["python", "-m", "app.main"]
