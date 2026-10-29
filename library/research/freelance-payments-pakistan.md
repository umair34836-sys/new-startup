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
