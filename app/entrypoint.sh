#!/bin/bash
set -euo pipefail

# Compute default number of workers if not set: (2 * CPUs) + 1
if [ -z "${GUNICORN_WORKERS:-}" ]; then
  GUNICORN_WORKERS=$(python - <<'PY'
import multiprocessing
cores = multiprocessing.cpu_count()
print((cores * 2) + 1)
PY
)
fi

: "Using config: workers=$GUNICORN_WORKERS threads=${GUNICORN_THREADS:-2} timeout=${GUNICORN_TIMEOUT:-30}" >&2

exec gunicorn -b 0.0.0.0:5000 \
  -w "$GUNICORN_WORKERS" \
  --threads "${GUNICORN_THREADS:-2}" \
  --timeout "${GUNICORN_TIMEOUT:-30}" \
  --access-logfile - \
  --error-logfile - \
  app:app
