# syntax=docker/dockerfile:1          # enables BuildKit features

FROM python:3.10-slim AS base

# Security first – don’t run as root
RUN adduser --disabled-password --gecos "" appuser
WORKDIR /app
USER appuser

# Copy source *after* installing deps, so dependency layers are cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the repo
COPY . .

# The command your app starts with – adjust to your entrypoint
CMD ["python", "-m", "your_package.__main__"]
