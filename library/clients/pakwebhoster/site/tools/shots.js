// Clean full-page screenshots (no menus opened) of the given pages, with every big image hidden
// (img or CSS background, png/jpg/webp/svg, larger than 160x160 px on screen, except the logo): the site's hero
// images are stock photos of people (some embedded inside .svg files), and the repo never stores people's photos.
// Also lists every image URL used per page.  usage: node shots.js <urls.txt> <shots_dir> <images.json>
const { chromium } = require('playwright');
const fs = require('fs');
const [urlsFile, out, imgOut] = process.argv.slice(2);
fs.mkdirSync(out, { recursive: true });
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const imgs = {};
  for (const line of fs.readFileSync(urlsFile, 'utf8').split('\n').filter(Boolean)) {
    const [url, name] = line.split(' ');
    const page = await ctx.newPage();
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
      await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) {
        window.scrollTo(0, y); await new Promise(r => setTimeout(r, 100)); } window.scrollTo(0, 0); });
      await page.waitForTimeout(800);
      const list = await page.evaluate(() => {
        const s = new Set(); const raster = /\.(jpe?g|png|webp|gif|svg)(\?|$)/i; let hidden = 0;
        document.querySelectorAll('*').forEach(e => {
          const src = e.tagName === 'IMG' ? (e.currentSrc || e.src) : null;
          const m = getComputedStyle(e).backgroundImage.match(/url\("?([^")]+)"?\)/);
          if (src) s.add(src); if (m) s.add(m[1]);
          const r = e.getBoundingClientRect(); const big = r.width > 160 && r.height > 160;
          const testim = /testimonilas/i;
          if (src && raster.test(src) && !/logo/i.test(src) && (big || testim.test(src))) { e.style.setProperty('visibility', 'hidden', 'important'); e.style.setProperty('opacity', '0', 'important'); hidden++; }
          if (m && raster.test(m[1]) && (big || testim.test(m[1]))) { e.style.setProperty('background-image', 'none', 'important'); hidden++; }
        });
        return { urls: [...s], hidden };
      });
      for (const u of list.urls) (imgs[u] = imgs[u] || []).push(url);
      await page.screenshot({ path: `${out}/${name}.png`, fullPage: true });
      console.log('shot', name, 'photos hidden:', list.hidden);
    } catch (e) { console.log('ERR', url, String(e).slice(0, 150)); }
    await page.close();
  }
  fs.writeFileSync(imgOut, JSON.stringify(imgs, null, 1));
  await browser.close();
})();
