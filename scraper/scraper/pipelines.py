# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import sqlite3

from asgiref.sync import sync_to_async
from scrapy.item import Item
from scrapy.spiders import Spider

log = logging.getLogger(__name__)


class ScraperPipeline:
    def open_spider(self, spider: Spider):
        # TODO: we need to somehow make sure that writes are serialized, otherwise we risk corruption
        # when inserting items.
        self.connection = sqlite3.connect(
            spider.settings.get('DB_PATH'), check_same_thread=False)
        self.cursor = self.connection.cursor()

    @sync_to_async
    def process_item(self, item: Item, spider: Spider) -> Item:
        # request_url = item['request_url']
        url = item['url']

        log.info("Saving URL %r", url)

        job_id = item['job_id']
        self.cursor.execute(
            "INSERT INTO crawls_crawledurl (crawl_job_id, url, created_at, updated_at, content) VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '')", (job_id, url))
        self.connection.commit()
        return item
