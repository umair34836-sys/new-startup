// Render every public page of hostlixo.in (+ any same-site subdomain linked from it, e.g. a billing/client area)
// in Chromium; open every accordion/tab/dropdown; save visible text, links and a full-page screenshot.
// Never logs in, orders, adds to cart or submits a form.
// usage: node crawl.js <urls.txt> <outdir>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [urlsFile, out] = process.argv.slice(2);
const HOSTS = (process.env.HOSTS || 'hostlixo.in').split(',');
// client-area paths that log in, register, add to cart, check out, or switch language/currency
const BLOCK = /(rp=\/login|login|register|clientarea|cart\.php\?a=(add|view|checkout|confcart)|a=add|pwreset|submitticket|logout|language=|currency=|dologin|\/cart\/|\/password|cdn-cgi|affiliates|\/index\.php\/login|rp=%2F)/i;
fs.mkdirSync(path.join(out, 'pages'), { recursive: true });
fs.mkdirSync(path.join(out, 'screens'), { recursive: true });

const norm = (u) => { const x = new URL(u); x.hash = '';
  if (x.hostname.startsWith('www.')) x.hostname = x.hostname.slice(4);
  if (x.hostname === HOSTS[0]) x.search = '';
  x.pathname = x.pathname.replace(/\/+$/, '') || '/'; return x.toString(); };
const slug = (u) => { const x = new URL(u);
  let s = (x.hostname !== HOSTS[0] ? x.hostname.split('.')[0] + '__' : '') + (x.pathname.replace(/^\/|\/$/g, '') || 'home') + x.search;
  return s.replace(/[^A-Za-z0-9._-]+/g, '_').slice(0, 120); };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 },
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36' });
  const queue = fs.readFileSync(urlsFile, 'utf8').split('\n').filter(Boolean).map(norm);
  const seen = new Set(queue);
  const index = []; const external = new Set();
  while (queue.length) {
    const url = queue.shift();
    const page = await ctx.newPage();
    let status = null, text = '', extra = [], title = '', links = [], err = null, finalUrl = url;
    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const r = await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
        status = r ? r.status() : null; finalUrl = page.url();
        await page.waitForTimeout(1500);
        // scroll so lazy content/counters load
        await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) {
          window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); });
        title = await page.title();
        const base = await page.evaluate(() => document.body.innerText);
        // click every tab-like control (custom openTabings tabs, bootstrap tabs/pills, billing toggles) and keep
        // whatever new text each state shows
        const ctrls = await page.$$('[onclick*="openTab"], [data-bs-toggle="tab"], [data-bs-toggle="pill"], [role="tab"], .nav-tabs a, .nav-pills a, .nav-pills button, input[type="checkbox"], input[type="radio"], [class*="toggle"]:not(.dropdown-toggle):not(.navbar-toggler), [class*="switch"]');
        const have = new Set(base.split('\n').map(s => s.trim()));
        for (const c of ctrls) {
          try {
            if (!(await c.isVisible())) continue;
            const label = (await c.evaluate(e => (e.innerText || e.value || e.getAttribute('onclick') || e.className || '').trim().slice(0, 60)));
            await c.click({ timeout: 3000, noWaitAfter: true }); await page.waitForTimeout(500);
            if (page.url() !== finalUrl) { await page.goBack(); continue; }
            const t = await page.evaluate(() => document.body.innerText);
            const fresh = t.split('\n').map(s => s.trim()).filter(s => s && !have.has(s));
            fresh.forEach(s => have.add(s));
            if (fresh.length) extra.push(`--- after clicking [${label}] ---\n` + fresh.join('\n'));
          } catch (e) {}
        }
        // open every accordion/collapse/dropdown/tab pane and <details> so hidden text is in innerText
        await page.evaluate(() => {
          document.querySelectorAll('details').forEach(d => d.open = true);
          document.querySelectorAll('.collapse, .accordion-collapse, .tab-pane, .dropdown-menu, .tabcontent, [class*="tab-content"] > *').forEach(e => {
            e.classList.add('show', 'active'); e.style.display = 'block'; e.style.height = 'auto'; e.style.visibility = 'visible'; });
        });
        await page.waitForTimeout(400);
        const all = await page.evaluate(() => document.body.innerText);
        const hidden = all.split('\n').map(s => s.trim()).filter(s => s && !have.has(s));
        if (hidden.length) extra.push('--- hidden text (accordions/tabs/dropdowns opened) ---\n' + hidden.join('\n'));
        text = base;
        links = await page.evaluate(() => [...document.querySelectorAll('a[href]')].map(a => a.href));
        const s = slug(url);
        await page.screenshot({ path: path.join(out, 'screens', s + '.png'), fullPage: true });
        err = null; break;
      } catch (e) { err = String(e).slice(0, 200); }
    }
    await page.close();
    const s = slug(url);
    fs.writeFileSync(path.join(out, 'pages', s + '.txt'),
      `URL: ${url}\nFINAL_URL: ${finalUrl}\nHTTP: ${status}\nTITLE: ${title}\nFETCHED: ${new Date().toISOString()} (Playwright Chromium, rendered innerText)\n\n${text}\n\n${extra.join('\n\n')}\n`);
    index.push({ url, finalUrl, slug: s, status, title, chars: text.length, extraLines: extra.join('\n').split('\n').length, err });
    console.log(status, text.length, url, err || '');
    for (const l of links) {
      let u; try { u = new URL(l); } catch { continue; }
      if (!/^https?:$/.test(u.protocol)) { if (/^(mailto|tel|whatsapp):/.test(u.protocol)) external.add(l); continue; }
      const h = u.hostname.replace(/^www\./, '');
      if (!HOSTS.includes(h)) { external.add(u.origin + u.pathname + u.search); continue; }
      if (BLOCK.test(u.pathname + u.search)) { external.add('(not crawled) ' + l); continue; }
      // relative links on the client area nest forever (index.php/store/index.php/...): skip
      if ((u.pathname + u.search).split('index.php').length > 2 || (u.pathname.match(/\/store\//g) || []).length > 1) continue;
      // product pages (/store/<group>/<product>) are the first step of an order: not opened
      if (/rp=\/store\/[^/]+\/[^/]+/.test(u.search) || /\/store\/[^/]+\/[^/]+/.test(u.pathname)) { external.add('(not crawled, order step) ' + l); continue; }
      const n = norm(l);
      if (/\.(png|jpe?g|webp|gif|svg|pdf|xml|txt|ico|css|js|zip)$/i.test(new URL(n).pathname)) continue;
      if (!seen.has(n)) { seen.add(n); queue.push(n); }
    }
  }
  fs.writeFileSync(path.join(out, 'pages', '_index.json'), JSON.stringify({ pages: index, external: [...external].sort() }, null, 1));
  await browser.close();
})();
