from __future__ import annotations

import datetime
import logging
import os
import sqlite3
from typing import Optional

import scrapy.http
import scrapy.signals
from scrapy.http.response import Response
from scrapy.http.response.text import TextResponse
from scrapy.spiders import Spider
from scrapy.spiders.crawl import Rule

import scraper
from scraper.es_connector import EduSharing
from scraper.util.sitemap import find_generate_sitemap

from .. import env
from ..util.generic_crawler_db import fetch_urls_passing_filterset
from ..web_tools import WebEngine
from .metadata_enricher import MetadataEnricher

log = logging.getLogger(__name__)


class GenericSpider(Spider):
    name = "generic_spider"
    friendlyName = "generic_spider"  # name as shown in the search ui
    version = "0.1.4"
    start_urls = []
    rules = [Rule(callback="parse")]
    custom_settings = {
        "WEB_TOOLS": WebEngine.Playwright,
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

    def __init__(self, urltocrawl="", ai_enabled="True", find_sitemap="False",
                 max_urls="3", filter_set_id="", **kwargs):
        EduSharing.resetVersion = True
        super().__init__(**kwargs)

        log.info("Initializing GenericSpider version %s", self.version)
        log.info("Arguments:")
        log.info("  urltocrawl: %r", urltocrawl)
        log.info("  ai_enabled: %r", ai_enabled)
        log.info("  find_sitemap: %r", find_sitemap)
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
            if find_sitemap == "True" and len(urls) == 1:
                sitemap_urls = find_generate_sitemap(
                    urls[0], max_entries=self.max_urls)
                self.start_urls = sitemap_urls
            else:
                self.start_urls = urls[:self.max_urls]

        # logging.warning("self.start_urls=" + self.start_urls[0])

        try:
            ai_enabled = to_bool(ai_enabled)
        except ValueError:
            log.error("Invalid value for ai_enabled: %s", ai_enabled)
            raise

        self.enricher = MetadataEnricher(ai_enabled=ai_enabled)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(
            spider.spider_opened, signal=scrapy.signals.spider_opened)  # pylint: disable=no-member
        return spider

    def spider_opened(self, spider: GenericSpider):
        """ Run when the spider is opened, before the crawl begins.
            Open the database and get the list of URLs to crawl. """

        log.info("Opened spider %s version %s", spider.name, spider.version)
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
        connection = sqlite3.connect(db_path)

        matches = fetch_urls_passing_filterset(connection, self.filter_set_id, limit=self.max_urls)

        log.info("Adding %d URLs to start_urls", len(matches))
        for row in matches:
            log.info("Adding URL to start_urls: %s", row.url)
            self.start_urls.append(row.url)

        self.enricher.setup(self.settings)

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

        item = await self.enricher.parse_page(response_url=response.url)

        log.info("New URL processed:------------------------------------------")
        log.info(item)
        log.info("------------------------------------------------------------")

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
