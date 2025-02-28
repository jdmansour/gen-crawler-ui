import logging
import sys
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from metadataenricher import env
from metadataenricher.metadata_enricher import MetadataEnricher
from pydantic import ValidationError, BaseModel
from pydantic_settings import BaseSettings


## Settings
class Settings(BaseSettings):
    api_key: str

try:
    settings = Settings()  # type: ignore
except ValidationError as e:
    print(e)
    sys.exit(1)


## Authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return None


## Logging
@asynccontextmanager
async def lifespan(app: FastAPI):
    """ Set up logging """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("uvicorn.error").propagate = False
    yield


## Main app
app = FastAPI(lifespan=lifespan)

@app.get("/metadata")
async def get_metadata(url: str, dependencies=Depends(validate_api_key)):
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
