# TikTok / TikTok Lite access (research 2026-10-24)

## What happened here (measured 2026-10-24)
- `yt-dlp` (in /home/user/tools/venv) on a TikTok link (vm.tiktok.com -> www.tiktok.com/@<user>/video/<id>): ERROR
  "Unexpected response from webpage request", with the warning "The extractor is attempting impersonation, but no
  impersonate target is available".
- TikTok oEmbed (`https://www.tiktok.com/oembed?url=...`) answered only with a browser User-Agent and gave an embed
  iframe, no caption text.
- web_capture.py (Crawl4AI, headless Chromium) loaded the page but the player said "We're having trouble playing this
  video", page text 1 character.
- TikTok Lite share links are normal vm.tiktok.com links that redirect to www.tiktok.com (seen above), so any TikTok
  tool covers TikTok Lite links too.

## Open-source options (sources read 2026-10-24 via agent-reach web search / raw.githubusercontent.com)
| Repo | What it is | Stars | Licence | Notes |
|---|---|---|---|---|
| yt-dlp/yt-dlp | downloader we already use for YouTube; has a TikTok extractor | (not re-read) | Unlicense | TikTok extractor supports browser impersonation (commit 5513036, 2025-10-01); impersonation needs the `curl_cffi` package (yt_dlp/networking/_curlcffi.py) |
| Evil0ctal/Douyin_TikTok_Download_API | self-hosted TikTok/Douyin/Bilibili data + no-watermark download API, MCP, Docker | 20,859 | Apache-2.0 (LICENSE) | heavier: a server to run |
| davidteather/TikTok-Api | unofficial TikTok API wrapper in Python (PyPI TikTokApi v7.3.3) | 6,715 | MIT | needs Playwright browsers (`python -m playwright install`) |

Not installed: the owner decides. Use only for watching/summarising; never re-upload other people's TikToks.
