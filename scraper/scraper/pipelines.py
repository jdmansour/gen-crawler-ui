# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import sqlite3

from scrapy.item import Item
from scrapy.spiders import Spider
from scraper.spiders.example import NoindexItem, CustomItem

log = logging.getLogger(__name__)


class ScraperPipeline:
    def open_spider(self, spider: Spider):
        # TODO: we need to somehow make sure that writes are serialized, otherwise we risk corruption
        # when inserting items.
        if spider.dry_run:
            log.info("Dry run mode enabled, not saving items to database.")
            return
        self.connection = sqlite3.connect(
            spider.settings.get('DB_PATH'), check_same_thread=False)
        self.cursor = self.connection.cursor()

    def process_item(self, item: Item, spider: Spider) -> Item:
        # log.info("Processing item: %r", item)
        if spider.dry_run:
            return item
        # request_url = item['request_url']
        url = item['url']
        job_id = item['job_id']

        if isinstance(item, CustomItem):
            log.info("Saving URL %r", url)
            self.cursor.execute(
                "INSERT OR IGNORE INTO crawls_crawledurl (crawl_job_id, url, created_at, updated_at, content, noindex) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '', 0)", (job_id, url))
            self.connection.commit()
        elif isinstance(item, NoindexItem):
            log.info("Marking URL %r as noindex", url)
            # set noindex = 1, updated_at = CURRENT_TIMESTAMP
            # for this job id and url
            self.cursor.execute(
                "UPDATE crawls_crawledurl SET noindex = 1, updated_at = CURRENT_TIMESTAMP WHERE crawl_job_id = ? AND url = ?", (job_id, url))
            self.connection.commit()

        return item
