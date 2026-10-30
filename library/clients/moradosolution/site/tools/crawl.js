// Render every public page of moradosolution.in in Chromium and save its visible text + links.
// usage: node crawl.js <urls.txt> <outdir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [urlsFile, out] = process.argv.slice(2);
const BLOCK = ['/admin', '/dashboard', '/cart', '/checkout', '/billing', '/login', '/register',
  '/verify-email', '/google-callback', '/api/'];
const HOST = 'moradosolution.in';
fs.mkdirSync(out, { recursive: true });

const norm = (u) => { const x = new URL(u); x.hash = ''; x.search = '';
  let p = x.pathname.replace(/\/+$/, '') || '/'; return `https://${HOST}${p}`; };
const slug = (u) => (new URL(u).pathname.replace(/^\/|\/$/g, '').replace(/\//g, '__') || 'home');

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1366, height: 900 },
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36' });
  const queue = fs.readFileSync(urlsFile, 'utf8').split('\n').filter(Boolean).map(norm);
  const seen = new Set(queue);
  const index = [];
  const external = new Set();
  while (queue.length) {
    const url = queue.shift();
    const page = await ctx.newPage();
    let status = null, text = '', title = '', links = [], err = null;
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const r = await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
        status = r ? r.status() : null;
        await page.waitForTimeout(1500);
        // open <details>/accordions so FAQ answers are in the text
        await page.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
        title = await page.title();
        text = await page.evaluate(() => document.body.innerText);
        links = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.href));
        err = null; break;
      } catch (e) { err = String(e).slice(0, 200); }
    }
    await page.close();
    const s = slug(url);
    fs.writeFileSync(path.join(out, s + '.txt'),
      `URL: ${url}\nHTTP: ${status}\nTITLE: ${title}\nFETCHED: ${new Date().toISOString()} (Playwright Chromium, rendered innerText)\n\n${text}\n`);
    index.push({ url, slug: s, status, title, chars: text.length, err });
    console.log(status, text.length, url, err || '');
    for (const l of links) {
      let u; try { u = new URL(l); } catch { continue; }
      if (!/^https?:$/.test(u.protocol)) { if (u.protocol === 'mailto:') external.add(l); continue; }
      if (u.hostname.replace(/^www\./, '') !== HOST) { external.add(u.origin + u.pathname); continue; }
      const n = norm(l);
      if (BLOCK.some(b => new URL(n).pathname.startsWith(b))) continue;
      if (/\.(png|jpe?g|webp|svg|pdf|xml|txt|ico|css|js)$/i.test(n)) continue;
      if (!seen.has(n)) { seen.add(n); queue.push(n); }
    }
  }
  fs.writeFileSync(path.join(out, '_index.json'), JSON.stringify({ pages: index, external: [...external].sort() }, null, 1));
  await browser.close();
})();
