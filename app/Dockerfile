FROM python:3.12-slim

# Create non-root user
RUN useradd -m appuser || true

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source as non-root owner
COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 5000

# Runtime tuning via environment variables (can be overridden in compose)
ENV GUNICORN_WORKERS=3 \
	GUNICORN_THREADS=2 \
	GUNICORN_TIMEOUT=30

# Ensure entrypoint is executable and use it to compute workers dynamically
RUN chmod +x /app/entrypoint.sh || true

ENTRYPOINT ["/app/entrypoint.sh"]