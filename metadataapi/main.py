import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from scraper import env
from scraper.spiders.metadata_enricher import MetadataEnricher


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Set up logging """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("uvicorn.error").propagate = False
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/metadata")
async def get_metadata(url: str):
    enricher = MetadataEnricher(ai_enabled=True)
    settings = {
        'GENERIC_CRAWLER_DB_PATH': env.get("GENERIC_CRAWLER_DB_PATH", allow_null=True),
        'GENERIC_CRAWLER_USE_LLM_API': env.get_bool("GENERIC_CRAWLER_USE_LLM_API", default=False),
        'GENERIC_CRAWLER_LLM_API_KEY': env.get("GENERIC_CRAWLER_LLM_API_KEY", default=""),
        'GENERIC_CRAWLER_LLM_API_BASE_URL': env.get("GENERIC_CRAWLER_LLM_API_BASE_URL",
                                           default="https://chat-ai.academiccloud.de/v1"),
        'GENERIC_CRAWLER_LLM_MODEL': env.get("GENERIC_CRAWLER_LLM_MODEL",
                                    default="meta-llama-3.1-8b-instruct"),
    }
    enricher.setup(settings)
    result = await enricher.parse_page(url)
    return result