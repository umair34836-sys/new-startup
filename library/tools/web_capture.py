# Free, local Firecrawl replacement (Crawl4AI 0.9, Apache-2.0, ~86k stars per Exa 2026-10-24): page -> clean markdown + full-page
# screenshot, using this container's Chromium. Runs in /home/user/tools/crawl-venv (setup-all.sh light).
#
#   /home/user/tools/crawl-venv/bin/python web_capture.py URL [URL ...] --out DIR [--width 1440] [--no-shot]
#
# Writes DIR/<slug>.md and DIR/<slug>.png per URL, and prints one line per URL.
# Limits: the site's domain must be allowed in the environment's network settings (Firecrawl fetched from its own
# servers, this does not), and Cloudflare-style anti-bot pages can refuse a headless browser.
import argparse, asyncio, base64, os, re

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")  # playwright 1.56.0 needs chromium-1194 there
# (container-dependent: on 2026-10-24 the image had chromium-1243 only and this script failed with "playwright install")
os.environ.setdefault("CRAWL4AI_NO_CLOUD_NOTICE", "1")
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

ap = argparse.ArgumentParser()
ap.add_argument("urls", nargs="+")
ap.add_argument("--out", required=True)
ap.add_argument("--width", type=int, default=1440)
ap.add_argument("--height", type=int, default=900)
ap.add_argument("--no-shot", action="store_true", help="markdown only")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)


def slug(url):
    s = re.sub(r"^https?://", "", url).strip("/")
    return re.sub(r"[^A-Za-z0-9]+", "_", s)[:80] or "page"


async def main():
    bc = BrowserConfig(headless=True, viewport_width=a.width, viewport_height=a.height, extra_args=["--no-sandbox"],
                       verbose=False)
    run = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, screenshot=not a.no_shot, scan_full_page=True,
                           wait_for_images=True, page_timeout=60000)
    async with AsyncWebCrawler(config=bc) as c:
        for url in a.urls:
            r = await c.arun(url, config=run)
            base = os.path.join(a.out, slug(url))
            if not r.success:
                print(f"FAIL {url}: {(r.error_message or '').splitlines()[0][:160] if r.error_message else r.status_code}")
                continue
            open(base + ".md", "w").write(str(r.markdown or ""))
            note = ""
            if r.screenshot:
                open(base + ".png", "wb").write(base64.b64decode(r.screenshot))
                note = f", screenshot {base}.png"
            print(f"OK   {url}: {len(str(r.markdown or ''))} chars -> {base}.md{note}")


asyncio.run(main())
