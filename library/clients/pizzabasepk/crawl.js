// Read-only crawl of pizzabasepk.com (Indolj storefront) in Chromium.
// Usage: node crawl.js <outdir>. Selects order type + city (no cart, no login, no forms),
// saves page text, full-page screenshots, every JSON the page loads, and each menu item's popup.
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || 'crawl';
for (const d of ['text', 'shots', 'net', 'items']) fs.mkdirSync(path.join(OUT, d), {recursive: true});
const sleep = ms => new Promise(r => setTimeout(r, ms));
let netN = 0;
function hookNet(p, tag) {
  p.on('response', async r => {
    const ct = r.headers()['content-type'] || '';
    if (!ct.includes('json') || !r.url().includes('indolj')) return;
    try { const t = await r.text(); netN++;
      fs.writeFileSync(path.join(OUT, 'net', `${String(netN).padStart(3, '0')}_${tag}.json`), JSON.stringify({url: r.url(), when: new Date().toISOString(), body: t}));
    } catch (e) {}
  });
}
async function save(p, name) {
  fs.writeFileSync(path.join(OUT, 'text', name + '.txt'), `URL: ${p.url()}\nDATE: ${new Date().toISOString()}\n\n` + await p.innerText('body'));
  await p.screenshot({path: path.join(OUT, 'shots', name + '.png'), fullPage: true});
}
async function chooseCity(p, type, city) {
  await p.goto('https://pizzabasepk.com/', {waitUntil: 'networkidle', timeout: 90000}); await sleep(2500);
  await p.getByText(type, {exact: true}).first().click(); await sleep(1200);
  const sv = p.locator('div[class*=singleValue], div[class*=placeholder]').first();
  await sv.click({force: true}); await sleep(800);
  const opts = await p.locator('div[class*=option]').allInnerTexts();
  if (city) { await p.locator('div[class*=option]', {hasText: city}).first().click(); await sleep(1000); }
  return opts;
}
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({viewport: {width: 1366, height: 900}});
  const p = await ctx.newPage(); hookNet(p, 'home');
  await p.goto('https://pizzabasepk.com/', {waitUntil: 'networkidle', timeout: 90000}); await sleep(3000);
  await save(p, '00_home_modal');
  const report = {date: new Date().toISOString(), runs: []};
  for (const type of ['Delivery', 'Pick-Up']) {
    let opts = await chooseCity(p, type, null);
    // pick-up may need a branch too: record whatever dropdowns appear
    report.runs.push({type, cityOptions: opts});
    for (const city of opts) {
      await chooseCity(p, type, city);
      const sels = p.locator('div[class*=singleValue], div[class*=placeholder]');
      const n = await sels.count(); const extra = [];
      for (let i = 1; i < n; i++) { // second dropdown (area / branch)
        await sels.nth(i).click({force: true}); await sleep(800);
        extra.push(await p.locator('div[class*=option]').allInnerTexts());
        await p.keyboard.press('Enter'); await sleep(800);
      }
      await p.screenshot({path: path.join(OUT, 'shots', `modal_${type}_${city}.png`)});
      report.runs.push({type, city, secondDropdowns: extra});
      await p.getByRole('button', {name: 'Select'}).first().click().catch(() => {});
      await p.waitForLoadState('networkidle').catch(() => {}); await sleep(3500);
      // expand "Show More"
      await p.getByText('Show More').first().click().catch(() => {}); await sleep(500);
      for (let y = 0; y < 30; y++) { await p.mouse.wheel(0, 1200); await sleep(300); }
      await save(p, `menu_${type}_${city.replace(/\W+/g, '_')}`);
    }
  }
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 1));
  // links
  const links = [...new Set(await p.$$eval('a', a => a.map(x => x.href)))];
  fs.writeFileSync(path.join(OUT, 'links.txt'), links.join('\n'));
  await b.close();
})();
