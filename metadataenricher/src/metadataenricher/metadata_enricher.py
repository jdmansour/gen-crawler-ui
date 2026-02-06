
import datetime
import json
import logging
from typing import Optional

import html2text
import httpx
import openai
import scrapy
import trafilatura  # type: ignore
from . import zapi
from .zapi import api
from .zapi.api import ai_text_prompts
from .zapi.api.ai_text_prompts import prompt
from .zapi import errors
from .zapi import models
from bs4 import BeautifulSoup
from valuespace_converter.valuespaces import Valuespaces
from .zapi.api.kidra import (predict_subjects_kidra_predict_subjects_post,
                            text_stats_analyze_text_post,
                            topics_flat_topics_flat_post)

from . import env
from .items import (AiPromptItemLoader, BaseItemLoader, KIdraItemLoader,
                     LicenseItemLoader, LomBaseItemloader,
                     LomClassificationItemLoader, LomEducationalItemLoader,
                     LomGeneralItemloader, LomLifecycleItemloader,
                     LomTechnicalItemLoader, PermissionItemLoader,
                     ResponseItemLoader, ValuespaceItemLoader)
from .util.license_mapper import LicenseMapper
from .web_tools import get_url_data

log = logging.getLogger(__name__)

class AuthenticationError(Exception):
    pass


class MetadataEnricher:
    zapi_client: zapi.AuthenticatedClient
    llm_client: Optional[openai.OpenAI] = None
    use_llm_api: bool = False
    llm_model: str = ""

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
new_lrt: Welche Materialart im schulischen Kontext stellt die Quelle dar? (Webseite, Artikel und Einzelpublikation, Bild, Video, Anleitung, Lexikon, Quiz, Wiki, Schülerarbeit, ...)
intendedEndUserRole: Für welche Zielgruppen eignet sich das Material? (Lerner/in, Lehrer/in, Eltern, Autor/in, ...)

Antworte im JSON-Format, und gebe keinen weiteren Text aus:
{
  "description": "Deine Beschreibung der Quelle",
  "keywords": ["Thema1", "Thema2"],
  "discipline": ["Geographie"],
  "educationalContext" ["Primarstufe"],
  "new_lrt": ["Artikel"],
  "intendedEndUserRole": ["Lehrer/in", "Lerner/in"]
}

Hier folgt der Text:
%(text)s
"""

    def __init__(self, ai_enabled: bool):
        self.is_setup = False
        self.ai_enabled = ai_enabled
        self.valuespaces = Valuespaces()
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



    def setup(self, settings):
        self.is_setup = True
        self.settings = settings

        self.use_llm_api = settings.get('GENERIC_CRAWLER_USE_LLM_API', False)
        log.info("GENERIC_CRAWLER_USE_LLM_API: %r", self.use_llm_api)
        if not self.use_llm_api:
            return

        api_key = settings.get('GENERIC_CRAWLER_LLM_API_KEY', '')
        if not api_key:
            raise RuntimeError(
                "No API key set for LLM API. Please set GENERIC_CRAWLER_LLM_API_KEY.")

        base_url = settings.get('GENERIC_CRAWLER_LLM_API_BASE_URL', '')
        if not base_url:
            raise RuntimeError(
                "No base URL set for LLM API. Please set GENERIC_CRAWLER_LLM_API_BASE_URL.")

        self.llm_model = settings.get('GENERIC_CRAWLER_LLM_MODEL', '')
        if not self.llm_model:
            raise RuntimeError(
                "No model set for LLM API. Please set GENERIC_CRAWLER_LLM_MODEL.")
        
        log.info("Using LLM API with the following settings:")
        log.info("GENERIC_CRAWLER_LLM_API_KEY: <set>")
        log.info("GENERIC_CRAWLER_LLM_API_BASE_URL: %r", base_url)
        log.info("GENERIC_CRAWLER_LLM_MODEL: %r", self.llm_model)
        self.llm_client = openai.OpenAI(api_key=api_key, base_url=base_url)

    async def parse_page(self, response_url: str):
        url_data = await get_url_data(response_url)
        if not url_data:
            log.warning("Playwright failed to fetch data for %s", response_url)
            return
        log.info("Response from get_url_data:")
        for key, val in url_data.items():
            log.info("%s: %r", key, str(val)[:100])

        # ToDo: validate "trafilatura"-fulltext-extraction from playwright
        # (compared to the html2text approach)
        # HTML extracted from the browser view
        playwright_html: str = url_data["html"] or ""
        # Main text extracted from browser view
        trafilatura_text: str = url_data["text"] or ""
        log.info("trafilatura_text: %s", str(trafilatura_text)[:100])

        text_html2text = self.manual_cleanup_text(playwright_html)
        log.info("Cleaned up text via html2text: %s", text_html2text[:100])

        if trafilatura_meta_playwright := trafilatura.extract_metadata(playwright_html.encode()):
            trafilatura_meta = trafilatura_meta_playwright.as_dict()
        else:
            trafilatura_meta = {}
        log.info("trafilatura_meta: %s", trafilatura_meta)

        selector_playwright = scrapy.Selector(text=playwright_html)

        # extract LRMI objects from the response
        lrmi_path = '//script[@type="application/ld+json"]//text()'
        lrmi_objects = []
        for l in selector_playwright.xpath(lrmi_path).getall():
            try:
                obj = json.loads(l)
            except json.JSONDecodeError:
                log.warning("Failed to parse JSON-LD object: %s", l)
                continue

            log.debug("JSON-LD object: %s", type(obj))
            if isinstance(obj, list):
                for o in obj:
                    if isinstance(o, dict):
                        lrmi_objects.append(o)
            elif isinstance(obj, dict):
                lrmi_objects.append(obj)
            else:
                log.warning("Unexpected JSON-LD object: %s", l)
                continue

        def getLRMI(field: str):
            for obj in lrmi_objects:
                value = obj.get(field)
                if value:
                    log.info("JSON-LD found: %s:%s", field, value)
                    return value
            log.info("JSON-LD not found: %s", field)

        base_loader = BaseItemLoader(selector=selector_playwright)
        source_id = self.get_id(response_url=response_url)
        source_hash = self.get_hash()
        base_loader.add_value("sourceId", source_id)
        base_loader.add_value("hash", source_hash)
        base_loader.add_value("thumbnail", getLRMI("thumbnailUrl"))
        base_loader.add_xpath("thumbnail", '//meta[@property="og:image"]/@content')
        base_loader.add_xpath("lastModified", '//meta[@name="last-modified"]/@content')

        # Creating the nested ItemLoaders according to our items.py data model
        lom_loader = LomBaseItemloader()
        general_loader = LomGeneralItemloader(selector=selector_playwright)
        technical_loader = LomTechnicalItemLoader(selector=selector_playwright)
        educational_loader = LomEducationalItemLoader()
        classification_loader = LomClassificationItemLoader()
        valuespace_loader = ValuespaceItemLoader()
        license_loader = LicenseItemLoader(selector=selector_playwright)
        permissions_loader = PermissionItemLoader(selector=selector_playwright)
        # default all materials to public, needs to be changed depending on the spider!
        permissions_loader.add_value("public", self.settings.get("DEFAULT_PUBLIC_STATE"))
        response_loader = ResponseItemLoader()
        kidra_loader = KIdraItemLoader()

        # ToDo: rework LRMI JSON-LD extraction
        #  - so it can handle websites when there are several JSON-LD containers within a single DOM
        # ToDo: try to grab as many OpenGraph metadata properties as possible (for reference, see:
        # https://ogp.me)

        general_loader.add_xpath("title", '//meta[@property="og:title"]/@content')
        general_loader.add_xpath("title", '//title/text()')
        # HTML language and locale properties haven proven to be pretty inconsistent, but they might
        # be useful as fallback values.
        # ToDo: websites might return languagecodes as 4-char values (e.g. "de-DE") instead of the
        # 2-char value "de"
        # -> we will have to detect/clean up languageCodes to edu-sharing's expected 2-char format
        general_loader.add_value("language", getLRMI("inLanguage"))
        general_loader.add_xpath("language", "//html/@lang")
        general_loader.add_xpath("language", '//meta[@property="og:locale"]/@content')
        general_loader.add_value("description", getLRMI("description"))
        general_loader.add_value("description", getLRMI("about"))
        general_loader.add_value("keyword", getLRMI("keywords"))
        
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

        technical_loader.add_value("format", getLRMI("fileFormat"))
        # ToDo: do we really want to hard-code this?
        technical_loader.replace_value("format", "text/html")
        technical_loader.add_value("size", getLRMI("ContentSize"))
        technical_loader.add_value("location", getLRMI("url"))
        technical_loader.add_value("location", response_url)
        technical_loader.replace_value("size", len(playwright_html))
        technical_loader.add_xpath(
            "location", '//meta[@property="og:url"]/@content')

        date: Optional[str] = None
        if trafilatura_meta:
            date = trafilatura_meta.get('date')
        if not date:
            date = selector_playwright.xpath('//meta[@name="date"]/@content').get()

        self.get_lifecycle_author(
            lom_loader=lom_loader, selector=selector_playwright, date=date)

        self.get_lifecycle_publisher(
            lom_loader=lom_loader, selector=selector_playwright, date=date)

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

        # lrmi_intended_end_user_role = getLRMI("audience.educationalRole")
        # if lrmi_intended_end_user_role:
        #     valuespace_loader.add_value("intendedEndUserRole", lrmi_intended_end_user_role)
        # ToDo: rework
        # # attention: serlo URLs will break the getLRMI() Method because JSONBase cannot extract
        # the JSON-LD properly
        # # ToDo: maybe use the 'jmespath' Python package to retrieve this value more reliably
        valuespace_loader.add_value("learningResourceType", getLRMI("learningResourceType"))

        # loading all nested ItemLoaders into our BaseItemLoader:
        base_loader.add_value("license", license_loader.load_item())
        base_loader.add_value("valuespaces", valuespace_loader.load_item())
        base_loader.add_value("permissions", permissions_loader.load_item())
        base_loader.add_value("response", response_loader.load_item())

        return base_loader.load_item()
    
    def manual_cleanup_text(self, html_source: str) -> str:
        parsed_html = BeautifulSoup(html_source, features="lxml")
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
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        return h.handle(html)

    def get_id(self, response_url: str) -> str:
        """ Return a stable identifier (URI) of the crawled item """
        # TODO: use something more clever
        return response_url

    def get_hash(self) -> str:
        """ Return a stable hash to detect content changes (for future crawls). """
        # TODO: this is obviously not stable
        return f"{datetime.datetime.now().isoformat()}"
    

    def get_lifecycle_publisher(self, lom_loader: LomBaseItemloader, selector: scrapy.Selector,
                                date: Optional[str]):
        meta_publisher = selector.xpath(
            '//meta[@name="publisher"]/@content').get()
        if meta_publisher:
            lifecycle_publisher_loader = LomLifecycleItemloader()
            lifecycle_publisher_loader.add_value("role", "publisher")
            lifecycle_publisher_loader.add_value(
                "organization", meta_publisher)
            lifecycle_publisher_loader.add_value("date", date)

            lom_loader.add_value(
                "lifecycle", lifecycle_publisher_loader.load_item())

    def get_lifecycle_author(self, lom_loader: LomBaseItemloader, selector: scrapy.Selector,
                             date: Optional[str]):
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
            lifecycle_author_loader.add_value("date", date)
            lom_loader.add_value(
                "lifecycle", lifecycle_author_loader.load_item())

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
        log.info("zapi_get_curriculum result:")
        filtered = [t for t in result.topics or [] if t.label]
        topics = sorted(filtered, key=lambda t: t.weight, reverse=True)
        # TODO: sort by weight
        max_print = 10
        for topic in topics[:max_print]:
            log.info("Topic: %r", topic)
            # log.info("Topic: weight=%f label=%r match=%r", topic.weight, topic.label, topic.match)
        if len(topics) > max_print:
            log.info("... %d more topics", len(topics) - max_print)

        n_topics = 3
        topic_uris = [topic.uri for topic in topics[:n_topics]]
        return topic_uris

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
        # ai_prompt_itemloader.add_value("ai_response_raw", result)
        ai_prompt_itemloader.add_value("ai_response", result)
        base_loader.add_value(
            "ai_prompts", ai_prompt_itemloader.load_item())

        # log.info("AI response: %r", result)
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
            log.info("AI response: %r", result)
            return

        log.info("Structured AI response: %s", result_dict)

        description = result_dict.get("description")

        def get_list(result_dict: dict, key: str) -> list[str]:
            value = result_dict.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, str):
                return [value]

            log.warning(
                "Invalid LLM response. Expected string or list for key %r, got %r (type %r)",
                key, value, type(value))
            return []

        keywords = get_list(result_dict, "keywords")
        disciplines = get_list(result_dict, "discipline")
        educational_context = get_list(result_dict, "educationalContext")
        intended_end_user_role = get_list(result_dict, "intendedEndUserRole")
        new_lrt = get_list(result_dict, "new_lrt")

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
            try:
                chat_completion = self.llm_client.chat.completions.create(
                    messages=[{"role": "system", "content": "Du bist ein hilfreicher KI-Assistent der Informationen über Bildungsmaterialien herausfinden soll."}, {
                        "role": "user", "content": prompt}],
                    model=self.llm_model
                )
            except openai.APITimeoutError:
                log.error("LLM API request timed out.")
                return None
            except openai.AuthenticationError as e:
                raise AuthenticationError("LLM API authentication failed.") from e
            # log.info("LLM API response: %s", chat_completion)
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
    

