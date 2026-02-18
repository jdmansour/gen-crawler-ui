# Stage 1: Build the frontend web component
FROM node:22-slim AS frontend-builder

WORKDIR /frontend-spa
COPY frontend-spa/package.json ./
RUN npm install
COPY frontend-spa/ ./
RUN npx vite build --mode library

# Stage 2: Django web app
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app/ui

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Place venv outside /app/ui so dev volume mounts don't shadow it
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Install dependencies using the lockfile (layer cached separately from app code)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=ui/uv.lock,target=uv.lock \
    --mount=type=bind,source=ui/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

COPY ui/ /app/ui/

# Copy frontend build output into Django app's static directory
COPY --from=frontend-builder /frontend-spa/dist/ /app/ui/crawls/static/gen-crawler/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV DJANGO_VITE_DEV_MODE=False

# Collect all static files (including frontend web component) into STATIC_ROOT
RUN uv run python manage.py collectstatic --no-input
CMD ["uv", "run", "gunicorn", "crawler_ui.wsgi", "--bind", "0.0.0.0:8000"]
