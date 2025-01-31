from __future__ import annotations

import datetime
import json
import logging
import os
import re
import sqlite3
from typing import Optional

import httpx
import openai
import scrapy.http
import scrapy.signals
import trafilatura  # type: ignore
from bs4 import BeautifulSoup
from scrapy.http.response import Response
from scrapy.http.response.text import TextResponse
from scrapy.spiders import Spider
from scrapy.spiders.crawl import Rule

import zapi
import zapi.api
import zapi.api.ai_text_prompts
import zapi.api.ai_text_prompts.prompt
import zapi.errors
import zapi.models
from scraper.util.sitemap import find_generate_sitemap
from valuespace_converter.app.valuespaces import Valuespaces
from zapi.api.kidra import (predict_subjects_kidra_predict_subjects_post,
                            text_stats_analyze_text_post,
                            topics_flat_topics_flat_post)

from .. import env
from ..items import (AiPromptItemLoader, BaseItemLoader, KIdraItemLoader,
                     LicenseItemLoader, LomBaseItemloader,
                     LomClassificationItemLoader, LomEducationalItemLoader,
                     LomGeneralItemloader, LomLifecycleItemloader,
                     LomTechnicalItemLoader, ResponseItemLoader,
                     ValuespaceItemLoader)
from ..util.generic_crawler_db import fetch_urls_passing_filterset
from ..util.license_mapper import LicenseMapper
from ..web_tools import WebEngine, WebTools
from .base_classes import LrmiBase
import scraper

log = logging.getLogger(__name__)


class GenericSpider(Spider, LrmiBase):
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

    clean_tags = ["nav", "header", "footer"]
    prompts = {
        "description": "Fasse folgenden Text in 3 Sätzen zusammen: %(text)s",
        "keyword": "Liefere 4 Schlagworte für folgenden Text: %(text)s",
        "discipline": "Für welche Schul bzw. Fachgebiete eignet sich folgender Text: %(text)s",
        "educationalContext": "Für welche Bildungsstufe eignet sich folgender Text: %(text)s",
        "new_lrt": "Welche Materialart im schulischen Kontext ist folgender Text: %(text)s",
        "intendedEndUserRole": "Für welche Zielgruppen eignet sich folgender Text: %(text)s",
    }
    ALL_IN_ONE_PROMPT = """Folgender Text ist ein Bildungsmaterial von einer Webseite. Bitte extrahiere folgende Informationen:

description: Gebe eine Beschreibung und Zusammenfassung der Quelle in 3 Sätzen.
keywords: Finde 3-5 Schlagworte die den Text beschreiben.
discipline: Für welche Schul- bzw. Fachgebiete eignet sich das Material?
educationalContext: Für welche Bildungsstufen eignet sich das Material? Berücksichtige die Sprachschwierigkeit des Textes und die Altersangemessenheit der Formulierung. (Mögliche Antworten: Elementarbereich, Schule, Primarstufe, Sekundarstufe I, Sekundarstufe II, Hochschule, Berufliche Bildung, Fortbildung, Erwachsenenbildung, Förderschule, Fernunterricht, Informelles Lernen)
new_lrt: Welche Materialart im schulischen Kontext stellt die Quelle dar? (Text, Bild, Tool, ...)
intendedEndUserRole: Für welche Zielgruppen eignet sich das Material? (Lerner/in, Lehrer/in, Eltern, Autor/in, ...)

Antworte im JSON-Format, und gebe keinen weiteren Text aus:
{
  "description": "Deine Beschreibung der Quelle",
  "keywords": ["thema1", "thema2"],
  "discipline": ["Geographie"],
  "educationalContext" ["Primarstufe"],
  "new_lrt": ["Text"],
  "intendedEndUserRole": ["Lehrer/in", "Lerner/in"]
}

Hier folgt der Text:
%(text)s
"""
    valuespaces: Valuespaces
    ai_enabled: bool
    zapi_client: zapi.AuthenticatedClient
    llm_client: Optional[openai.OpenAI] = None
    use_llm_api: bool = False
    llm_model: str = ""

    def __init__(self, urltocrawl="", validated_result="", ai_enabled="True", find_sitemap="False",
                 max_urls="1", filter_set_id="", **kwargs):
        super().__init__(**kwargs)

        log.info("Initializing GenericSpider version %s", self.version)
        log.info("Arguments:")
        log.info("  urltocrawl: %r", urltocrawl)
        log.info("  validated_result: %r", validated_result)
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

        self.results_dict = {}
        if urltocrawl != "":
            urls = [url.strip() for url in urltocrawl.split(",")]
            if find_sitemap == "True" and len(urls) == 1:
                sitemap_urls = find_generate_sitemap(
                    urls[0], max_entries=self.max_urls)
                self.start_urls = sitemap_urls
            else:
                self.start_urls = urls[:self.max_urls]

        if validated_result != "":
            self.results_dict = json.loads(validated_result)
            urltocrawl = self.results_dict["url"]
            self.start_urls = [urltocrawl]

        # logging.warning("self.start_urls=" + self.start_urls[0])
        self.valuespaces = Valuespaces()

        try:
            self.ai_enabled = to_bool(ai_enabled)
        except ValueError:
            log.error("Invalid value for ai_enabled: %s", ai_enabled)
            raise

        if self.ai_enabled:
            log.info("Starting generic_spider with ai_enabled flag!")
            self.zapi_client = zapi.AuthenticatedClient(
                token=env.get("Z_API_KEY", False),
                prefix='',
                auth_header_name="X-API-KEY",
                base_url="https://ai-prompt-service.staging.openeduhub.net",
                raise_on_unexpected_status=True
            )
        else:
            log.info(
                "Starting generic_spider with MINIMAL settings. AI Services are DISABLED!")
            # this optional flag allows us to control if we want to use
            # AI-suggested metadata. We can compare the items gathered
            # by the "generic_spider_minimal" against the (AI-enabled)
            # "generic_spider"
            self.name = "generic_spider_minimal"
            self.friendlyName = "generic_spider_minimal"

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

        self.setup_llm_client()

    def setup_llm_client(self):
        self.use_llm_api = self.settings.get('GENERIC_CRAWLER_USE_LLM_API', False)
        log.info("GENERIC_CRAWLER_USE_LLM_API: %r", self.use_llm_api)
        if not self.use_llm_api:
            return

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

    def getId(self, response: Optional[Response] = None) -> str:
        """Return a stable identifier (URI) of the crawled item"""
        assert response
        return response.url

    def getHash(self, response: Optional[Response] = None) -> str:
        """
        Return a stable hash to detect content changes (for future crawls).
        """
        return f"{datetime.datetime.now().isoformat()}v{self.version}"

    async def parse(self, response: Response):
        if not self.hasChanged(response):
            return

        url_data = await WebTools.getUrlData(response.url, engine=WebEngine.Playwright)
        if not url_data:
            log.warning("Playwright failed to fetch data for %s", response.url)
            return

        response = response.copy()
        assert isinstance(response, TextResponse)

        # ToDo: validate "trafilatura"-fulltext-extraction from playwright
        # (compared to the html2text approach)
        playwright_text: str = url_data["html"] or ""
        playwright_bytes: bytes = playwright_text.encode()
        trafilatura_text = url_data["text"]
        log.info("trafilatura_text: %s", trafilatura_text)
        # ToDo: implement text extraction .env toggle: default / advanced / basic?
        #  - default: use trafilatura by default?
        #  - advanced: which trafilatura parameters could be used to improve text extraction for
        #    "weird" results?
        #  - basic: fallback to html2text extraction (explicit .env setting)
        # trafilatura_meta_scrapy = trafilatura.extract_metadata(response.body).as_dict()
        trafilatura_meta_playwright = trafilatura.extract_metadata(
            playwright_bytes)
        parsed_html = BeautifulSoup(url_data["html"] or "", features="lxml")
        for tag in self.clean_tags:
            tags = parsed_html.find_all(
                tag) if parsed_html.find_all(tag) else []
            for t in tags:
                t.clear()
        crawler_ignore = parsed_html.find_all(
            name=None, attrs={"data-crawler": "ignore"})
        for t in crawler_ignore:
            t.clear()
        html = parsed_html.prettify()
        text_html2text = WebTools.html2Text(html)
        if trafilatura_meta_playwright:
            trafilatura_meta = trafilatura_meta_playwright.as_dict()
        else:
            trafilatura_meta = {}

        response.meta["data"] = {
            # legacy, do we need these fields?
            "content": url_data["html"],
            "parsed_html": parsed_html,
            "text": text_html2text,
            "trafilatura_text": trafilatura_text,
            "trafilatura_meta": trafilatura_meta,
        }

        selector_playwright = scrapy.Selector(text=playwright_text)
        robot_meta_tags: list[str] = selector_playwright.xpath(
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

        base_loader = BaseItemLoader(selector=selector_playwright)
        base_loader.add_value("sourceId", self.getId(response))
        base_loader.add_value("hash", self.getHash(response))
        base_loader.add_value("thumbnail", self.getLRMI(
            "thumbnailUrl", response=response))
        base_loader.add_xpath(
            "thumbnail", '//meta[@property="og:image"]/@content')
        base_loader.add_xpath(
            "lastModified", '//meta[@name="last-modified"]/@content')

        # Creating the nested ItemLoaders according to our items.py data model
        lom_loader = LomBaseItemloader()
        general_loader = LomGeneralItemloader(response=response)
        technical_loader = LomTechnicalItemLoader(selector=selector_playwright)
        educational_loader = LomEducationalItemLoader()
        classification_loader = LomClassificationItemLoader()
        valuespace_loader = ValuespaceItemLoader()
        license_loader = LicenseItemLoader(selector=selector_playwright)
        permissions_loader = self.getPermissions(response)
        response_loader = ResponseItemLoader()
        kidra_loader = KIdraItemLoader()

        # ToDo: rework LRMI JSON-LD extraction
        #  - so it can handle websites when there are several JSON-LD containers within a single DOM
        # ToDo: try to grab as many OpenGraph metadata properties as possible (for reference, see:
        # https://ogp.me)

        # general_loader.add_xpath("title", '//meta[@property="og:title"]/@content')
        general_loader.add_xpath("title", '//title/text()')
        # HTML language and locale properties haven proven to be pretty inconsistent, but they might
        # be useful as fallback values.
        # ToDo: websites might return languagecodes as 4-char values (e.g. "de-DE") instead of the
        # 2-char value "de"
        # -> we will have to detect/clean up languageCodes to edu-sharing's expected 2-char format
        general_loader.add_value("language", self.getLRMI(
            "inLanguage", response=response))
        general_loader.add_xpath("language", "//html/@lang")
        general_loader.add_xpath(
            "language", '//meta[@property="og:locale"]/@content')
        general_loader.add_value("description", self.getLRMI(
            "description", "about", response=response))
        general_loader.add_value(
            "keyword", self.getLRMI("keywords", response=response))
        
        if self.ai_enabled:
            excerpt = text_html2text[:4000]
            # todo: turn this "inside out" - don't pass the loaders,
            # but return structured data and load it here
            self.query_llm(excerpt, general_loader, base_loader, valuespace_loader)

            kidra_loader.add_value(
                "curriculum", self.zapi_get_curriculum(excerpt))
            classification, reading_time = self.zapi_get_statistics(excerpt)
            kidra_loader.add_value("text_difficulty", classification)
            kidra_loader.add_value("text_reading_time", reading_time)
            kidra_loader.add_value(
                "kidraDisciplines", self.zapi_get_disciplines(excerpt))
            # ToDo: map/replace the previously set 'language'-value by AI suggestions from Z-API?
            base_loader.add_value("kidra_raw", kidra_loader.load_item())
        else:
            if trafilatura_description := trafilatura_meta.get("description"):
                general_loader.add_value(
                    "description", trafilatura_description)
            if trafilatura_title := trafilatura_meta.get("title"):
                general_loader.replace_value("title", trafilatura_title)

        lom_loader.add_value("general", general_loader.load_item())

        technical_loader.add_value(
            "format", self.getLRMI("fileFormat", response=response))
        # ToDo: do we really want to hard-code this?
        technical_loader.replace_value("format", "text/html")
        technical_loader.add_value("size", self.getLRMI(
            "ContentSize", response=response))
        technical_loader.add_value(
            "location", self.getLRMI("url", response=response))
        technical_loader.add_value("location", response.url)
        technical_loader.replace_value("size", len(response.body))
        # ToDo: 'size' should probably use the length of our playwright response, not scrapy's
        # response.body
        technical_loader.add_xpath(
            "location", '//meta[@property="og:url"]/@content')

        self.get_lifecycle_author(
            lom_loader=lom_loader, selector=selector_playwright, response=response)

        self.get_lifecycle_publisher(
            lom_loader=lom_loader, selector=selector_playwright, response=response)

        # we might be able to extract author/publisher information from typical <meta> or <head>
        # fields in the DOM
        lom_loader.add_value("educational", educational_loader.load_item())
        lom_loader.add_value(
            "classification", classification_loader.load_item())
        lom_loader.add_value("technical", technical_loader.load_item())
        # after LomBaseItem is filled with nested metadata, we build the LomBaseItem and add it to
        # our BaseItem:
        base_loader.add_value("lom", lom_loader.load_item())

        # Todo: does this deal with multiple authors correctly?
        license_loader.add_xpath("author", '//meta[@name="author"]/@content')
        # trafilatura offers a license detection feature as part of its "extract_metadata()"-method

        if trafilatura_license_detected := trafilatura_meta.get("license"):
            license_mapper = LicenseMapper()
            license_url_mapped = license_mapper.get_license_url(
                license_string=trafilatura_license_detected
            )
            # ToDo: this is a really risky assignment! Validation of trafilatura's license detection
            #  will be necessary! (this is a metadata field that needs to be confirmed by a human!)
            license_loader.add_value("url", license_url_mapped)

        # lrmi_intended_end_user_role = self.getLRMI("audience.educationalRole", response=response)
        # if lrmi_intended_end_user_role:
        #     valuespace_loader.add_value("intendedEndUserRole", lrmi_intended_end_user_role)
        # ToDo: rework
        # # attention: serlo URLs will break the getLRMI() Method because JSONBase cannot extract
        # the JSON-LD properly
        # # ToDo: maybe use the 'jmespath' Python package to retrieve this value more reliably
        valuespace_loader.add_value("learningResourceType", self.getLRMI(
            "learningResourceType", response=response))

        # loading all nested ItemLoaders into our BaseItemLoader:
        base_loader.add_value("license", license_loader.load_item())
        base_loader.add_value("valuespaces", valuespace_loader.load_item())
        base_loader.add_value("permissions", permissions_loader.load_item())
        base_loader.add_value("response", response_loader.load_item())

        if self.results_dict:
            title = self.results_dict['title']
            description = self.results_dict['description']
            if len(self.results_dict['disciplines']) != 0:
                disciplines = self.results_dict['disciplines']
                base_loader.load_item()['valuespaces']['discipline'] = disciplines
            educational_context = self.results_dict['educational_context']
            intendedEndUserRole = self.results_dict['intendedEndUserRole']
            keywords = self.results_dict['keywords']
            license = self.results_dict['license']
            new_lrt = self.results_dict['new_lrt']
            curriculum = self.results_dict['curriculum']
            if len(self.results_dict['text_difficulty']) != 0:
                text_difficulty = self.results_dict['text_difficulty']
                base_loader.load_item()[
                    'kidra_raw']['text_difficulty'] = text_difficulty
            if len(self.results_dict['text_reading_time']) != 0:
                text_reading_time = self.results_dict['text_reading_time']
                base_loader.load_item()[
                    'kidra_raw']['text_reading_time'] = text_reading_time

            # TODO: this looks wrong
            base_loader.load_item()['lom']['general']['title'] = title
            base_loader.load_item()['lom']['general']['description'] = description
            base_loader.load_item()['lom']['general']['keyword'] = keywords
            base_loader.load_item()['valuespaces']['new_lrt'] = new_lrt
            base_loader.load_item()[
                'valuespaces']['educationalContext'] = educational_context
            base_loader.load_item()[
                'valuespaces']['intendedEndUserRole'] = intendedEndUserRole
            base_loader.load_item()['license'] = license
            # base_loader.load_item()['valuespaces']['curriculum'] = curriculum
            base_loader.load_item()['kidra_raw']['curriculum'] = curriculum

        log.info("New URL processed:------------------------------------------")
        log.info(base_loader.load_item())
        log.info("------------------------------------------------------------")

        yield base_loader.load_item()

    def get_lifecycle_publisher(self, lom_loader: LomBaseItemloader, selector: scrapy.Selector,
                                response: Response):
        meta_publisher = selector.xpath(
            '//meta[@name="publisher"]/@content').get()
        if meta_publisher:
            lifecycle_publisher_loader = LomLifecycleItemloader()
            lifecycle_publisher_loader.add_value("role", "publisher")
            lifecycle_publisher_loader.add_value(
                "organization", meta_publisher)
            self.get_lifecycle_date(
                lifecycle_loader=lifecycle_publisher_loader, selector=selector, response=response)

            lom_loader.add_value(
                "lifecycle", lifecycle_publisher_loader.load_item())

    def get_lifecycle_author(self, lom_loader: LomBaseItemloader, selector: scrapy.Selector,
                             response: Response):
        meta_author = selector.xpath('//meta[@name="author"]/@content').get()
        if meta_author:
            lifecycle_author_loader = LomLifecycleItemloader()
            lifecycle_author_loader.add_value("role", "author")
            # author strings could be one or several names or organizations.
            # The license loader expects a 'firstName'.
            lifecycle_author_loader.add_value("firstName", meta_author)
            # ToDo: (optional) try determining if names need to be sorted into
            # 'firstName', 'lastName' or 'organization'-field-values
            # ToDo: shoving the whole string into 'firstName' is a hacky approach that will cause
            # organizations to appear as persons within the "lifecycle"-metadata. fine-tune this
            # approach later.
            self.get_lifecycle_date(
                lifecycle_loader=lifecycle_author_loader, selector=selector, response=response)

            lom_loader.add_value(
                "lifecycle", lifecycle_author_loader.load_item())

    @staticmethod
    def get_lifecycle_date(lifecycle_loader: LomLifecycleItemloader, selector: scrapy.Selector,
                           response: Response):
        if "date" in response.meta["data"]["trafilatura_meta"]:
            # trafilatura's metadata extraction scans for dates within
            # <meta name="date" content"..."> Elements
            date = selector.xpath('//meta[@name="date"]/@content').get()
            date_trafilatura: str = response.meta["data"]["trafilatura_meta"]["date"]
            if date_trafilatura:
                lifecycle_loader.add_value("date", date_trafilatura)
            elif date:
                lifecycle_loader.add_value("date", date)

    def zapi_get_curriculum(self, text: str) -> list[str]:
        """ Determines the curriculum topic (Lehrplanthema) using the z-API. """
        log.info("zapi_get_curriculum called")

        data = zapi.models.TopicAssistantKeywordsData(text=text)
        try:
            result = topics_flat_topics_flat_post.sync(client=self.zapi_client, body=data)
        except (zapi.errors.UnexpectedStatus, httpx.TimeoutException):
            log.error("zapi_get_curriculum: Failed to get curriculum topics from z-API.", exc_info=True)
            return []

        assert isinstance(result, zapi.models.TopicAssistantKeywordsResult)
        log.info("zapi_get_curriculum result: %s", result)

        n_topics = 3
        if result.topics:
            topics = result.topics[:n_topics]
            topic_names = [topic.uri for topic in topics]
            return topic_names
        
        return []

    def zapi_get_statistics(self, text: str) -> tuple[str, float]:
        """ Queries the z-API to get the text difficulty and reading time. """

        log.info("zapi_get_statistics called",)
        data = zapi.models.InputData(
            text=text, reading_speed=200, generate_embeddings=False)
        try:
            result = text_stats_analyze_text_post.sync(client=self.zapi_client, body=data)
        except (zapi.errors.UnexpectedStatus, httpx.TimeoutException):
            log.error("zapi_get_statistics: Failed to get text statistics from z-API.", exc_info=True)
            return "", 0.0
        log.info("zapi_get_statistics result: %s", result)
        
        return result.classification, round(result.reading_time, 2)  # type: ignore

    def zapi_get_disciplines(self, text: str) -> list[str]:
        """ Gets the disciplines for a given text using the z-API. """

        log.info("zapi_get_disciplines called")
        data = zapi.models.DisciplinesData(text=text)
        try:
            result = predict_subjects_kidra_predict_subjects_post.sync(client=self.zapi_client, body=data)
        except (zapi.errors.UnexpectedStatus, httpx.TimeoutException):
            log.error("zapi_get_disciplines: Failed to get disciplines from z-API.", exc_info=True)
            return []
        log.info("zapi_get_disciplines result: %s", result)

        min_score = 0.3
        uri_discipline = 'http://w3id.org/openeduhub/vocabs/discipline/'
        discipline_names = [
            uri_discipline + d.id for d in result.disciplines if d.score > min_score  # type: ignore
        ]

        return discipline_names

    def query_llm(self, excerpt: str, general_loader: LomGeneralItemloader,
                  base_loader: BaseItemLoader, valuespace_loader: ValuespaceItemLoader):
        """ Performs the LLM queries for the given text, and fills the
            corresponding ItemLoaders. """
        
        log.info("query_llm called")

        prompt = self.ALL_IN_ONE_PROMPT % ({'text': excerpt})
        result = self.call_llm_inner(prompt)

        # log prompt and response
        ai_prompt_itemloader = AiPromptItemLoader()
        ai_prompt_itemloader.add_value("ai_prompt", prompt)
        ai_prompt_itemloader.add_value("ai_response_raw", result)
        ai_prompt_itemloader.add_value("ai_response", result)
        base_loader.add_value(
            "ai_prompts", ai_prompt_itemloader.load_item())

        log.info("AI response: %r", result)
        if result is None:
            log.error("Failed to get response from AI service.")
            return

        # try to parse the result
        try:
            # strip everything up to the first '{' character and after the last '}'
            result = result[result.find('{'):result.rfind('}') + 1]
            result_dict = json.loads(result)
        except json.JSONDecodeError:
            log.error("Failed to parse JSON response from AI service.", exc_info=True)
            return
        
        log.info("Structured AI response: %s", result_dict)

        description = result_dict.get("description")
        keywords = result_dict.get("keywords")
        disciplines = result_dict.get("discipline")
        educational_context = result_dict.get("educationalContext")
        intended_end_user_role = result_dict.get("intendedEndUserRole")
        new_lrt = result_dict.get("new_lrt")

        log.info("Adding description: %s", description)
        log.info("Adding keywords: %s", keywords)
        general_loader.add_value("description", description)
        general_loader.add_value("keyword", keywords)
        # general_loader.add_value("keyword", ['apfel', 'birne'])
        # general_loader.add_value("keyword", ['kirsche'])

        def process_valuespaces(valuespace_name: str, values: list[str]):
            log.info("process_valuespaces(%r, %r)", valuespace_name, values)
            for value in values:
                parsed = self.valuespaces.findInText(valuespace_name, value)
                log.info("  %r -> %r", value, parsed)
                valuespace_loader.add_value(valuespace_name, parsed)

        process_valuespaces("discipline", disciplines)
        process_valuespaces("educationalContext", educational_context)
        process_valuespaces("intendedEndUserRole", intended_end_user_role)
        process_valuespaces("new_lrt", new_lrt)


    def call_llm_inner(self, prompt: str) -> Optional[str]:
        if self.llm_client:
            chat_completion = self.llm_client.chat.completions.create(
                messages=[{"role": "system", "content": "You are a helpful assistant"}, {
                    "role": "user", "content": prompt}],
                model=self.llm_model
            )
            log.info("LLM API response: %s", chat_completion)
            return chat_completion.choices[0].message.content or ""

        # TODO: add error checking
        api_result = zapi.api.ai_text_prompts.prompt.sync(
            client=self.zapi_client, body=prompt)
        assert isinstance(api_result, zapi.models.TextPromptEntity)
        if not api_result.responses:
            log.error(
                "No valid response from AI service for prompt: %s", prompt)
            return None
        return api_result.responses[0].strip()


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
