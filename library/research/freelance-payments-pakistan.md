# Getting paid from abroad in Pakistan (Fiverr / Upwork) + Claude connectors (2026-10-29)

The owner asked on 2026-10-29: "kia me fiverr ya upwork k trough other country se Pakistan me payment le sakte hai ? Or kia
claude k sath connect ker sakte hai in mese kisi ek ko bhi ?"
These are WebSearch summaries from 2026-10-29. Pages were not opened one by one unless noted.
Fees and limits change, so re-check them on the official help pages before telling a client a number.

## Fiverr -> Pakistan
- **Payoneer is the main route.** The Fiverr help centre page "Setting up Payoneer as a payout method" (help.fiverr.com/hc/en-us/articles/14257019400465) lists, per the search summary:
  - bank transfer in local currency: 1-3 business days, $3 Payoneer fee, $20 minimum;
  - USD wire: slower, lower fee, $20 minimum;
  - only one active Payoneer method at a time.
- **Direct link to a Pakistani bank: not confirmed.** A Fiverr community thread asks whether it is possible. Blogs mention JazzCash / EasyPaisa, but these are unverified.
- **PayPal: not available in Pakistan** (several secondary sources).

## Upwork -> Pakistan
- **Payment methods:** "Direct to Local Bank" in PKR, Payoneer, wire transfer, and ACH to a US dollar account (Upwork community answers and blogs; not checked on Upwork's own help page).
- **Payoneer:**
  - one 2026 blog: 2% conversion fee for PKR withdrawals to a Pakistani bank, or $1.50 for a USD withdrawal;
  - other sources give different numbers. Unverified.
- **Direct to Local Bank (PKR):**
  - one 2026 blog says Upwork charges no fee, but the bank's exchange rate is ~1-3% under mid-market;
  - arrival in about 4 business days, or 3-7 business days in another blog. Unverified.
- **Upwork's own fee** on what the client pays is not covered here. Check Upwork's fee page.

## Claude connectors
- **Upwork: yes, an official connector exists.**
  - SearchMcpRegistry (2026-10-29) lists "Upwork – Hire talent or find work" in the Claude connector directory (directoryUuid 27973c01-..., 45+ tools, e.g. find_jobs, find_saved_jobs, confirm_draft, get_account, end_contract, boost_profile).
  - It is not connected in this account.
  - https://mcp.upwork.com/mcp answers 401 with an OAuth `resource_metadata` header (curl 2026-10-29), so it is a live OAuth MCP server.
  - Connect it from claude.ai Settings > Connectors.
- **Fiverr: no official connector found** (SearchMcpRegistry "fiverr" 2026-10-29: none).
  - Only unofficial options: KyuRish/fiverr-mcp-server (PyPI, public gig search) and Bright Data's Fiverr scraper MCP.
  - They read public gigs only; they don't manage your seller account. Unofficial servers need a code review before use.

Sources:
- [Fiverr help: Payoneer payout](https://help.fiverr.com/hc/en-us/articles/14257019400465-Payoneer-account)
- [Fiverr community: local bank question](https://community.fiverr.com/public/forum/boards/start-here-c9d/posts/344854-can-i-connect-a-pakistani-local-bank-account-directly-to-fiverr-for-withdrawals)
- [Upwork community: USD to PKR](https://community.upwork.com/t5/New-to-Upwork/How-much-do-upwork-cost-while-withdrawing-usd-to-pkr/m-p/1187580)
- [Upwork fees in Pakistan (elevatepay blog)](https://www.elevatepay.co/blog/upwork-fees-pakistan)
- [Payoneer vs Wise for Pakistani freelancers (abroadmate)](https://abroadmate.me/guides/payoneer-vs-wise-pakistan-freelancers-2026)
- [fiverr-mcp-server (PyPI)](https://pypi.org/project/fiverr-mcp-server/)
- [Bright Data Fiverr MCP](https://brightdata.com/ai/mcp-server/fiverr)

## Owner's Upwork profile (2026-10-29)
- The owner connected the Upwork connector (freelancer account). Via the connector, with his approval, these were set:
  - title "Video Editor | Promo Reels, YouTube Edits & Thumbnails"
  - overview (video-only, facts from delivered work, no client names)
  - 18 video/design skills (web skills removed at his choice)
  - availability: full time
  - English: Fluent
  - work history: Self-employed, Freelance Video Editor, from 2026-01-01, Islamabad (city and month are placeholders he accepted)
- Connector quirks:
  - add_employment country needs ISO alpha-3 ("PAK"); "PK" failed with "Invalid country code".
  - Only one language preview can be pending at a time.
  - Non-English languages are always added as BASIC, so Urdu/Hindi go in on the website as Native.
- Website-only (not in the connector): profile photo, hourly rate, portfolio items. The profile stays private / NOT_STARTED until those are done.

## Hourly rate research (2026-10-29, owner asked "hourly rate kitna rakhna chaye ?")
- Upwork find_freelancers search "video editor short form reels", location Pakistan (connector, 2026-10-29). The first 10
  results were not all in Pakistan. Their profile rates:
  - Pakistan: $5 (3 profiles, 0-1 jobs, $80+ to $5K+ earned), $19.99 (Top Rated Plus, 15 jobs)
  - Vietnam: $10, $15, $15, $19
  - Brazil: $8
  - Bangladesh: $30 (Top Rated Plus, $80K+ earned)
- Upwork Help Center via the connector (2026-10-29):
  - The Freelancer Service Fee "ranges from 0% to 15% per contract" and is deducted from the rate.
  - The rate form shows the fee and your net amount.
  - Source: support.upwork.com/hc/en-us/articles/211062538.
- WebSearch summary (2026-10-29; the page itself was not opened, because curl returned no text):
  - upwork.com/hire/video-editors/cost/ is quoted as "$6 - $25 per hour", median about $10.
- Advice given to the owner (judgment, not a measured fact):
  - start at $12/hr while the profile has 0 reviews;
  - raise to $15-20 after the first 3-5 good reviews;
  - bid per video or per project on fixed-price jobs.
