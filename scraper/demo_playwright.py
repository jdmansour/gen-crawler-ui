
import asyncio
import base64
from pathlib import Path
from playwright.async_api import async_playwright

async def main():
    url = "https://www.spiegel.de"
    # url = "https://www.reddit.com/"
    # url = "https://www.gamestar.de/"
    #url = "https://www.heise.de/"
    url = "https://www.lehrer-online.de/"
    # url = "chrome://extensions/"
    cdp_endpoint = "http://localhost:9222"

    async with async_playwright() as p:
        # connect_over_cdp preserves the default browser context where extensions live
        browser = await p.chromium.connect_over_cdp(cdp_endpoint)

        # --- Verify extensions are loaded ---
        default_context = browser.contexts[0]
        print(f"Browser has {len(browser.contexts)} context(s)")
        print(f"Default context has {len(default_context.service_workers)} service worker(s)")
        for sw in default_context.service_workers:
            print(f"  Extension service worker: {sw.url}")

        page = await default_context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})

        await page.goto(url)
        dpr = await page.evaluate("window.devicePixelRatio")
        print(f"Device pixel ratio: {dpr}")

        await page.wait_for_load_state('networkidle', timeout=1000)

        # Use CDP Emulation to force DPR=2 for this page
        cdp = await default_context.new_cdp_session(page)
        await cdp.send("Emulation.setDeviceMetricsOverride", {
            "width": 1280,
            "height": 800,
            "deviceScaleFactor": 2,
            "mobile": False,
        })

        # Wait a moment for re-render at new DPR
        await page.wait_for_timeout(500)

        dpr2 = await page.evaluate("window.devicePixelRatio")
        print(f"Device pixel ratio after CDP override: {dpr2}")

        # Method 1: Playwright screenshot (may or may not respect CDP override)
        await page.screenshot(path="screenshot_playwright.png", scale="device")
        print("Saved screenshot_playwright.png")

        # Method 2: Raw CDP screenshot (most reliable for 2x)
        result = await cdp.send("Page.captureScreenshot", {
            "format": "png",
            "captureBeyondViewport": False,
        })
        png_data = base64.b64decode(result["data"])
        Path("screenshot_cdp.png").write_bytes(png_data)
        print(f"Saved screenshot_cdp.png ({len(png_data)} bytes)")

if __name__ == "__main__":
    asyncio.run(main())