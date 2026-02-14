from __future__ import annotations

import json
import logging
import sqlite3
from urllib.parse import urlparse

import openai
import scrapy
import scrapy.signals
from scrapy.crawler import Crawler
from scrapy.exceptions import CloseSpider
from scrapy.http.response import Response
from scrapy.http.response.text import TextResponse
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from .state_helper import StateHelper
from .utils import check_db

log = logging.getLogger(__name__)


class CustomItem(scrapy.Item):
    job_id = scrapy.Field()
    # The url of this item
    url = scrapy.Field()
    # The url that this item was found on
    request_url = scrapy.Field()
    # The url that linked to this page, None if it is the start page
    from_url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    # Distance from the crawl root, 0 = start page, 1 = linked from start page, etc.
    depth = scrapy.Field()


class HierarchyAnalysisItem(scrapy.Item):
    job_id = scrapy.Field()
    url = scrapy.Field()
    breadcrumbs_found = scrapy.Field()
    breadcrumb_selector = scrapy.Field()
    breadcrumb_item_selector = scrapy.Field()
    breadcrumbs = scrapy.Field()


class NoindexItem(scrapy.Item):
    """ Used to mark a page as noindex. """
    job_id = scrapy.Field()
    url = scrapy.Field()


class ExampleSpider(scrapy.Spider):
    name = "example"
    # allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]
    # rules = [
    #     Rule(LxmlLinkExtractor())
    # ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.pipelines.ScraperPipeline': 300,
        },
        'FEED_EXPORT_FIELDS': None,
    }
    llm_client: openai.OpenAI
    crawler_id: int | None
    crawl_job_id: int | None
    follow_links: bool
    infer_hierarchy: bool

    def __init__(self, *args, start_url: str, crawler_id: str | None = None,
                 crawl_job_id: str | None = None, follow_links: bool = False,
                 infer_hierarchy: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.follow_links = to_bool(follow_links)
        self.link_extractor = LxmlLinkExtractor()
        self.items_processed = 0
        self.infer_hierarchy = infer_hierarchy
        self.dry_run = False
        self.spider_failed = False
        self.spider_canceled = False
        self.llm_model = ''

        if crawler_id is None:
            log.info("No crawler_id provided, this is a dry run without "
                     "database updates or Redis status publishing.")
            self.dry_run = True

        self.state_helper = StateHelper(self.dry_run,
                                        int(crawler_id) if crawler_id else None,
                                        int(crawl_job_id) if crawl_job_id else None)

        if self.infer_hierarchy:
            log.info("Hierarchy inference is enabled for this spider.")

    def setup_llm_client(self):
        log.info("Setting up LLM client for hierarchy inference")
        api_key = self.settings.get('GENERIC_CRAWLER_LLM_API_KEY', '')
        if not api_key:
            raise RuntimeError(
                "No API key set for LLM API. Please set GENERIC_CRAWLER_LLM_API_KEY.")

        base_url = self.settings.get('GENERIC_CRAWLER_LLM_API_BASE_URL', '')
        if not base_url:
            raise RuntimeError(
                "No base URL set for LLM API. Please set GENERIC_CRAWLER_LLM_API_BASE_URL.")

        self.llm_model = self.settings.get('GENERIC_CRAWLER_LLM_MODEL', '')
        if not self.llm_model:
            raise RuntimeError(
                "No model set for LLM API. Please set GENERIC_CRAWLER_LLM_MODEL.")

        log.info("Using LLM API with the following settings:")
        log.info("GENERIC_CRAWLER_LLM_API_KEY: <set>")
        log.info("GENERIC_CRAWLER_LLM_API_BASE_URL: %r", base_url)
        log.info("GENERIC_CRAWLER_LLM_MODEL: %r", self.llm_model)
        self.llm_client = openai.OpenAI(api_key=api_key, base_url=base_url)

    @classmethod
    def from_crawler(cls, crawler: Crawler, *args, **kwargs):
        # pylint: disable=E1101
        spider = super(ExampleSpider, cls).from_crawler(
            crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened,
                                signal=scrapy.signals.spider_opened)
        crawler.signals.connect(spider.spider_closed,
                                signal=scrapy.signals.spider_closed)
        crawler.signals.connect(spider.spider_error,
                                signal=scrapy.signals.spider_error)
        return spider

    def spider_opened(self, spider: ExampleSpider):
        """ Called when the spider is opened. """

        log.info("Opened spider %s", spider.name)
        check_db(self.settings)
        self.state_helper.setup(self.settings)

        if self.infer_hierarchy:
            self.setup_llm_client()

        if self.dry_run:
            return

        try:
            self.state_helper.spider_opened(
                spider, self.start_urls[0], self.follow_links, 'EXPLORATION')
        except (sqlite3.Error, ValueError) as e:
            log.error("Error updating crawl job state: %s", e)
            self.spider_failed = True
            raise CloseSpider("Failed to initialize crawl job state") from e

    def spider_closed(self, spider: ExampleSpider, reason: str):
        """ Called when the spider is closed. """
        log.info("Closed spider %s, reason: %s", spider.name, reason)
        if self.dry_run:
            return

        spider_cancelled = reason in ('cancelled', 'shutdown')

        # Check if the job was already canceled before overwriting the state
        if self.spider_failed:
            self.state_helper.update_spider_state(spider, 'FAILED')
        elif spider_cancelled:
            self.state_helper.update_spider_state(spider, 'CANCELED')
        else:
            self.state_helper.update_spider_state(spider, 'COMPLETED')

        # get statistics
        # if robotstxt/forbidden is 1 and downloader/request_count is 1,
        # then the crawl was blocked by robots.txt

        if spider.crawler.stats is None:
            log.warning("No stats available for spider %s", spider.name)
            return

        stats = spider.crawler.stats.get_stats()
        log.info("Crawl statistics: %s", stats)
        if (stats.get('robotstxt/forbidden', 0) >= 1 and
            stats.get('downloader/request_count', 0) == 1):
            log.warning("Crawl appears to have been blocked by robots.txt")
            self.state_helper.update_spider_state(spider, 'FAILED')

    def spider_error(self, failure, response, spider: ExampleSpider):  # pylint: disable=W0613
        """ Called when the spider encounters an error. """
        log.error("Spider %s encountered an error: %s", spider.name, failure)
        self.state_helper.update_spider_state(spider, 'FAILED')

    def parse(self, response: Response, from_url=None, depth=0):
        """
            from_url: the url that linked to this page, None if it is the start page
            respose.request.url: the url of this page
        """
        assert response.request is not None
        assert isinstance(response, TextResponse)
        request_origin = get_origin(response.request.url)
        # log.info("response.request.url: %s", response.request.url)
        # log.info("from_url: %s", from_url)

        # Get the value of the robots meta tag, if present
        tags = response.xpath('//meta[@name="robots"]/@content').getall()
        # log.info("Found robots tags: %s", tags)
        robots = []
        for tag in tags:
            parts = [x.strip() for x in tag.split(',')]
            robots.extend(parts)
        log.info("Parsed robots tags: %s", robots)
        if 'noindex' in robots or 'none' in robots:
            log.info("Page is marked as noindex, skipping")
            # Mark this page as noindex
            item = NoindexItem()
            item['job_id'] = self.state_helper.crawl_job_id
            item['url'] = response.request.url
            yield item
            return
        if 'nofollow' in robots:
            log.info("Page is marked as nofollow, not following links")
            # Leave this page in, but don't follow any links
            return

        # If these are base urls, scrapy *should* fill in the correct
        # base url (https://weltderphysik.de)
        for link in self.link_extractor.extract_links(response):
            if not self.crawler.crawling:
                log.info("Crawl has been stopped, exiting")
                return

            if get_origin(link.url) != request_origin:
                # print(f"Skipping {link.url}")
                log.info("Skipping %s", link.url)
                # print(f"Origin is {get_origin(link.url)}, request origin is {request_origin}")
                continue
            item = CustomItem()
            item['job_id'] = self.state_helper.crawl_job_id
            item['request_url'] = response.request.url
            item['url'] = link.url
            item['depth'] = depth + 1
            if from_url:
                item['from_url'] = from_url
            log.info("Found link %s", link.url)

            # Track processed items for progress updates
            self.items_processed += 1

            # Send progress update every 10 items
            if self.items_processed % 10 == 0:
                self.state_helper.publish_progress_update(link.url)

            yield item
            if self.follow_links:
                log.info("Following link %s", link.url)
                yield scrapy.Request(
                    link.url, callback=self.parse,
                    cb_kwargs={'from_url': response.url, 'depth': depth + 1})
                # yield response.follow(link, self.parse)

        # # find all links on the page that are to the same origin
        # origin = get_origin(response.url)
        # links = response.css('a::attr(href)').extract()
        if self.infer_hierarchy:
            html = response.text
            query = INFER_HIERARCHY_QUERY + "\n\n" + html

            chat_completion = self.llm_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an HTML analysis assistant. You extract structured data from HTML source code. You only report what is actually present in the HTML - never invent or assume content that isn't there."},
                    {"role": "user", "content": query},
                ],
                model=self.llm_model,
            )
            llm_response = chat_completion.choices[0].message.content
            assert llm_response is not None
            log.info("Hierarchy inference response: %s", llm_response)
            obj = extract_and_validate_json(llm_response)

            hierarchy_item = HierarchyAnalysisItem()
            hierarchy_item['job_id'] = self.state_helper.crawl_job_id
            hierarchy_item['url'] = response.request.url
            hierarchy_item['breadcrumbs_found'] = obj.get(
                'breadcrumbs_found', False)
            hierarchy_item['breadcrumb_selector'] = obj.get(
                'breadcrumb_selector', None)
            hierarchy_item['breadcrumb_item_selector'] = obj.get(
                'breadcrumb_item_selector', None)
            
            # Resolve relative breadcrumb URLs to absolute using the page URL
            raw_breadcrumbs = obj.get('breadcrumbs', [])
            for crumb in raw_breadcrumbs:
                if crumb.get('url'):
                    crumb['url'] = response.urljoin(crumb['url'])

            # If the current page is not in the breadcrumbs, add it as the last breadcrumb
            if raw_breadcrumbs and (raw_breadcrumbs[-1].get('url') != response.request.url):
                title = response.xpath('//title/text()').get() or "(no title)"
                raw_breadcrumbs.append({"name": title, "url": response.request.url})

            log.info("Extracted breadcrumbs: %s", json.dumps(raw_breadcrumbs, indent=2))

            hierarchy_item['breadcrumbs'] = raw_breadcrumbs
            yield hierarchy_item


def extract_and_validate_json(response: str) -> dict:
    """
    Extracts JSON object from between <answer> tags and validates it.
    Raises ValueError if the JSON is invalid or if the tags are not found.
    """
    start_tag = "<answer>"
    end_tag = "</answer>"
    start_index = response.find(start_tag)
    end_index = response.find(end_tag)
    if start_index == -1 or end_index == -1:
        raise ValueError("Response does not contain <answer> tags")
    json_str = response[start_index + len(start_tag):end_index].strip()
    try:
        obj = json.loads(json_str)
        # TODO: validate that obj has the expected structure
        return obj
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}") from e


INFER_HIERARCHY_QUERY = """
Extract breadcrumb navigation from the HTML below.

CRITICAL RULES:
1. Only report breadcrumbs if there are actual <a> links INSIDE a breadcrumb container.
2. A breadcrumb container is an element with "breadcrumb" in its class, id, or aria-label attribute.
3. If the breadcrumb container exists but is EMPTY or contains no <a> links, set breadcrumbs_found to false.
4. Do NOT report sidebar navigation, header menus, or footer links as breadcrumbs.
5. It is better to report no breadcrumbs than to hallucinate them.

STEPS:
1. Search for elements with "breadcrumb" in class/id/aria-label.
2. If found, check whether the element contains <a> links. If it is empty or has no links, return breadcrumbs_found: false.
3. If no breadcrumb container exists, look for a horizontal link list separated by ">" or "/" that represents page hierarchy. Do NOT confuse this with sidebar or main navigation.
4. Extract breadcrumb links in hierarchical order (home -> current page). Omit irrelevant items (login links, duplicate current-page links) and set breadcrumb_items_skip accordingly.

Respond with JSON wrapped in <answer> tags:

Page WITH breadcrumbs:
<answer>
{"breadcrumbs_found": true, "breadcrumb_selector": "nav.breadcrumbs", "breadcrumb_item_selector": "nav.breadcrumbs a", "breadcrumb_items_skip": 0, "breadcrumbs": [{"name": "Home", "url": "/"}, {"name": "Category", "url": "/category"}]}
</answer>

Page WITHOUT breadcrumbs (including empty breadcrumb containers):
<answer>
{"breadcrumbs_found": false, "breadcrumb_selector": null, "breadcrumb_item_selector": null, "breadcrumb_items_skip": null, "breadcrumbs": []}
</answer>

Before your <answer>, briefly state what you found (e.g. "Found nav[data-qa=breadcrumbs] but it contains no links" or "Found 3 breadcrumb links in ol.breadcrumb").

----
"""


def get_origin(url: str):
    """
    Returns the scheme (http, https), domain and port of a given url.

    >>> get_origin('https://example.com:8080/blah/blub')
    'https://example.com:8080'
    >>> get_origin('blah.com/test')
    'http://blah.com'
    """
    parsed = urlparse(url)
    if parsed.scheme == '':
        parsed = urlparse(f'http://{url}')
    return f"{parsed.scheme}://{parsed.netloc}"


def to_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    if value.lower() in ['true', '1']:
        return True
    if value.lower() in ['false', '0']:
        return False
    raise ValueError(f"Cannot convert {value} to boolean")
