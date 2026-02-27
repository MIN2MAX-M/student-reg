# ---------- BUILDER STAGE ----------
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Requirements moved to src/
COPY src/requirements.txt .

RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ---------- RUNTIME STAGE ----------
FROM python:3.12-slim

WORKDIR /app
RUN useradd -m appuser

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl \
 && rm -rf /wheels

# App code moved under src/app
COPY src/app ./app

USER appuser
EXPOSE 8000
CMD ["python", "-m", "app.main"]
