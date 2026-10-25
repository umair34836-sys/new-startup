// Second pass (read-only): menu in viewport-sized steps (the list is lazy), every item popup,
// hero slider images, the info pages (FAQ accordions opened). Usage: node crawl_items.js <outdir>
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || 'crawl', only = process.argv.slice(3); // optional item ids: popups only
for (const d of ['steps', 'items', 'pages']) fs.mkdirSync(path.join(OUT, d), {recursive: true});
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch();
  const p = await (await b.newContext({viewport: {width: 1366, height: 900}})).newPage();
  await p.goto('https://pizzabasepk.com/', {waitUntil: 'networkidle', timeout: 90000}); await sleep(2500);
  await p.getByRole('button', {name: 'Select'}).first().click(); // default: Delivery + Attock
  await p.waitForLoadState('networkidle').catch(() => {}); await sleep(4000);
  if (!only.length) {
  // hero slider: click "next" through the slides
  const imgs = new Set();
  for (let i = 0; i < 10; i++) {
    (await p.$$eval('img', a => a.map(x => x.currentSrc || x.src))).forEach(s => imgs.add(s));
    await p.screenshot({path: path.join(OUT, 'steps', `hero_${i}.png`), clip: {x: 0, y: 80, width: 1366, height: 600}});
    const nxt = p.locator('button[class*=next], .swiper-button-next, [aria-label*=ext]').first();
    if (await nxt.count()) await nxt.click({force: true}).catch(() => {}); await sleep(1200);
  }
  // step through the page
  const H = await p.evaluate(() => document.body.scrollHeight);
  let i = 0; const allText = [];
  for (let y = 0; y < H + 900; y += 700, i++) {
    await p.evaluate(yy => window.scrollTo(0, yy), y); await sleep(1300);
    (await p.$$eval('img', a => a.map(x => x.currentSrc || x.src))).forEach(s => imgs.add(s));
    await p.screenshot({path: path.join(OUT, 'steps', `step_${String(i).padStart(3, '0')}.png`)});
    allText.push(`--- y=${y}\n` + await p.innerText('body'));
  }
  fs.writeFileSync(path.join(OUT, 'steps', 'steps_text.txt'), allText.join('\n'));
  }
  // item popups: cards carry a price "Rs."; click each card by its title
  const menu = JSON.parse(JSON.parse(fs.readFileSync(path.join(OUT, 'structured_menu.json'))).body).details;
  const names = [];
  for (const c of Object.values(menu)) if (c && c.items) for (const k of c.sortedItemKeys) names.push([c.title.trim(), c.items[k].item_name.trim(), k]);
  const seenN = {};
  for (const [cat, name, id] of names) {
    const nth = seenN[name] = (seenN[name] ?? -1) + 1; // same name in several deal categories: page order = menu order
    if (only.length && !only.includes(id)) continue;
    try {
      await p.evaluate(() => window.scrollTo(0, 0)); await sleep(300);
      const loc = p.getByText(name, {exact: true}).nth(nth);
      for (let t = 0; t < 40 && !(await loc.isVisible().catch(() => false)); t++) { await p.mouse.wheel(0, 700); await sleep(250); }
      await loc.scrollIntoViewIfNeeded(); await loc.click(); await sleep(1800);
      const dlg = p.locator('[role=dialog], .modal-content, [class*=Modal]').last();
      const txt = await dlg.innerText().catch(() => p.innerText('body'));
      fs.writeFileSync(path.join(OUT, 'items', `${id}.txt`), `CATEGORY: ${cat}\nITEM: ${name}\nURL: ${p.url()}\nDATE: ${new Date().toISOString()}\n\n${txt}`);
      await p.screenshot({path: path.join(OUT, 'items', `${id}.png`)});
      await p.keyboard.press('Escape'); await sleep(600);
      if (p.url() !== 'https://pizzabasepk.com/') { await p.goBack(); await sleep(1500); }
    } catch (e) { fs.writeFileSync(path.join(OUT, 'items', `${id}.err`), String(e).slice(0, 500)); }
  }
  if (only.length) return b.close();
  fs.writeFileSync(path.join(OUT, 'images_seen.txt'), [...imgs].join('\n'));
  for (const u of ['https://pizzabasepk.com/pages/privacy-policy', 'https://pizzabasepk.com/pages/faqs']) {
    await p.goto(u, {waitUntil: 'networkidle', timeout: 90000}); await sleep(2500);
    const heads = p.locator('button[aria-expanded=false], [class*=accordion] button, details summary');
    for (let k = 0; k < await heads.count(); k++) { await heads.nth(k).click({force: true}).catch(() => {}); await sleep(250); }
    const n = u.split('/').pop();
    fs.writeFileSync(path.join(OUT, 'pages', n + '.txt'), `URL: ${u}\nDATE: ${new Date().toISOString()}\n\n` + await p.innerText('body'));
    await p.screenshot({path: path.join(OUT, 'pages', n + '.png'), fullPage: true});
  }
  await b.close();
})();
