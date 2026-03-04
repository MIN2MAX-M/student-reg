FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 \
 && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt \
 && rm -f /tmp/requirements.txt

COPY src/app ./app

RUN useradd -m -u 10001 appuser
USER appuser

EXPOSE 8000
CMD ["python", "-m", "app.main"]
