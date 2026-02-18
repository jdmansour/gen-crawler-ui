
import json
import logging
import os
import sqlite3
import time

import redis
from scrapy.settings import BaseSettings
from scrapy.spiders import Spider

log = logging.getLogger(__name__)


class StateHelper:
    settings: BaseSettings

    def __init__(self, dry_run: bool, crawler_id: int | None, crawl_job_id: int | None):
        self.dry_run = dry_run
        self.crawler_id = crawler_id
        self.crawl_job_id = crawl_job_id
        self.items_processed = 0

        # Redis setup for status updates
        self.redis_client = None
        if not self.dry_run:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
            try:
                self.redis_client = redis.from_url(redis_url)
                log.info("Redis client initialized with URL: %s", redis_url)
            except redis.RedisError as e:
                log.warning("Could not connect to Redis: %s", e)
                self.redis_client = None

    def setup(self, settings: BaseSettings):
        self.settings = settings

    def update_spider_state(self, spider: Spider, state: str):
        """ Updates the CrawlJob instance in the database and publishes to Redis. """

        log.info("Updating spider %s state to %s", spider.name, state)
        if self.dry_run:
            return

        try:
            # Update database
            connection = sqlite3.connect(spider.settings.get('DB_PATH'))
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE crawls_crawljob SET state=?, updated_at=CURRENT_TIMESTAMP WHERE id=?",
                (state, self.crawl_job_id))
            connection.commit()
            connection.close()
            log.info("Updated crawl job %d state to %s",
                     self.crawl_job_id, state)

            # Publish to Redis for real-time updates
            if self.redis_client:
                try:
                    connection = sqlite3.connect(
                        spider.settings.get('DB_PATH'))
                    cursor = connection.cursor()
                    # select state and count of crawled urls
                    cursor.execute("SELECT state, (SELECT COUNT(*) FROM crawls_crawledurl WHERE crawl_job_id=?) FROM crawls_crawljob WHERE id=?",
                                   (self.crawl_job_id, self.crawl_job_id))
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

                    new_state = self.recalc_crawler_state()
                    status_data = {
                        'type': 'crawler_update',
                        'crawler_id': self.crawler_id,
                        'state': new_state,
                        'timestamp': time.time()
                    }
                    self.redis_client.publish(channel, json.dumps(status_data))
                    log.info(
                        "Published status update to Redis channel: %s", channel)
                except Exception as redis_error:
                    log.warning("Failed to publish to Redis: %s", redis_error)

        except Exception as e:
            log.error("Error updating crawl job state: %s", e)

    def recalc_crawler_state(self) -> str:
        """Recalculate the crawler state from crawl job states in the database."""
        log.info("Recalculating crawler state for crawler_id %d", self.crawler_id)

        db_path = self.settings.get('DB_PATH')
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        # any exploration crawl jobs running or pending?
        cursor.execute(
            "SELECT 1 FROM crawls_crawljob WHERE crawler_id=? AND crawl_type='EXPLORATION' AND state IN ('RUNNING', 'PENDING') LIMIT 1", (self.crawler_id,))
        if cursor.fetchone():
            connection.close()
            return 'EXPLORATION_RUNNING'
        # no exploration crawl jobs completed or canceled?
        cursor.execute(
            "SELECT 1 FROM crawls_crawljob WHERE crawler_id=? AND crawl_type='EXPLORATION' AND state IN ('COMPLETED', 'CANCELED') LIMIT 1", (self.crawler_id,))
        if not cursor.fetchone():
            # check if latest exploration job failed
            cursor.execute(
                "SELECT state FROM crawls_crawljob WHERE crawler_id=? AND crawl_type='EXPLORATION' ORDER BY created_at DESC LIMIT 1", (self.crawler_id,))
            row = cursor.fetchone()
            connection.close()
            if row and row[0] == 'FAILED':
                return 'EXPLORATION_REQUIRED_JOB_FAILED'
            return 'EXPLORATION_REQUIRED'
        # any content crawl jobs running or pending?
        cursor.execute(
            "SELECT 1 FROM crawls_crawljob WHERE crawler_id=? AND crawl_type='CONTENT' AND state IN ('RUNNING', 'PENDING') LIMIT 1", (self.crawler_id,))
        if cursor.fetchone():
            connection.close()
            return 'CONTENT_CRAWL_RUNNING'
        # check if latest content job failed
        cursor.execute(
            "SELECT state FROM crawls_crawljob WHERE crawler_id=? AND crawl_type='CONTENT' ORDER BY created_at DESC LIMIT 1", (self.crawler_id,))
        row = cursor.fetchone()
        connection.close()
        if row and row[0] == 'FAILED':
            return 'READY_FOR_CONTENT_CRAWL_JOB_FAILED'
        return 'READY_FOR_CONTENT_CRAWL'

    def publish_progress_update(self, current_url: str):
        """ Publishes progress update to Redis. """
        if self.redis_client:
            try:
                # TODO: can we use items_processed from the exploration scraper instead of hitting the database every time? 
                # Count crawled URLs for this job
                connection = sqlite3.connect(self.settings.get('DB_PATH'))
                cursor = connection.cursor()
                # select state and count of crawled urls
                cursor.execute("SELECT state, (SELECT COUNT(*) FROM crawls_crawledurl WHERE crawl_job_id=?) FROM crawls_crawljob WHERE id=?",
                               (self.crawl_job_id, self.crawl_job_id))
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
                log.debug(
                    "Published progress update: %d items processed", self.items_processed)
            except (sqlite3.Error, redis.RedisError) as e:
                log.warning("Failed to publish progress update: %s", e)

    def spider_opened(self, spider: Spider, start_url: str, follow_links: bool, crawl_type: str):
        if self.dry_run:
            return

        db_path = self.settings.get('DB_PATH')
        log.info("Using database at %s", db_path)
        log.info("File exists? %s", os.path.exists(db_path))

        scrapy_job_id = getattr(spider, '_job', None)  # type: ignore
        log.info("Scrapy job id: %s", scrapy_job_id)

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        # Insert if not exists, else update
        if self.crawl_job_id is None:
            # Create new crawl job row
            cursor.execute("""INSERT INTO crawls_crawljob (start_url, follow_links, crawler_id, created_at, updated_at, state, scrapy_job_id, crawl_type)
                                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'RUNNING', ?, ?)""",
                           (start_url, int(follow_links), self.crawler_id, scrapy_job_id, crawl_type))
            self.crawl_job_id = cursor.lastrowid
            log.info("Created new crawl job in database with id %d",
                     self.crawl_job_id)
        else:
            # Update CrawlJob in database:
            # - set state to RUNNING
            # - set update_at to current timestamp
            # - set scrapy_job_id if available
            cursor.execute("UPDATE crawls_crawljob SET state='RUNNING', updated_at=CURRENT_TIMESTAMP, scrapy_job_id=? WHERE id=?",
                           (scrapy_job_id, self.crawl_job_id))
            log.info("Updated crawl job %d to RUNNING", self.crawl_job_id)

        connection.commit()
        connection.close()

        # send out initial state update
        self.update_spider_state(spider, 'RUNNING')
