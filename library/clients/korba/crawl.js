// Read-only crawl of korba-restaurant.localoria.com (a Localoria listing page) in Chromium.
// Usage: node crawl.js <outdir>. Saves each page's text, full-page screenshot (scrolled in steps so lazy
// content loads), every JSON response, all links and every image/video URL the pages use. No forms, no clicks
// that send anything; ad hosts are blocked.
const {chromium} = require('playwright');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2] || 'crawl';
const PAGES = ['https://korba-restaurant.localoria.com/', 'https://korba-restaurant.localoria.com/full-menu'];
for (const d of ['text', 'shots', 'net', 'html']) fs.mkdirSync(path.join(OUT, d), {recursive: true});
const sleep = ms => new Promise(r => setTimeout(r, ms));
const AD = /googlesyndication|doubleclick|adservice|googletagmanager|google-analytics/;
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({viewport: {width: 1366, height: 900}});
  await ctx.route('**/*', r => AD.test(r.request().url()) ? r.abort() : r.continue());
  const media = new Set(); let netN = 0;
  const p = await ctx.newPage();
  p.on('response', async r => {
    const u = r.url(), ct = r.headers()['content-type'] || '';
    if (/image|video/.test(ct) || /\.(jpe?g|png|webp|gif|mp4|webm|mov)(\?|$)/i.test(u)) media.add(u);
    if (ct.includes('json')) { try { netN++; fs.writeFileSync(path.join(OUT, 'net', `${String(netN).padStart(3, '0')}.json`),
      JSON.stringify({url: u, when: new Date().toISOString(), body: await r.text()})); } catch (e) {} }
  });
  const report = {date: new Date().toISOString(), pages: []};
  for (const [i, url] of PAGES.entries()) {
    await p.goto(url, {waitUntil: 'networkidle', timeout: 90000}); await sleep(2000);
    for (let y = 0; y < 40; y++) { await p.mouse.wheel(0, 700); await sleep(250); }
    await sleep(1500);
    const name = String(i).padStart(2, '0') + '_' + (new URL(url).pathname.replace(/\W+/g, '_') || 'home');
    fs.writeFileSync(path.join(OUT, 'text', name + '.txt'), `URL: ${p.url()}\nDATE: ${new Date().toISOString()}\n\n` + await p.innerText('body'));
    fs.writeFileSync(path.join(OUT, 'html', name + '.html'), await p.content());
    await p.screenshot({path: path.join(OUT, 'shots', name + '.png'), fullPage: true});
    const dom = await p.evaluate(() => ({
      imgs: [...document.querySelectorAll('img')].map(x => x.currentSrc || x.src),
      videos: [...document.querySelectorAll('video, video source, iframe')].map(x => x.src || x.currentSrc),
      bgs: [...document.querySelectorAll('*')].map(e => getComputedStyle(e).backgroundImage).filter(s => s && s !== 'none'),
      links: [...document.querySelectorAll('a')].map(a => a.href),
    }));
    report.pages.push({url, ...dom});
  }
  report.mediaResponses = [...media];
  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 1));
  await b.close();
})();
