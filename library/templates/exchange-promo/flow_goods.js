// Records the real goodss.store pages + Discord invite page for the GOOD's promos (2026-11-02).
// Cursor + ripple on every click. Only in-page tabs, the calculator selects/amount and anchor scrolls are used;
// the exchange form is never filled or submitted, the Discord "Accept Invite" is never pressed.
//   NODE_PATH="$(npm root -g)" node flow_goods.js <outdir> <portrait|landscape> [shot ...]
const { Recorder } = require('/home/user/new-startup/library/tools/screen_recorder.js');
const [out, fmt] = process.argv.slice(2, 4);
const only = process.argv.slice(4);
const OPT = fmt === 'landscape'
  ? { width: 1920, height: 1080, zoom: 1.35 }
  : { width: 1080, height: 1920, zoom: 1.4 };
OPT.block = [/googletagmanager|google-analytics|doubleclick|web3forms/];
const scroll = async (r, sel, { offset = 120, after = 1400 } = {}) => {
  await r.page.locator(sel).first().evaluate((el, off) => {
    const z = parseFloat(getComputedStyle(document.documentElement).zoom || '1') || 1;
    const y = el.getBoundingClientRect().top + window.scrollY - off;
    window.scrollTo({ top: y, behavior: 'smooth' });
  }, offset);
  r.log('scroll', { sel }); await r.wait(after);
};
const hover = async (r, sel, ms = 650) => { const p = await r.target(sel); await r.moveTo(p.x, p.y, ms); await r.wait(300); };
const SITE = 'https://www.goodss.store/';
const SHOTS = {
  async hero(r) {
    await r.goto(SITE, { wait: 3000 });
    await hover(r, '#hero-rates-btn'); await hover(r, '#hero-calc-btn'); await r.wait(800);
  },
  async rates(r) {
    await r.goto(SITE, { wait: 2500 });
    await scroll(r, '#rates', { offset: 40 });
    await r.mark('pkr'); await r.click('#filter-pkr', { label: 'PKR', after: 1600 });
    await r.mark('crypto'); await r.click('#filter-crypto', { label: 'CRYPTO', after: 1600 });
    await r.mark('gift'); await r.click('#filter-binance-gift', { label: 'BINANCE GIFT', after: 1600 });
    await r.mark('all'); await r.click('#filter-all', { label: 'All', after: 1500 });
  },
  async calc(r) {
    await r.goto(SITE, { wait: 2500 });
    await scroll(r, '#calculator', { offset: 40 });
    await r.select('#calc-send-currency', 'PKR', { label: 'PKR' });
    await r.select('#calc-receive-currency', 'USDT', { label: 'Crypto' });
    await r.mark('type'); await r.type('#calc-amount', '32500', { label: 'amount', after: 1800 });
    await hover(r, '#calc-receive-display', 700); await r.wait(1200);
  },
  async how(r) {
    await r.goto(SITE, { wait: 2500 });
    await scroll(r, '#how-it-works', { offset: 40 });
    for (const s of ['#step-1', '#step-2', '#step-3']) await hover(r, s, 700);
    await r.wait(900);
  },
  async contact(r) {
    await r.goto(SITE, { wait: 2500 });
    await scroll(r, '#contact', { offset: 40 });
    for (const s of ['#channel-discord', '#channel-telegram', '#channel-whatsapp', '#channel-email', '#availability-card']) await hover(r, s, 600);
    await r.wait(900);
  },
  async discord(r) {
    await r.goto('https://discord.com/invite/goods', { wait: 5000 });
    await r.wait(1500);
  },
};
(async () => {
  for (const [name, fn] of Object.entries(SHOTS)) {
    if (only.length && !only.includes(name)) continue;
    const r = await Recorder.launch({ out: `${out}/${name}`, ...OPT });
    try { await fn(r); } catch (e) { console.log(name, 'ERROR', String(e).slice(0, 300)); }
    const res = await r.finish(); console.log(name, res.duration.toFixed(1), 's', res.frames, 'frames');
  }
})();
