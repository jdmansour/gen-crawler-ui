import base64
import logging
import socket
import urllib.parse
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


def replace_host_with_ip(cdp_endpoint: str) -> str:
    "Parses a URL and replaces the hostname with its IP address."
    parsed = urllib.parse.urlparse(cdp_endpoint)
    host = parsed.hostname or "localhost"
    port = parsed.port
    path = parsed.path
    try:
        ip_address = socket.gethostbyname(host)
    except Exception as e:
        log.error("Failed to resolve host %s: %s", host, e)
        raise

    return f"{parsed.scheme}://{ip_address}:{port}{path}"


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
            log.info("Fetching URL with Playwright: %s", url)
            cdp_endpoint = env.get("PLAYWRIGHT_CDP_ENDPOINT")
            log.info("PLAYWRIGHT_CDP_ENDPOINT: %s", cdp_endpoint)

            # Chrome does not allow connections if a host header is sent which is not
            # localhost or an IP address. Passing headers to connect_over_cdp doesn't
            # seem to work, so we resolve the IP address here.
            cdp_endpoint = replace_host_with_ip(cdp_endpoint)
            log.info("CDP endpoint with resolved IP: %s", cdp_endpoint)

            browser = await p.chromium.connect_over_cdp(cdp_endpoint)
            # Use the default browser context so extensions (uBlock, ISDCAC) are active
            context = browser.contexts[0]
            page = await context.new_page()
            await page.goto(url, wait_until="load", timeout=90000)
            # waits for a website to fire the DOMContentLoaded event or for a timeout of 90s
            # since waiting for 'networkidle' seems to cause timeouts
            html = await page.content()

            # Use CDP to capture a 2x retina screenshot.
            # Playwright's page.screenshot() ignores CDP emulation overrides
            # on the default browser context, so we use raw CDP calls instead.
            cdp = await context.new_cdp_session(page)
            await cdp.send("Emulation.setDeviceMetricsOverride", {
                "width": 1280,
                "height": 800,
                "deviceScaleFactor": 2,
                "mobile": False,
            })
            result = await cdp.send("Page.captureScreenshot", {
                "format": "png",
                "captureBeyondViewport": False,
            })
            screenshot_bytes = base64.b64decode(result["data"])
            await cdp.detach()

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
