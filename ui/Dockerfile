FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app/ui

# Git is needed to fetch git-sourced dependencies (djangorestframework)
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy
# Place venv outside /app/ui so dev volume mounts don't shadow it
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

# Install dependencies using the lockfile (layer cached separately from app code)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

COPY . /app/ui
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV DJANGO_VITE_DEV_MODE=False
CMD ["uv", "run", "gunicorn", "crawler_ui.wsgi", "--bind", "0.0.0.0:8000"]
