from __future__ import annotations

import datetime
import json
import logging
import os
import sqlite3
import time
from typing import Optional

import playwright.async_api
import redis
import scrapy.http
import scrapy.signals
from scrapy.exceptions import CloseSpider
from scrapy.http.response import Response
from scrapy.http.response.text import TextResponse
from scrapy.spiders import Spider
from scrapy.spiders.crawl import Rule

import scraper
from metadataenricher.metadata_enricher import MetadataEnricher
from metadataenricher import metadata_enricher
from scraper.es_connector import EduSharing

from .. import env
from ..util.generic_crawler_db import fetch_urls_passing_filterset

log = logging.getLogger(__name__)


class GenericSpider(Spider):
    name = "generic_spider"
    friendlyName = "generic_spider"  # name as shown in the search ui
    version = "0.1.4"
    start_urls = []
    rules = [Rule(callback="parse")]
    custom_settings = {
        "WEB_TOOLS": "playwright",
        "ROBOTSTXT_OBEY": False,
        "ITEM_PIPELINES": {
            "scraper.pipelines_edusharing.EduSharingCheckPipeline": 0,
            "scraper.pipelines_edusharing.FilterSparsePipeline": 25,
            "scraper.pipelines_edusharing.LOMFillupPipeline": 100,
            "scraper.pipelines_edusharing.NormLicensePipeline": 125,
            "scraper.pipelines_edusharing.NormLanguagePipeline": 150,
            "scraper.pipelines_edusharing.ConvertTimePipeline": 200,
            "scraper.pipelines_edusharing.ProcessValuespacePipeline": 250,
            "scraper.pipelines_edusharing.ProcessThumbnailPipeline": 300,
            "scraper.pipelines_edusharing.JSONStorePipeline": 1000,
            "scraper.pipelines_edusharing.EduSharingStorePipeline": 1000,
        }
    }

    def __init__(self, urltocrawl="", ai_enabled="True",
                 max_urls="3", filter_set_id="", crawler_id=None, crawl_job_id=None, **kwargs):
        EduSharing.resetVersion = True
        super().__init__(**kwargs)

        log.info("Initializing GenericSpider version %s", self.version)
        log.info("Arguments:")
        log.info("  urltocrawl: %r", urltocrawl)
        log.info("  ai_enabled: %r", ai_enabled)
        log.info("  max_urls: %r", max_urls)
        log.info("  filter_set_id: %r", filter_set_id)
        log.info("  kwargs: %r", kwargs)
        log.info("scraper module: %r", scraper)
        log.info("__file__: %r", __file__)


        if urltocrawl and filter_set_id:
            raise ValueError("You must set either 'urltocrawl' or 'filter_set_id', not both.")

        if not urltocrawl and not filter_set_id:
            raise ValueError("You must set either 'urltocrawl' or 'filter_set_id'.")

        if filter_set_id != "":
            self.filter_set_id = int(filter_set_id)
        else:
            self.filter_set_id = None

        self.max_urls = int(max_urls)

        if urltocrawl != "":
            urls = [url.strip() for url in urltocrawl.split(",")]
            self.start_urls = urls[:self.max_urls]

        # logging.warning("self.start_urls=" + self.start_urls[0])
        self.crawl_job_id: Optional[int] = crawl_job_id
        self.crawler_id: Optional[int] = crawler_id
        self.items_processed = 0
        self.spider_failed = False
        self.crawler_output_node: Optional[str] = None

        try:
            ai_enabled = to_bool(ai_enabled)
        except ValueError:
            log.error("Invalid value for ai_enabled: %s", ai_enabled)
            raise

        self.enricher = MetadataEnricher(ai_enabled=ai_enabled)

        # Shared with ExampleSpider
                # Redis setup for status updates
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        try:
            self.redis_client = redis.from_url(redis_url)
            log.info("Redis client initialized with URL: %s", redis_url)
        except Exception as e:
            log.warning("Could not connect to Redis: %s", e)
            self.redis_client = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        # pylint: disable=E1101
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=scrapy.signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=scrapy.signals.spider_closed)
        crawler.signals.connect(spider.spider_error, signal=scrapy.signals.spider_error)
        return spider

    def spider_opened(self, spider: GenericSpider):
        """ Run when the spider is opened, before the crawl begins.
            Open the database and get the list of URLs to crawl. """

        log.info("Opened spider %s version %s", spider.name, spider.version)
        # TODO: synchronize DB loading logic with ExampleSpider
        db_path = self.settings.get('GENERIC_CRAWLER_DB_PATH')
        log.info("Using database at %s", db_path)
        if db_path is not None:
            log.info("File exists? %s", os.path.exists(db_path))
        if db_path is None or not os.path.exists(db_path):
            log.error(
                "No database set or database not found. Please set GENERIC_CRAWLER_DB_PATH.")
            return

        if not self.filter_set_id:
            return

        log.info("Filter set ID: %s", self.filter_set_id)
        # List filter rules in this filter set
        try:
            connection = sqlite3.connect(db_path)

            matches = fetch_urls_passing_filterset(connection, self.filter_set_id, limit=self.max_urls)

            log.info("Adding %d URLs to start_urls", len(matches))
            for row in matches:
                log.info("Adding URL to start_urls: %s", row.url)
                self.start_urls.append(row.url)

            # get crawler_id from FilterSet
            cursor = connection.cursor()
            cursor.execute("SELECT crawler_id FROM crawls_filterset WHERE id=?", (self.filter_set_id,))
            row = cursor.fetchone()
            if row:
                self.crawler_id = row[0]
            else:
                # Stop the crawl
                log.error("No crawler_id found for filter_set_id %s", self.filter_set_id)
                self.spider_failed = True
                raise CloseSpider(f"No crawler_id found for filter_set_id {self.filter_set_id}.")

            scrapy_job_id = getattr(spider, '_job', None)  # type: ignore
            log.info("Scrapy job id: %s", scrapy_job_id)

            if self.crawl_job_id is None:
                # e.g. launched from command line
                # Add a new CrawlJob entry in the database

                #cursor = connection.cursor()
                cursor.execute("""INSERT INTO crawls_crawljob (start_url, follow_links, crawler_id, created_at, updated_at, state, scrapy_job_id, crawl_type)
                                  VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'RUNNING', ?, 'CONTENT')""",
                                ("", 1, self.crawler_id, scrapy_job_id))
                self.crawl_job_id = cursor.lastrowid
            else:
                # Launched from the web app
                # Update CrawlJob entry to set state to RUNNING
                cursor.execute("UPDATE crawls_crawljob SET state='RUNNING', updated_at=CURRENT_TIMESTAMP, scrapy_job_id=? WHERE id=?", (scrapy_job_id, self.crawl_job_id))
                log.info("Updated crawl job %d to RUNNING", self.crawl_job_id)
                
            connection.commit()
            connection.close()
            log.info("Created new crawl job in database with id %d", self.crawl_job_id)
        except (sqlite3.Error, ValueError) as e:
            log.error("Error while running crawler: %s", e)
            self.spider_failed = True
            raise CloseSpider(f"Error while running crawler: {e}") from e

        self.enricher.setup(self.settings)

    def update_spider_state(self, spider: GenericSpider, state: str):
        """ Updates the CrawlJob instance in the database and publishes to Redis. """

        log.info("Updating spider %s state to %s", spider.name, state)
        try:
            # Update database
            connection = sqlite3.connect(self.settings.get('DB_PATH'))
            cursor = connection.cursor()
            cursor.execute("UPDATE crawls_crawljob SET state=?, updated_at=CURRENT_TIMESTAMP WHERE id=?", (state, self.crawl_job_id))
            connection.commit()
            connection.close()
            log.info("Updated crawl job %d state to %s", self.crawl_job_id, state)

            # Publish to Redis for real-time updates
            if self.redis_client:
                try:
                    connection = sqlite3.connect(self.settings.get('DB_PATH'))
                    cursor = connection.cursor()
                    # select state and count of crawled urls
                    cursor.execute("SELECT state, (SELECT COUNT(*) FROM crawls_crawledurl WHERE crawl_job_id=?) FROM crawls_crawljob WHERE id=?", (self.crawl_job_id, self.crawl_job_id))
                    row = cursor.fetchone()
                    connection.close()
                    if row:
                        crawl_job_state = row[0]
                        crawl_job_crawled_url_count = row[1]
                    else:
                        crawl_job_state = 'UNKNOWN'
                        crawl_job_crawled_url_count = 0 

                    status_data = {
                        'type': 'crawl_job_update',
                        'crawler_id': self.crawler_id,
                        'crawl_job': {
                            'id': self.crawl_job_id,
                            'state': crawl_job_state,
                            'crawled_url_count': crawl_job_crawled_url_count,
                        },
                        'items_processed': self.items_processed,
                        'current_url': None,
                        'timestamp': time.time()
                    }
                    channel = f'crawler_status_{self.crawler_id}'
                    self.redis_client.publish(channel, json.dumps(status_data))
                    log.info("Published status update to Redis channel: %s", channel)
                except Exception as redis_error:
                    log.warning("Failed to publish to Redis: %s", redis_error)
            
        except Exception as e:
            log.error("Error updating crawl job state: %s", e)

    def _publish_progress_update(self, current_url: str):
        """ Publishes progress update to Redis. """
        if self.redis_client:
            try:
                # Count crawled URLs for this job
                connection = sqlite3.connect(self.settings.get('DB_PATH'))
                cursor = connection.cursor()
                # select state and count of crawled urls
                cursor.execute("SELECT state, (SELECT COUNT(*) FROM crawls_crawledurl WHERE crawl_job_id=?) FROM crawls_crawljob WHERE id=?", (self.crawl_job_id, self.crawl_job_id))
                row = cursor.fetchone()
                connection.close()
                if row:
                    crawl_job_state = row[0]
                    crawl_job_crawled_url_count = row[1]
                else:
                    crawl_job_state = 'UNKNOWN'
                    crawl_job_crawled_url_count = 0

                progress_data = {
                    'type': 'crawl_job_update',
                    'crawler_id': self.crawler_id,
                    'crawl_job': {
                        'id': self.crawl_job_id,
                        'state': crawl_job_state,
                        'crawled_url_count': crawl_job_crawled_url_count,
                    },
                    'items_processed': self.items_processed,
                    'current_url': current_url,
                    'timestamp': time.time()
                }
                channel = f'crawler_status_{self.crawler_id}'
                self.redis_client.publish(channel, json.dumps(progress_data))
                log.debug("Published progress update: %d items processed", self.items_processed)
            except Exception as e:
                log.warning("Failed to publish progress update: %s", e)

    def spider_closed(self, spider: GenericSpider):
        """ Called when the spider is closed. """
        log.info("Closed spider %s", spider.name)
        if self.spider_failed:
            self.update_spider_state(spider, 'FAILED')
        else:
            self.update_spider_state(spider, 'COMPLETED')

    def spider_error(self, failure, response, spider: GenericSpider):
        """ Called when the spider encounters an error. """
        log.error("Spider %s encountered an error: %s", spider.name, failure)
        self.update_spider_state(spider, 'FAILED')

    def getId(self, response: Optional[Response] = None) -> str:
        """Return a stable identifier (URI) of the crawled item"""
        assert response
        return response.url

    def getHash(self, response: Optional[Response] = None) -> str:
        """
        Return a stable hash to detect content changes (for future crawls).
        """
        return f"{datetime.datetime.now().isoformat()}v{self.version}"

    def hasChanged(self, response: Response) -> bool:
        # if self.forceUpdate:
        #     return True
        # if self.uuid:
        #     if self.getUUID(response) == self.uuid:
        #         logging.info(f"matching requested id: {self.uuid}")
        #         return True
        #     return False
        # if self.remoteId:
        #     if str(self.getId(response)) == self.remoteId:
        #         logging.info(f"matching requested id: {self.remoteId}")
        #         return True
        #     return False
        db = EduSharing().find_item(self.getId(response), self)
        if db is None or db[1] != self.getHash(response):
            return True
        else:
            logging.info(f"Item {self.getId(response)} (uuid: {db[0]}) has not changed")
            return False

    async def parse(self, response: Response):
        if not self.hasChanged(response):
            return
        
        assert isinstance(response, TextResponse)

        # Respect robots meta tags
        robot_meta_tags: list[str] = response.xpath(
            "//meta[@name='robots']/@content").getall()
        respect_robot_meta_tags = env.get_bool(
            key="RESPECT_ROBOT_META_TAGS", allow_null=True, default=True)
        if robot_meta_tags and respect_robot_meta_tags:
            # There are 3 Robot Meta Tags (<meta name="robots" content="VALUE">) that we need to
            # respect:
            # - "noindex"       (= don't index the current URL)
            # - "nofollow"      (= don't follow any links on this site)
            # - "none"          (= shortcut for combined value "noindex, nofollow")
            # by default, we try to respect the webmaster's wish to not be indexed/crawled
            if "noindex" in robot_meta_tags:
                log.info(
                    "Robot Meta Tag 'noindex' identified. Aborting further parsing of item: %s .",
                    response.url)
                return
            if "nofollow" in robot_meta_tags:
                # ToDo: don't follow any links, but parse the current response
                #  -> yield response with 'nofollow'-setting in cb_kwargs
                log.info(
                    "Robot Meta Tag 'nofollow' identified. Parsing item %s , but WILL NOT "
                    "follow any links found within.", response.url
                )
            if "none" in robot_meta_tags:
                log.info(
                    "Robot Meta Tag 'none' identified (= 'noindex, nofollow'). "
                    "Aborting further parsing of item: %s itself and any links within it.",
                    response.url
                )
                return

        try:
            item = await self.enricher.parse_page(response_url=response.url)
        except metadata_enricher.AuthenticationError as auth_error:
            log.error("Authentication error while enriching metadata for %s: %s",
                      response.url, auth_error)
            self.spider_failed = True
            raise CloseSpider(f"Authentication error: {auth_error}") from auth_error
        except playwright.async_api.Error as e:
            log.error("Playwright error while enriching metadata for %s: %s",
                      response.url, e)
            self.spider_failed = True
            raise CloseSpider(f"Playwright error: {e}") from e

        # item["custom"]["generic_crawler_name"] = "test"

        log.info("New URL processed:------------------------------------------")
        log.info(item)
        log.info("------------------------------------------------------------")

        # Track processed items for progress updates
        self.items_processed += 1
        
        # Send progress update every 10 items
        if self.items_processed % 10 == 0:
            self._publish_progress_update(response.url)

        yield item


def to_bool(value: str) -> bool:
    """ Converts a string to a bool. Yes, true, t, 1 is True.
        No, false, f, 0 is False. The function is case insensitive.
        Returns a ValueError if the argument is something else.
    """

    if value.lower() in ("yes", "true", "t", "1"):
        return True
    if value.lower() in ("no", "false", "f", "0"):
        return False
    raise ValueError(f"Invalid boolean value: {value}")
