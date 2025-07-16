# syntax=docker/dockerfile:1
FROM python:3.10-slim AS base

# ─── basic hardening ─────────────────────────────────────────────
RUN adduser --disabled-password --gecos "" appuser
WORKDIR /app
USER appuser

# ─── copy full source first (simplest / safest) ──────────────────
COPY . .

# ─── install dependencies if they exist ──────────────────────────
# 1) classic requirements.txt
# 2) pyproject.toml / setup.cfg   → falls back to “pip install .”
RUN python -m pip install --upgrade pip --no-cache-dir \
 && if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt ; \
    elif [ -f pyproject.toml ] || [ -f setup.cfg ]; then \
        pip install --no-cache-dir . ; \
    else \
        echo "No dependency file found – skipping pip install"; \
    fi

# ─── default command (adjust to your app) ────────────────────────
CMD ["python", "-m", "your_package.__main__"]
