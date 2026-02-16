# ---------- BUILDER STAGE ----------
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Build wheels into /wheels (not mixed with other files)
RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels


# ---------- RUNTIME STAGE ----------
FROM python:3.12-slim

WORKDIR /app

RUN useradd -m appuser

# Copy only wheels (no requirements.txt)
COPY --from=builder /wheels /wheels

# Install wheels
RUN pip install --no-cache-dir /wheels/*.whl \
 && rm -rf /wheels

# Copy app code only
COPY app ./app

USER appuser

EXPOSE 8000
CMD ["python", "-m", "app.main"]
