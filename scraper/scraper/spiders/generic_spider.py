from __future__ import annotations

import datetime
import logging
import sqlite3
from typing import Optional

import playwright.async_api
import scrapy.signals
from metadataenricher import metadata_enricher
from metadataenricher.metadata_enricher import MetadataEnricher
from scrapy.exceptions import CloseSpider
from scrapy.http.response import Response
from scrapy.http.response.text import TextResponse
from scrapy.spiders import Spider
from scrapy.spiders.crawl import Rule

import scraper
from scraper.es_connector import EduSharing

from .. import env
from ..util.generic_crawler_db import fetch_urls_passing_filterset
from .state_helper import StateHelper
from .utils import check_db

log = logging.getLogger(__name__)


class GenericSpider(Spider):
    name = "generic_spider"
    friendlyName = "generic_spider"  # name as shown in the search ui
    version = "0.1.4"
    start_urls = []
    rules = [Rule(callback="parse")]
    custom_settings = {
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

    def __init__(self, urltocrawl:str="", ai_enabled:str="True",
                 max_urls:str="3", filter_set_id:str="",
                 crawler_id:str|None=None, crawl_job_id:str|None=None, **kwargs):
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
        self.crawl_job_id: Optional[int] = int(crawl_job_id) if crawl_job_id else None
        self.crawler_id: Optional[int] = int(crawler_id) if crawler_id else None
        self.items_processed = 0
        self.spider_failed = False
        self.crawler_output_node: Optional[str] = None
        self.dry_run = False

        if crawler_id is None:
            log.info("No crawler_id provided, this is a dry run without "
                     "database updates or Redis status publishing.")
            self.dry_run = True

        if self.dry_run:
            del self.custom_settings["ITEM_PIPELINES"]["scraper.pipelines_edusharing.EduSharingStorePipeline"]

        try:
            ai_enabled_bool = to_bool(ai_enabled)
        except ValueError:
            log.error("Invalid value for ai_enabled: %s", ai_enabled)
            raise

        self.enricher = MetadataEnricher(ai_enabled=ai_enabled_bool)
        self.state_helper = StateHelper(self.dry_run,
            int(crawler_id) if crawler_id else None,
            int(crawl_job_id) if crawl_job_id else None)

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
        check_db(self.settings)
        self.state_helper.setup(self.settings)

        log.info("Filter set ID: %s", self.filter_set_id)
        log.info("GENERIC_CRAWLER_DB_PATH: %s", self.settings.get('GENERIC_CRAWLER_DB_PATH'))
        log.info("DB_PATH: %s", self.settings.get('DB_PATH'))
        db_path = self.settings.get('GENERIC_CRAWLER_DB_PATH')

        # If we have a filter set id, we can load URLs from the DB.
        if self.filter_set_id is not None:
            try:
                connection = sqlite3.connect(db_path)

                # Load URLs from the latest exploration crawl passing this filter set
                matches = fetch_urls_passing_filterset(
                    connection, self.filter_set_id, limit=self.max_urls)
                log.info("Adding %d URLs to start_urls", len(matches))
                for row in matches:
                    self.start_urls.append(row.url)

                if not self.dry_run:
                    # get crawler_id from FilterSet
                    cursor = connection.cursor()
                    cursor.execute(
                        "SELECT crawler_id FROM crawls_filterset WHERE id=?", (self.filter_set_id,))
                    if row := cursor.fetchone():
                        self.state_helper.crawler_id = row[0]
                    else:
                        # Stop the crawl
                        log.error("No crawler_id found for filter_set_id %s", self.filter_set_id)
                        self.spider_failed = True
                        raise CloseSpider(f"No crawler_id found for filter_set_id {self.filter_set_id}.")

                    self.state_helper.spider_opened(spider, "", True, 'CONTENT')

            except (sqlite3.Error, ValueError) as e:
                log.error("Error while running crawler: %s", e)
                self.spider_failed = True
                raise CloseSpider(f"Error while running crawler: {e}") from e

        self.enricher.setup(self.settings)

    def spider_closed(self, spider: GenericSpider):
        """ Called when the spider is closed. """
        log.info("Closed spider %s", spider.name)
        if self.dry_run:
            return

        if self.spider_failed:
            self.state_helper.update_spider_state(spider, 'FAILED')
        else:
            self.state_helper.update_spider_state(spider, 'COMPLETED')

    def spider_error(self, failure, response, spider: GenericSpider):  # pylint: disable=unused-argument
        """ Called when the spider encounters an error. """
        log.error("Spider %s encountered an error: %s", spider.name, failure)
        self.spider_failed = True
        # TODO: add "if not failed" check in database to update_spider_state
        self.state_helper.update_spider_state(spider, 'FAILED')

    def getId(self, response: Optional[Response] = None) -> str:
        """Return a stable identifier (URI) of the crawled item"""
        assert response
        return response.url

    def getHash(self, response: Optional[Response] = None) -> str:  # pylint: disable=unused-argument
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
        logging.info("Item %s (uuid: %s) has not changed", self.getId(response), db[0])
        return False

    async def parse(self, response: Response):
        if not self.hasChanged(response):
            return

        if not isinstance(response, TextResponse):
            log.warning("Response is not a TextResponse, but %s, skipping: %s", type(response), response.url)
            return
        
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

        if not item:
            log.warning("Could not extract metadata for %s", response.url)
            return

        log.info("New URL processed:------------------------------------------")
        log.info(item)
        log.info("------------------------------------------------------------")

        # Track processed items for progress updates
        self.items_processed += 1

        # Send progress update every 10 items
        if self.items_processed % 10 == 0:
            self.state_helper.publish_progress_update(response.url)

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
