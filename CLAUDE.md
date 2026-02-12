# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Generic Web Crawler for WLO (Wirlernenonline). A full-stack application that crawls educational websites, extracts metadata using AI/LLM, and integrates with the edu-sharing learning management system.

## Architecture

Monorepo with 5 services sharing a single SQLite database (`database/db.sqlite3`):

- **frontend-spa/** — React 19 + TypeScript + MUI 7 SPA (Vite build)
- **ui/** — Django 5.2 backend, REST API (DRF), SSE real-time updates via Redis
- **scraper/** — Scrapy spiders deployed via Scrapyd; two crawl types: exploration (discover URLs) and content (extract metadata)
- **metadataapi/** — FastAPI service exposing metadata extraction as an API
- **metadataenricher/** — Core Python library for metadata extraction (JSON-LD, OpenGraph, LLM, Z-API/KIdra)
- **valuespace-converter/** — Library for converting educational metadata to standardized taxonomies

Inter-service communication: Django talks to Scrapyd over HTTP and to the frontend via REST + SSE. Scraper imports metadataenricher as a library. All services share the SQLite DB via volume mount in Docker.

## Development Commands

### Frontend (frontend-spa/)
```bash
cd frontend-spa
npm install
npm run dev          # Vite dev server with HMR
npm run build        # tsc -b && vite build
npm run lint         # ESLint
npm run storybook    # Storybook on port 6006
```

### Django Backend (ui/)
```bash
cd ui
uv sync              # Install all deps (including dev group)
uv run python manage.py migrate
uv run python manage.py runserver
uv run pytest
uv run pylint crawls/
```

### Scraper (scraper/)
Uses `uv` for package management. metadataenricher and valuespace-converter are editable local dependencies.
```bash
cd scraper
uv sync
uv run scrapy crawl example -a start_url=https://example.com
uv run pytest
uv run mypy .
```

### Docker (full stack)
```bash
source env-gwdg.sh   # Required: sets env vars for edu-sharing, LLM, Z-API keys

# Production
docker compose up --build

# Dev mode (Vite HMR)
DJANGO_VITE_DEV_MODE=true docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

### Frontend Tests
```bash
cd frontend-spa
npx vitest           # Unit tests
npx playwright test  # Browser tests
```

## Key Environment Variables

Required in docker-compose (see `env.sh`, `env-gwdg.sh`, `env-openai.sh` for templates):
- `EDU_SHARING_BASE_URL`, `EDU_SHARING_USERNAME`, `EDU_SHARING_PASSWORD` — edu-sharing integration
- `Z_API_KEY` — KIdra educational analysis API
- `GENERIC_CRAWLER_USE_LLM_API`, `GENERIC_CRAWLER_LLM_API_KEY`, `GENERIC_CRAWLER_LLM_MODEL` — LLM config
- `DB_PATH` — SQLite database path
- `SCRAPYD_URL` — Scrapyd service URL
- `REDIS_URL` — Redis for real-time event aggregation

## Key Data Models (ui/crawls/models.py)

- **SourceItem** — edu-sharing content source
- **Crawler** — Crawler definition with start URL and config
- **CrawlJob** — Individual crawl run (exploration or content type)
- **CrawledURL** — URLs discovered during crawls
- **FilterSet / FilterRule** — URL pattern include/exclude rules

## Code Conventions

- Python: pylint with Django plugin (config in `ui/pyproject.toml`), mypy for type checking
- TypeScript: ESLint + Prettier
- Python package management: `uv` for all subprojects (each has its own `pyproject.toml` and `uv.lock`)
- Frontend can also build as a web component for embedding in edu-sharing
