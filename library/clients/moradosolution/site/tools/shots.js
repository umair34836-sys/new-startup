// Full-page screenshots of key pages + list of every image URL used on any page.
// usage: node shots.js <urls.txt> <shots_dir> <images.json>
const { chromium } = require('playwright');
const fs = require('fs');
const [urlsFile, out, imgOut] = process.argv.slice(2);
const SHOT = ['/', '/game-hosting', '/minecraft-budget', '/hytale', '/vps', '/vds-bare-metal', '/bare-metal',
  '/infrastructure', '/ddos-protection', '/sales', '/about', '/services', '/status', '/support', '/contact'];
fs.mkdirSync(out, { recursive: true });
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const imgs = {};
  for (const url of fs.readFileSync(urlsFile, 'utf8').split('\n').filter(Boolean)) {
    const page = await ctx.newPage();
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
      await page.waitForTimeout(1200);
      const list = await page.evaluate(() => {
        const s = new Set();
        document.querySelectorAll('img').forEach(i => i.currentSrc && s.add(i.currentSrc));
        document.querySelectorAll('*').forEach(e => {
          const m = getComputedStyle(e).backgroundImage.match(/url\("?([^")]+)"?\)/); if (m) s.add(m[1]); });
        return [...s];
      });
      for (const u of list) (imgs[u] = imgs[u] || []).push(new URL(url).pathname);
      const p = new URL(url).pathname.replace(/\/$/, '') || '/';
      if (SHOT.includes(p)) {
        // scroll through once so lazy images load
        await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) {
          window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
        await page.waitForTimeout(800);
        const name = (p === '/' ? 'home' : p.slice(1)) + '.png';
        await page.screenshot({ path: `${out}/${name}`, fullPage: true });
        console.log('shot', name);
      }
    } catch (e) { console.log('ERR', url, String(e).slice(0, 150)); }
    await page.close();
  }
  fs.writeFileSync(imgOut, JSON.stringify(imgs, null, 1));
  await browser.close();
})();
