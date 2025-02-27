
# First stage: build the egg file

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS build-stage

# Copy deps
COPY scraper /workdir/scraper
COPY metadataenricher /workdir/metadataenricher
COPY valuespace-converter /workdir/valuespace-converter

# Build
WORKDIR /workdir/scraper
RUN uv sync
RUN uv run scrapyd-deploy --build-egg=1738306332.egg

# Main stage: build the scrapyd container

FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /workdir/app

# Copy deps
COPY metadataenricher /workdir/metadataenricher
COPY valuespace-converter /workdir/valuespace-converter
COPY scraper/edu_sharing_client /workdir/app/edu_sharing_client

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=scraper/uv.lock,target=uv.lock \
    --mount=type=bind,source=scraper/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev
    # uv sync --frozen --no-install-project --no-dev

# Scrapy config
VOLUME /etc/scrapyd/ /var/lib/scrapyd/
COPY scraper/scrapyd.conf /etc/scrapyd/

# Copy the built egg
RUN mkdir -p /workdir/app/eggs
# The name of the project is "scraper"
COPY --from=build-stage /workdir/scraper/1738306332.egg /workdir/app/eggs/scraper/1738306332.egg

EXPOSE 6800
ENV DB_PATH=/workdir/app/database/db.sqlite
ENV PATH="/workdir/app/.venv/bin:$PATH"

ENTRYPOINT []

# We have to mount /app/database in the docker compose file.
CMD ["scrapyd", "--pidfile="]
