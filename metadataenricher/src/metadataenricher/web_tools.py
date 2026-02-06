import logging
from asyncio import Semaphore
from typing import TypedDict

import html2text
import trafilatura
from playwright.async_api import async_playwright

from . import env

log = logging.getLogger(__name__)
logging.getLogger("trafilatura").setLevel(logging.INFO)  # trafilatura is quite spammy

ignored_file_extensions: list[str] = [
    # file extensions that cause unexpected behavior when trying to render them with a headless browser
    ".aac",
    ".avi",
    ".bin",
    ".bmp",
    ".bz",
    ".cda",
    ".csv",
    ".doc",
    ".docx",
    ".epub",
    ".gz",
    ".mbz",
    ".mid",
    ".midi",
    ".mp3",
    ".mp4",
    ".mpeg",
    ".mpkg",
    ".odp",
    ".ods",
    ".odt",
    ".oga",
    ".ogx",
    ".opus",
    ".otf",
    ".pdf",
    ".pptx",
    ".rar",
    ".rtf",
    ".sh",
    ".tar",
    ".ts",
    ".ttf",
    ".txt",
    ".vsd",
    ".wav",
    ".weba",
    ".webm",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
    ".3gp",
    ".3g2",
    ".7z",
]


class UrlDataDict(TypedDict):
    html: str
    text: str
    cookies: dict[str, str] | None
    har: str | None
    screenshot_bytes: bytes | None


_sem_playwright: Semaphore = Semaphore(10)
# reminder: if you increase this Semaphore value, you NEED to change the "browserless v2"-docker-container
# configuration accordingly! (e.g., by increasing the MAX_CONCURRENT_SESSIONS and MAX_QUEUE_LENGTH configuration
# settings, see: https://www.browserless.io/docs/docker)

async def get_url_data(url: str) -> UrlDataDict | None:
    # Ignore URLs that look like binary files.
    # Note that this does not detect the case when a problematic MIME type is served
    # but the URL looks OK.
    bad_extension_found = any(url.endswith(ext) for ext in ignored_file_extensions)
    if bad_extension_found:
        log.warning("File extension in URL %s detected which cannot be rendered by headless browsers. Skipping WebTools rendering for this url...", url)
        return

    # relevant docs for this implementation: https://hub.docker.com/r/browserless/chrome#playwright and
    # https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp
    async with _sem_playwright:
        async with async_playwright() as p:
            log.debug("Fetching data with Playwright")
            ws_endpoint = env.get("PLAYWRIGHT_WS_ENDPOINT") + "/chrome/playwright"
            browser = await p.chromium.connect(ws_endpoint)
            browser = await browser.new_context(java_script_enabled=True)
            log.debug("  browser.new_page()")
            page = await browser.new_page()
            log.debug("  page.goto(url=%r)", url)
            await page.goto(url, wait_until="load", timeout=90000)
            # waits for a website to fire the DOMContentLoaded event or for a timeout of 90s
            # since waiting for 'networkidle' seems to cause timeouts
            html = await page.content()
            screenshot_bytes = await page.screenshot()
            # ToDo: HAR / cookies
            #  if we are able to replicate the Splash response with all its fields,
            #  we could save traffic/requests that are currently still being handled by Splash
            #  see: https://playwright.dev/python/docs/api/class-browsercontext#browser-context-cookies

        fulltext = ""
        html_bytes: bytes = html.encode()
        trafilatura_text: str | None = trafilatura.extract(html_bytes)
        if trafilatura_text:
            # trafilatura text extraction is (in general) more precise than html2Text, so we'll use it if available
            fulltext = trafilatura_text
        else:
            h = html2text.HTML2Text()
            h.ignore_links = True
            h.ignore_images = True
            fulltext = h.handle(html)

        return {"html": html,
                "text": fulltext,
                "cookies": None,
                "har": None,
                "screenshot_bytes": screenshot_bytes}
