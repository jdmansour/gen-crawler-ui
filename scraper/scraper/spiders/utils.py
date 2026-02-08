
import logging
import os
from scrapy.settings import BaseSettings

log = logging.getLogger(__name__)

def check_db(settings: BaseSettings) -> str:
    db_path = settings.get('GENERIC_CRAWLER_DB_PATH', None)
    if db_path is None:
        raise RuntimeError("GENERIC_CRAWLER_DB_PATH is not set. Please set it to the path of your database.")
    if not os.path.exists(db_path):
        raise RuntimeError(f"Database not found at {db_path}. Please check your GENERIC_CRAWLER_DB_PATH setting.")
    return db_path
