
# # Install uv.
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# Copy the application into the container.
COPY metadataapi /app/metadataapi
# Copy dependencies next to it
COPY metadataenricher /app/metadataenricher
COPY valuespace-converter /app/valuespace-converter

# Install the application dependencies.
WORKDIR /app/metadataapi
# Place the .venv outside of the application directory,
# so if we mount it (in dev mode) we don't affect the
# .venv on the host.
ENV UV_PROJECT_ENVIRONMENT=/app/.venv
RUN uv sync --frozen --no-cache
# Populate the valuespace cache
RUN uv run python -m valuespace_converter.valuespaces

# Run the application.
CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "8081", "--host", "0.0.0.0"]