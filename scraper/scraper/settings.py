import logging

from scrapy.utils.log import configure_logging

import scraper.env as env
from pathlib import Path
from decouple import config

# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"

# LOG_FILE = env.get("LOG_FILE", allow_null=True)
# LOG_LEVEL = env.get("LOG_LEVEL", default="INFO")
# LOG_FORMATTER = "scraper.custom_log_formatter.CustomLogFormatter"

# configure_logging(settings={"LOG_FILE": LOG_FILE, "LOG_LEVEL": LOG_LEVEL, "LOG_FORMATTER": LOG_FORMATTER})

# fixes Scrapy DeprecationWarning on startup (Scrapy v2.10+)
# (see: https://docs.scrapy.org/en/latest/topics/request-response.html#request-fingerprinter-implementation):

# Default behaviour for regular crawlers of non-license-controlled content
# When set True, every item will have GROUP_EVERYONE attached in edu-sharing
# When set False, no permissions are set at all, which can be helpful if you want to control them later (e.g. via inherition)
DEFAULT_PUBLIC_STATE = False

# Splash (Web Thumbnailer)
# Will be rolled out via docker-compose by default
SPLASH_URL = None if env.get_bool("DISABLE_SPLASH", default=False) else env.get("SPLASH_URL")
SPLASH_WAIT = 2  # seconds to let the page load
SPLASH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}  # use chrome to not create warnings on pages

# edu-sharing config
EDU_SHARING_BASE_URL = env.get("EDU_SHARING_BASE_URL")
EDU_SHARING_USERNAME = env.get("EDU_SHARING_USERNAME")
EDU_SHARING_PASSWORD = env.get("EDU_SHARING_PASSWORD")

# z-api config
Z_API_KEY = env.get("Z_API_KEY")

# Thumbnail config
THUMBNAIL_SMALL_SIZE = 250 * 250
THUMBNAIL_SMALL_QUALITY = 40
THUMBNAIL_LARGE_SIZE = 800 * 800
THUMBNAIL_LARGE_QUALITY = 60
THUMBNAIL_MAX_SIZE = 1 * 1024 * 1024  # max size for images that can not be converted (e.g. svg)

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "scraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "scraper.middlewares.ScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "scraper.middlewares.ScraperDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
    "scrapy.extensions.periodic_log.PeriodicLog": 0,
}
# PeriodicLog Extension Settings
# (see: https://docs.scrapy.org/en/latest/topics/extensions.html#periodic-log-extension)
PERIODIC_LOG_STATS = True
PERIODIC_LOG_DELTA = True
PERIODIC_LOG_TIMING_ENABLED = True

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# ITEM_PIPELINES is set in the Scraper's custom_settings
# ITEM_PIPELINES = {
#     "scraper.pipelines.ScraperPipeline": 300,
# }
# storeMode = env.get("MODE", default="edu-sharing")
# ITEM_PIPELINES = {
#     "converter.pipelines.EduSharingCheckPipeline": 0,
#     "converter.pipelines.FilterSparsePipeline": 25,
#     "converter.pipelines.LOMFillupPipeline": 100,
#     "converter.pipelines.NormLicensePipeline": 125,
#     "converter.pipelines.NormLanguagePipeline": 150,
#     "converter.pipelines.ConvertTimePipeline": 200,
#     "converter.pipelines.ProcessValuespacePipeline": 250,
#     "converter.pipelines.ProcessThumbnailPipeline": 300,
# }
# match storeMode:
#     case "None" | None:
#         ITEM_PIPELINES.update({"converter.pipelines.DummyPipeline": 1000})
#     case "csv":
#         ITEM_PIPELINES.update({"converter.pipelines.CSVStorePipeline": 1000})
#     case "edu-sharing":
#         ITEM_PIPELINES.update({"converter.pipelines.EduSharingStorePipeline": 1000})
#     case "json":
#         ITEM_PIPELINES.update({"converter.pipelines.JSONStorePipeline": 1000})
#     case "jsonl":
#         ITEM_PIPELINES.update(
#             {
#                 "converter.pipelines.JSONLinesStorePipelineRaw": 5,
#                 "converter.pipelines.JSONLinesStorePipelineProcessed": 1000,
#             }
#         )
#     case _:
#         logging.info(
#             f"MODE-value '{storeMode}' not recognized! Please check your '.env'-Settings! "
#             f"Defaulting to MODE = 'edu-sharing'"
#         )
#         ITEM_PIPELINES.update({"converter.pipelines.EduSharingStorePipeline": 1000})

# # add custom pipelines from the .env file, if any
# ADDITIONAL_PIPELINES = env.get("CUSTOM_PIPELINES", True)
# if ADDITIONAL_PIPELINES:
#     for pipe in map(lambda p: p.split(":"), ADDITIONAL_PIPELINES.split(",")):
#         logging.info("Enabling custom pipeline: " + pipe[0])
#         ITEM_PIPELINES[pipe[0]] = int(pipe[1])

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# Enables useful test exports with `scrapy crawl -o my-test-output.json <spider>`
# The order of these fields determines how they appear in the output file, therefore we're sorting these fields from
# most-important to least-important metadata fields for debugging (spammy fields appear last):
FEED_EXPORT_FIELDS = [
    "sourceId",
    "hash",
    "origin",
    "lastModified",
    "license",
    "lom",
    "publisher",
    "valuespaces",
    "valuespaces_raw",
    "ai_prompts",
    "kidra_raw",
    # metadata fields which aren't used as often
    "collection",
    "custom",
    "notes",
    "permissions",
    "ranking",
    "status",
    "uuid",
    "fulltext",
    # Response cannot be serialized since it has `bytes` keys
    # "response",
    # Too much clutter:
    # "binary",
    # "screenshot_bytes",
    # "thumbnail",
]
FEED_EXPORT_INDENT = 2
FEED_EXPORT_ENCODING = "utf-8"

default_db_path = Path(__file__).resolve().parents[2] / "ui" / "db.sqlite3"
DB_PATH = config("DB_PATH", default_db_path)

LOG_LEVEL = "INFO"

GENERIC_CRAWLER_DB_PATH = env.get("GENERIC_CRAWLER_DB_PATH", allow_null=True)
GENERIC_CRAWLER_USE_LLM_API = env.get_bool("GENERIC_CRAWLER_USE_LLM_API", default=False)
GENERIC_CRAWLER_LLM_API_KEY = env.get("GENERIC_CRAWLER_LLM_API_KEY", default="")
GENERIC_CRAWLER_LLM_API_BASE_URL = env.get("GENERIC_CRAWLER_LLM_API_BASE_URL",
                                           default="https://chat-ai.academiccloud.de/v1")
GENERIC_CRAWLER_LLM_MODEL = env.get("GENERIC_CRAWLER_LLM_MODEL",
                                    default="meta-llama-3.1-8b-instruct")
