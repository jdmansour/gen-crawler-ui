# -*- coding: utf-8 -*-

from __future__ import annotations

import base64
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import datetime
import logging
import pprint
import re
import time
from abc import ABCMeta
from asyncio import Future
from io import BytesIO
from typing import BinaryIO, TextIO, Optional

import PIL
import dateparser
import dateutil.parser
import isodate
import scrapy
import scrapy.crawler
import twisted.internet.error
from PIL import Image
from async_lru import alru_cache
from itemadapter import ItemAdapter
from scrapy import settings
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonItemExporter
from scrapy.http.request import NO_CALLBACK
from scrapy.utils.defer import maybe_deferred_to_future
from scrapy.utils.project import get_project_settings
from twisted.internet.defer import Deferred

from scraper import env
from scraper.constants import *
from scraper.es_connector import EduSharing
from scraper.items import BaseItem
from scraper.spiders.generic_spider import GenericSpider
from scraper.util.edu_sharing_source_template_helper import EduSharingSourceTemplateHelper
from scraper.util.language_mapper import LanguageMapper
from metadataenricher.web_tools import get_url_data
from valuespace_converter.valuespaces import Valuespaces

log = logging.getLogger(__name__)


class BasicPipeline(metaclass=ABCMeta):
    def process_item(self, item: scrapy.Item, spider: scrapy.Spider) -> Optional[scrapy.Item]:
        """
        This method is called for every item pipeline component.

        `item` is an :ref:`item object <item-types>`, see
        :ref:`supporting-item-types`.

        :meth:`process_item` must either: return an :ref:`item object <item-types>`,
        return a :class:`~twisted.internet.defer.Deferred` or raise a
        :exc:`~scrapy.exceptions.DropItem` exception.

        Dropped items are no longer processed by further pipeline components.

        :param item: the scraped item
        :type item: :ref:`item object <item-types>`

        :param spider: the spider which scraped the item
        :type spider: :class:`~scrapy.spiders.Spider` object
        """
        return item


class LOMFillupPipeline(BasicPipeline):
    """
    fillup missing props by "guessing" or loading them if possible
    """

    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        if "fulltext" not in item and "text" in item["response"]:
            item["fulltext"] = item["response"]["text"]
        return raw_item


class FilterSparsePipeline(BasicPipeline):
    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        try:
            if "title" not in item["lom"]["general"]:
                raise DropItem(
                    "Entry {} has no title location".format(item["sourceId"])
                )
        except KeyError:
            raise DropItem(f'Item {item} has no lom.technical.location')
        try:
            if "location" not in item["lom"]["technical"] and not "binary" in item:
                raise DropItem(
                    "Entry {} has no technical location or binary data".format(item["lom"]["general"]["title"])
                )
        except KeyError:
            raise DropItem(f'Item {item} has no lom.technical.location')
        # pass through explicit uuid elements
        if "uuid" in item:
            return raw_item
        try:
            # if it contains keywords, it's valid
            if _ := item["lom"]["general"]["keyword"]:
                return raw_item
        except KeyError:
            pass
        try:
            # if it has a description, it's valid
            if _ := item["lom"]["general"]["description"]:
                return raw_item
        except KeyError:
            pass
        try:
            # if it the valuespaces.learningResourceType is set, it is valid
            if _ := item["valuespaces"]["learningResourceType"]:
                return raw_item
        except KeyError:
            pass
        # if none of the above matches drop the item

        try:
            raise DropItem(
                "Entry "
                + item["lom"]["general"]["title"]
                + " has neither keywords nor description"
            )
        except KeyError:
            raise DropItem(f'Item {item} was dropped for not providing enough metadata')


class NormLanguagePipeline(BasicPipeline):
    """Normalize raw or ambiguous language strings to 2-letter-language-codes (ISO 639-1)."""
    def process_item(self, item, spider):
        item_adapter = ItemAdapter(item)
        try:
            lom_general_languages: list[str] = item_adapter["lom"]["general"]["language"]
            if lom_general_languages:
                language_mapper = LanguageMapper(languages=lom_general_languages)
                normalized_language_codes: list[str] | None = language_mapper.normalize_list_of_language_strings()
                if normalized_language_codes:
                    item_adapter["lom"]["general"]["language"] = normalized_language_codes
        except KeyError:
            # happens when the "language" field does not exist within lom.general
            pass
        try:
            lom_educational_languages: list[str] = item_adapter["lom"]["educational"]["language"]
            if lom_educational_languages:
                language_mapper = LanguageMapper(languages=lom_educational_languages)
                normalized_language_codes: list[str] | None = language_mapper.normalize_list_of_language_strings()
                if normalized_language_codes:
                    item_adapter["lom"]["general"]["language"] = normalized_language_codes
        except KeyError:
            # happens when the "language" field does not exist within lom.educational
            pass
        return item


class NormLicensePipeline(BasicPipeline):
    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        if "url" in item["license"] and not item["license"]["url"] in Constants.VALID_LICENSE_URLS:
            for key in Constants.LICENSE_MAPPINGS:
                if item["license"]["url"].startswith(key):
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS[key]
                    break
        if "internal" in item["license"] and (
                "url" not in item["license"]
                or item["license"]["url"] not in Constants.VALID_LICENSE_URLS
        ):
            for key in Constants.LICENSE_MAPPINGS_INTERNAL:
                if item["license"]["internal"].casefold() == key.casefold():
                    # use the first entry
                    item["license"]["url"] = Constants.LICENSE_MAPPINGS_INTERNAL[key][0]
                    break

        if "url" in item["license"] and "oer" not in item["license"]:
            match item["license"]["url"]:
                case Constants.LICENSE_CC_BY_20 | \
                     Constants.LICENSE_CC_BY_25 | \
                     Constants.LICENSE_CC_BY_30 | \
                     Constants.LICENSE_CC_BY_40 | \
                     Constants.LICENSE_CC_BY_SA_20 | \
                     Constants.LICENSE_CC_BY_SA_25 | \
                     Constants.LICENSE_CC_BY_SA_30 | \
                     Constants.LICENSE_CC_BY_SA_40 | \
                     Constants.LICENSE_CC_ZERO_10:
                    item["license"]["oer"] = OerType.ALL
                case _:
                    # ToDo: log default case if not too spammy
                    pass

        if "internal" in item["license"] and "oer" not in item["license"]:
            internal = item["license"]["internal"].lower()
            if "cc-by-sa" in internal or "cc-0" in internal or "pdm" in internal:
                item["license"]["oer"] = OerType.ALL
        if "expirationDate" in item["license"]:
            item["license"]["expirationDate"] = dateparser.parse(item["license"]["expirationDate"])
        if "lifecycle" in item["lom"]:
            for contribute in item["lom"]["lifecycle"]:
                if "date" in contribute:
                    contribute["date"] = dateparser.parse(contribute["date"])

        return raw_item


class ConvertTimePipeline(BasicPipeline):
    """
    convert typicalLearningTime into an integer representing seconds
    + convert duration into an integer
    """

    def process_item(self, raw_item, spider):
        # map lastModified
        item = ItemAdapter(raw_item)
        if "lastModified" in item:
            try:
                item["lastModified"] = float(item["lastModified"])
            except:
                try:
                    date = dateutil.parser.parse(item["lastModified"])
                    item["lastModified"] = int(date.timestamp())
                except:
                    log.warning(
                        "Unable to parse given lastModified date "
                        + item["lastModified"]
                    )
                    del item["lastModified"]

        if "typicalLearningTime" in item["lom"]["educational"]:
            t = item["lom"]["educational"]["typicalLearningTime"]
            mapped = None
            splitted = t.split(":")
            if len(splitted) == 3:
                mapped = (
                        int(splitted[0]) * 60 * 60
                        + int(splitted[1]) * 60
                        + int(splitted[2])
                )
            if mapped is None:
                log.warning(
                    "Unable to map given typicalLearningTime "
                    + t
                    + " to numeric value"
                )
            item["lom"]["educational"]["typicalLearningTime"] = mapped
        if "technical" in item["lom"]:
            if "duration" in item["lom"]["technical"]:
                raw_duration = item["lom"]["technical"]["duration"]
                duration = raw_duration.strip()
                if duration:
                    if len(duration.split(":")) == 3:
                        duration = isodate.parse_time(duration)
                        duration = duration.hour * 60 * 60 + duration.minute * 60 + duration.second
                    elif duration.startswith("PT"):
                        duration = int(isodate.parse_duration(duration).total_seconds())
                    else:
                        try:
                            duration = int(duration)
                        except:
                            duration = None
                            log.warning("duration {} could not be normalized to seconds".format(raw_duration))
                    item["lom"]["technical"]["duration"] = duration
        return raw_item


class ProcessValuespacePipeline(BasicPipeline):
    """
    generate de_DE / i18n strings for valuespace fields
    """

    def __init__(self):
        self.valuespaces = Valuespaces()

    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        json = item["valuespaces"]
        item["valuespaces_raw"] = dict(json)
        delete = []
        for key in json:
            # remap to new i18n layout
            mapped = []
            for entry in json[key]:
                _id = {}
                valuespace: list[dict] = self.valuespaces.data[key]
                found = False
                for v in valuespace:
                    labels = list(v["prefLabel"].values())
                    if "altLabel" in v:
                        # the Skohub update on 2024-04-19 generates altLabels as a list[str] per language ("de", "en)
                        # (for details, see: https://github.com/openeduhub/oeh-metadata-vocabs/pull/65)
                        alt_labels: list[list[str]] = list(v["altLabel"].values())
                        if alt_labels and isinstance(alt_labels, list):
                            for alt_label in alt_labels:
                                if alt_label and isinstance(alt_label, list):
                                    labels.extend(alt_label)
                                if alt_label and isinstance(alt_label, str):
                                    labels.append(alt_label)
                    labels = list(map(lambda x: x.casefold(), labels))
                    if v["id"].endswith(entry) or entry.casefold() in labels:
                        _id = v["id"]
                        found = True
                        break
                if found and len(list(filter(lambda x: x == _id, mapped))) == 0:
                    mapped.append(_id)
            if len(mapped):
                json[key] = mapped
            else:
                delete.append(key)
        for key in delete:
            del json[key]
        item["valuespaces"] = json
        return raw_item


class ProcessThumbnailPipeline(BasicPipeline):
    """
    generate thumbnails
    """

    @staticmethod
    def scale_image(img, max_size):
        w = float(img.width)
        h = float(img.height)
        while w * h > max_size:
            w *= 0.9
            h *= 0.9
        return img.resize((int(w), int(h)), Image.Resampling.LANCZOS).convert("RGB")

    async def process_item(self, raw_item, spider):
        """
        By default, the thumbnail-pipeline handles several cases:
        - if there is a URL-string inside the "BaseItem.thumbnail"-field:
        -- download image from URL; rescale it into different sizes (small/large);
        --- save the thumbnails as base64 within
        ---- "BaseItem.thumbnail.small", "BaseItem.thumbnail.large"
        --- (afterward delete the URL from "BaseItem.thumbnail")

        - if there is NO "BaseItem.thumbnail"-field:
        -- on-demand: use Playwright to take a screenshot, rescale and save (as above)
        """
        item = ItemAdapter(raw_item)
        response: scrapy.http.Response | None = None
        url: str | None = None
        settings_crawler = get_settings_for_crawler(spider)

        # if screenshot_bytes is provided (the crawler has already a binary representation of the image,
        # the pipeline will convert/scale the given image
        if "screenshot_bytes" in item:
            log.info("screenshot_bytes provided by crawler, using it to create thumbnail without additional HTTP request")
            # in case we are already using playwright in a spider, we can skip one additional HTTP Request by
            # accessing the (temporary available) "screenshot_bytes"-field
            img = Image.open(BytesIO(item["screenshot_bytes"]))
            self.create_thumbnails_from_image_bytes(img, item, settings_crawler)
            # The final BaseItem data model doesn't use screenshot_bytes.
            # Therefore, we delete it after we're done with processing it
            del item["screenshot_bytes"]
        elif "thumbnail" in item:
            log.info("Thumbnail URL provided by crawler, trying to download it: %s", item["thumbnail"])
            # a thumbnail (url) was provided within the item -> we will try to fetch it from the url
            url: str = item["thumbnail"]
            time_start: datetime = datetime.datetime.now()
            try:
                thumbnail_response: scrapy.http.Response = await self.download_thumbnail_url(url, spider)
                # we expect that some thumbnail URLs will be wrong, outdated or already offline, which is why we catch
                # the most common Exceptions while trying to dwonload the image.
            except twisted.internet.error.TCPTimedOutError:
                log.warning(f"Thumbnail download of URL {url} failed due to TCPTimedOutError. "
                            f"(You might see this error if the image is unavailable under that specific URL.) "
                            f"Falling back to website screenshot.")
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            except twisted.internet.error.DNSLookupError:
                log.warning(f"Thumbnail download of URL {url} failed due to DNSLookupError. "
                            f"(The webserver might be offline.) Falling back to website screenshot.")
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            time_end: datetime = datetime.datetime.now()
            log.debug(f"Loading thumbnail from {url} took {time_end - time_start} (incl. awaiting).")
            log.debug(f"Thumbnail-URL-Cache: {self.download_thumbnail_url.cache_info()} after trying to query {url} ")
            if thumbnail_response.status != 200:
                log.debug(f"Thumbnail-Pipeline received a unexpected response (status: {thumbnail_response.status}) "
                          f"from {url} (-> resolved URL: {thumbnail_response.url}")
                # fall back to website screenshot
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            else:
                # Some web-servers 'lie' in regard to their HTTP status, e.g., they forward to a 404 HTML page and still
                # respond with a '200' code.
                try:
                    # We need to do additional checks before accepting the response object as a valid candidate for the
                    # image transformation
                    _mimetype: bytes = thumbnail_response.headers["Content-Type"]
                    _mimetype: str = _mimetype.decode()
                    if _mimetype.startswith("image/"):
                        # we expect thumbnail URLs to be of MIME-Type 'image/...'
                        # see: https://www.iana.org/assignments/media-types/media-types.xhtml#image
                        response = thumbnail_response
                        # only set the response if thumbnail retrieval was successful!
                    elif _mimetype == "application/octet-stream":
                        # ToDo: special handling for 'application/octet-stream' necessary?
                        log.debug(f"Thumbnail URL of MIME-Type 'image/...' expected, "
                                 f"but received '{_mimetype}' instead. "
                                 f"(If thumbnail conversion throws unexpected errors further down the line, "
                                 f"the Thumbnail-Pipeline needs to be re-visited! URL: {url} )")
                        response = thumbnail_response
                    else:
                        log.warning(f"Thumbnail URL {url} does not seem to be an image! "
                                    f"Header contained Content-Type '{_mimetype}' instead. "
                                    f"(Falling back to screenshot)")
                        del item["thumbnail"]
                        return await self.process_item(raw_item, spider)
                except KeyError:
                    log.warning(f"Thumbnail URL response did not contain a Content-Type / MIME-Type! "
                                f"Thumbnail URL queried: {url} "
                                f"-> resolved URL: {thumbnail_response.url} "
                                f"(HTTP Status: {thumbnail_response.status}")
                    del item["thumbnail"]
                    return await self.process_item(raw_item, spider)
        elif (
                "location" in item["lom"]["technical"]
                and len(item["lom"]["technical"]["location"]) > 0
        ):
            log.info("No thumbnail URL provided by crawler, trying to use the location as thumbnail URL: %s", item["lom"]["technical"]["location"][0])
            playwright_websocket_endpoint: str | None = env.get("PLAYWRIGHT_CDP_ENDPOINT")
            if (playwright_websocket_endpoint):
                # we're using Playwright to take a website screenshot if:
                # - the spider explicitly defined Playwright in its 'custom_settings'-dict
                # - or: the thumbnail URL could not be downloaded (= fallback)

                # this edge-case is necessary for spiders that only need playwright to gather a screenshot,
                # but don't use playwright within the spider itself
                target_url: str = item["lom"]["technical"]["location"][0]
                playwright_dict = await get_url_data(url=target_url)
                screenshot_bytes = playwright_dict.get("screenshot_bytes")
                img = Image.open(BytesIO(screenshot_bytes))
                self.create_thumbnails_from_image_bytes(img, item, settings_crawler)

        if response is None:
            pass
        else:
            try:
                if response.headers["Content-Type"] == b"image/svg+xml":
                    if len(response.body) > settings_crawler.get("THUMBNAIL_MAX_SIZE"):
                        raise Exception(
                            "SVG images can't be converted, and the given image exceeds the maximum allowed size ("
                            + str(len(response.body))
                            + " > "
                            + str(settings_crawler.get("THUMBNAIL_MAX_SIZE"))
                            + ")"
                        )
                    item["thumbnail"] = {}
                    _mimetype: bytes = response.headers["Content-Type"]
                    if _mimetype and isinstance(_mimetype, bytes):
                        item["thumbnail"]["mimetype"] = _mimetype.decode()
                    elif _mimetype and isinstance(_mimetype, str):
                        item["thumbnail"]["mimetype"] = _mimetype
                    item["thumbnail"]["small"] = base64.b64encode(
                        response.body
                    ).decode()
                else:
                    img = Image.open(BytesIO(response.body))
                    self.create_thumbnails_from_image_bytes(img, item, settings_crawler)
            except PIL.UnidentifiedImageError:
                # this error can be observed when a website serves broken / malformed images
                if url:
                    log.warning(f"Thumbnail download of image file {url} failed: image file could not be identified "
                                f"(Image might be broken or corrupt). Falling back to website-screenshot.")
                del item["thumbnail"]
                return await self.process_item(raw_item, spider)
            except Exception as e:
                if url is not None:
                    log.warning(f"Could not read thumbnail at {url}: {str(e)} (falling back to screenshot)")
                    raise e
                if "thumbnail" in item:
                    del item["thumbnail"]
                    return await self.process_item(raw_item, spider)
                else:
                    # item['thumbnail']={}
                    raise DropItem(
                        "No thumbnail provided or resource was unavailable for fetching"
                    )
        return raw_item

    @alru_cache(maxsize=128)
    async def download_thumbnail_url(self, url: str, spider: scrapy.Spider):
        """
        Download a thumbnail URL and **caches** the result.

        The cache works similarly to Python's built-in `functools.lru_cache`-decorator and discards the
        least recently used items first.
        (see: https://github.com/aio-libs/async-lru)

        Typical use-case:
        Some webhosters serve generic placeholder images as their default thumbnail.
        By caching the response of such URLs, we can save a significant amount of time and traffic.

        :param spider: The spider process that collected the URL.
        :param url: URL of a thumbnail/image.
        :return: Response or None
        """
        try:
            request = scrapy.Request(url=url, callback=NO_CALLBACK, priority=1)
            # Thumbnail downloads will be executed with a slightly higher priority (default: 0), so there's less delay
            # between metadata processing and thumbnail retrieval steps in the pipelines
            response: Deferred | Future = await maybe_deferred_to_future(
                spider.crawler.engine.download(request)
            )
            return response
        except ValueError:
            log.debug(f"Thumbnail-Pipeline received an invalid URL: {url}")

    # override the project settings with the given ones from the current spider
    # see PR 56 for details

    def create_thumbnails_from_image_bytes(self, image: Image.Image, item, settings):
        small_buffer: BytesIO = BytesIO()
        large_buffer: BytesIO = BytesIO()
        if image.format == "PNG":
            # PNG images with image.mode == "RGBA" cannot be converted cleanly to JPEG,
            # which is why we're handling PNGs separately
            small_copy = image.copy()
            large_copy = image.copy()
            # Pillow modifies the image object in place -> remember to use the correct copy
            small_copy.thumbnail(size=(250, 250))
            large_copy.thumbnail(size=(800, 800))
            # ToDo:
            #  Rework settings.py thumbnail config to retrieve values as width & height instead of sum(int)
            small_copy.save(small_buffer, format="PNG")
            large_copy.save(large_buffer, format="PNG")
            item["thumbnail"] = {}
            item["thumbnail"]["mimetype"] = "image/png"
            item["thumbnail"]["small"] = base64.b64encode(large_buffer.getvalue()).decode()
            item["thumbnail"]["large"] = base64.b64encode(large_buffer.getvalue()).decode()
        else:
            self.scale_image(image, settings.get("THUMBNAIL_SMALL_SIZE")).save(
                small_buffer,
                "JPEG",
                mode="RGB",
                quality=settings.get("THUMBNAIL_SMALL_QUALITY"),
            )
            self.scale_image(image, settings.get("THUMBNAIL_LARGE_SIZE")).save(
                large_buffer,
                "JPEG",
                mode="RGB",
                quality=settings.get("THUMBNAIL_LARGE_QUALITY"),
            )
            item["thumbnail"] = {}
            item["thumbnail"]["mimetype"] = "image/jpeg"
            item["thumbnail"]["small"] = base64.b64encode(
                small_buffer.getvalue()
            ).decode()
            item["thumbnail"]["large"] = base64.b64encode(
                large_buffer.getvalue()
            ).decode()


def get_settings_for_crawler(spider) -> scrapy.settings.Settings:
    all_settings = get_project_settings()
    crawler_settings = settings.BaseSettings(getattr(spider, "custom_settings") or {}, 'spider')
    if type(crawler_settings) == dict:
        crawler_settings = settings.BaseSettings(crawler_settings, 'spider')
    for key in crawler_settings.keys():
        if (
                all_settings.get(key) and crawler_settings.getpriority(key) > all_settings.getpriority(key)
                or not all_settings.get(key)
        ):
            all_settings.set(key, crawler_settings.get(key), crawler_settings.getpriority(key))
    return all_settings


class EduSharingCheckPipeline(EduSharing, BasicPipeline):
    def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        if "hash" not in item:
            log.error(
                "The spider did not provide a hash on the base object. "
                "The hash is required to detect changes on an element. "
                "(You should use the last modified date or something similar, "
                "e.g. '<date_modified_str>v<crawler_version>')"
            )
            item["hash"] = time.time()

        # @TODO: May this can be done only once?
        if self.find_source(spider) is None:
            log.info("create new source " + spider.name)
            self.create_source(spider)

        db_item = self.find_item(item["sourceId"], spider)
        if db_item:
            if item["hash"] != db_item[1]:
                log.debug(f"hash has changed, continuing pipelines for item {item['sourceId']}")
            else:
                log.debug(f"hash unchanged, skipping item {item['sourceId']}")
                # self.update(item['sourceId'], spider)
                # for tests, we update everything for now
                # activate this later
                # raise DropItem()
        return raw_item


class EduSharingStorePipeline(EduSharing, BasicPipeline):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def open_spider(self, spider):
        logging.debug("Entering EduSharingStorePipeline...\n"
                      "Checking if 'crawler source template' ('Quellendatensatz-Template') should be used "
                      "(see: 'EDU_SHARING_SOURCE_TEMPLATE_ENABLED' .env setting)...")
        est_enabled: bool = env.get_bool("EDU_SHARING_SOURCE_TEMPLATE_ENABLED", allow_null=True, default=False)
        # defaults to False for backwards-compatibility.
        # (The EduSharingSourceTemplateHelper class is explicitly set to throw errors and abort a crawl if this setting
        # is enabled! Activate this setting on a per-crawler basis!)
        if est_enabled:
            # "Quellendatensatz-Templates" might not be available on every edu-sharing instance. This feature is only
            # active if explicitly set via the .env file. (This choice was made to avoid errors with
            # old or unsupported crawlers.)
            est_helper: EduSharingSourceTemplateHelper = EduSharingSourceTemplateHelper(crawler_name=spider.name)
            whitelisted_properties: dict | None = est_helper.get_whitelisted_metadata_properties()
            if whitelisted_properties:
                setattr(spider, "edu_sharing_source_template_whitelist", whitelisted_properties)
                logging.debug(f"Edu-sharing source template retrieval was successful. "
                              f"The following metadata properties will be whitelisted for all items:\n"
                              f"{whitelisted_properties}")
            else:
                logging.error(f"Edu-Sharing Source Template retrieval failed. "
                              f"(Does a 'Quellendatensatz' exist in the edu-sharing repository for this spider?)")
        else:
            log.debug(f"Edu-Sharing Source Template feature is NOT ENABLED. Continuing EduSharingStorePipeline...")

    async def process_item(self, raw_item, spider):
        item = ItemAdapter(raw_item)
        title = "<no title>"
        if "title" in item["lom"]["general"]:
            title = str(item["lom"]["general"]["title"])
        entryUUID = EduSharing.build_uuid(item["response"]["url"] if "url" in item["response"] else item["hash"])
        inserted = await self.insert_item(spider, entryUUID, item)
        log.info("item " + entryUUID + " inserted/updated")
        log.info("type(inserted): " + str(type(inserted)))
        log.info(">>>>> raw item:\n %s", P().pformat(raw_item))
        log.info(">>>>> processed item\n: %s", P().pformat(inserted))
        # todo: move this to a signal in the crawler?
        # todo: set the parent_id on the returned item?
        if isinstance(spider, GenericSpider):
            if spider.crawler_output_node is None:
                parent_id = inserted.get("parent", {}).get("id", None)
                spider.crawler_output_node = parent_id
                log.info(f"Set crawler_output_node for spider {spider.name} to {parent_id}")
                url = f"https://repository.staging.openeduhub.net/edu-sharing/components/workspace?root=MY_FILES&id={parent_id}&displayType=0"
                log.info(f"You can view the crawled items at: {url}")
        self.counter += 1
            

        # @TODO: We may need to handle Collections
        # if 'collection' in item:
        #    for collection in item['collection']:
        # if dbItem:
        #     entryUUID = dbItem[0]
        #     logging.info('Updating item ' + title + ' (' + entryUUID + ')')
        #     self.curr.execute("""UPDATE "references_metadata" SET last_seen = now(), last_updated = now(), hash = %s, data = %s WHERE source = %s AND source_id = %s""", (
        #         item['hash'], # hash
        #         json,
        #         spider.name,
        #         str(item['sourceId']),
        #     ))
        # else:
        #     entryUUID = self.buildUUID(item['response']['url'])
        #     if 'uuid' in item:
        #         entryUUID = item['uuid']
        #     logging.info('Creating item ' + title + ' (' + entryUUID + ')')
        #     if self.uuidExists(entryUUID):
        #         logging.warn('Possible duplicate detected for ' + entryUUID)
        #     else:
        #         self.curr.execute("""INSERT INTO "references" VALUES (%s,true,now())""", (
        #             entryUUID,
        #         ))
        #     self.curr.execute("""INSERT INTO "references_metadata" VALUES (%s,%s,%s,%s,now(),now(),%s)""", (
        #         spider.name, # source name
        #         str(item['sourceId']), # source item identifier
        #         entryUUID,
        #         item['hash'], # hash
        #         json,
        #     ))
        return raw_item


class P(pprint.PrettyPrinter):
    def __init__(self, indent=1, width=80, depth=None, stream=None, *, compact=True, sort_dicts=True, underscore_numbers=False):
        super().__init__(indent, width, depth, stream, compact=compact, sort_dicts=sort_dicts, underscore_numbers=underscore_numbers)

    def _format(self, object, *args, **kwargs):
        if isinstance(object, str):
            if len(object) > 40:
                object = object[:19] + '...' + object[-18:]
        return pprint.PrettyPrinter._format(self, object, *args, **kwargs)


class DummyPipeline(BasicPipeline):
    # Scrapy will print the item on log level DEBUG anyway

    # class Printer:
    #     def write(self, byte_str: bytes) -> None:
    #         logging.debug(byte_str.decode("utf-8"))

    # def open_spider(self, spider):
    #     self.exporter = JsonItemExporter(
    #         DummyOutPipeline.Printer(),
    #         fields_to_export=[
    #             "collection",
    #             "fulltext",
    #             "hash",
    #             "lastModified",
    #             "license",
    #             "lom",
    #             "origin",
    #             "permissions",
    #             "publisher",
    #             "ranking",
    #             # "response",
    #             "sourceId",
    #             # "thumbnail",
    #             "type",
    #             "uuid",
    #             "valuespaces",
    #         ],
    #         indent=2,
    #         encoding="utf-8",
    #     )
    #     self.exporter.start_exporting()

    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()

    def process_item(self, item, spider):
        log.info("DRY RUN scraped {}".format(item["response"]["url"]))
        # self.exporter.export_item(item)
        return item
