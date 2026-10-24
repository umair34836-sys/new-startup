# Free, local Firecrawl replacement (Crawl4AI 0.9, Apache-2.0, ~86k stars per Exa 2026-10-24): page -> clean markdown + full-page
# screenshot, using this container's Chromium. Runs in /home/user/tools/crawl-venv (setup-all.sh light).
#
#   /home/user/tools/crawl-venv/bin/python web_capture.py URL [URL ...] --out DIR [--width 1440] [--no-shot]
#
# Writes DIR/<slug>.md and DIR/<slug>.png per URL, and prints one line per URL.
# Limits: the site's domain must be allowed in the environment's network settings (Firecrawl fetched from its own
# servers, this does not), and Cloudflare-style anti-bot pages can refuse a headless browser.
import argparse, asyncio, base64, glob, os, re, socket, subprocess, time

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")  # playwright 1.56.0 needs chromium-1194 there
# Container-dependent: on 2026-10-24 one image had chromium-1243 only and Playwright refused it ("playwright install").
# So if chromium-1194 is missing, start whatever Chromium the image has ourselves and attach over CDP.
os.environ.setdefault("CRAWL4AI_NO_CLOUD_NOTICE", "1")
MATCHING = glob.glob("/opt/pw-browsers/chromium-1194/chrome-linux*/chrome")
ANY = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))
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


def own_chromium():
    """Launch the image's Chromium with remote debugging; return (process, cdp_url)."""
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    p = subprocess.Popen([ANY[-1], "--headless=new", "--no-sandbox", f"--remote-debugging-port={port}",
                          f"--user-data-dir=/tmp/web_capture_{port}", "about:blank"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            socket.create_connection(("127.0.0.1", port), 0.2).close(); break
        except OSError:
            time.sleep(0.2)
    return p, f"http://127.0.0.1:{port}"


async def main():
    proc = None
    if MATCHING or not ANY:
        bc = BrowserConfig(headless=True, viewport_width=a.width, viewport_height=a.height, extra_args=["--no-sandbox"],
                           verbose=False)
    else:
        proc, cdp = own_chromium()
        bc = BrowserConfig(browser_mode="cdp", cdp_url=cdp, cdp_cleanup_on_close=True, headless=True, viewport_width=a.width,
                           viewport_height=a.height, verbose=False)
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
    return proc


proc = asyncio.run(main())
if proc:  # stop our own Chromium only after Crawl4AI has closed its CDP session
    proc.terminate()
