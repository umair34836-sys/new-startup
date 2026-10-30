// Click every on-page toggle of aethelgrid.cloud (menus, FAQ, locations, processors, plan types, panel tabs, currency
// menu) and save the new text each state shows + a screenshot. Only buttons that change the page in place are
// clicked: "Order Now", "Get Started", "Copy" and links are never pressed. usage: node explore.js <outdir>
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path');
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const SKIP = /^(Order Now|Get Started|Copy|Learn More)$/i;
const PAGES = ['https://aethelgrid.cloud/', 'https://aethelgrid.cloud/minecraft', 'https://aethelgrid.cloud/vps', 'https://aethelgrid.cloud/discord'];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  for (const u of PAGES) {
    await p.goto(u, { waitUntil: 'networkidle', timeout: 60000 }); await p.waitForTimeout(1500);
    const slug = (new URL(u).pathname.replace(/\//g, '') || 'home');
    let log = `URL: ${u}\nFETCHED: ${new Date().toISOString()} (Playwright Chromium)\n`;
    const have = new Set((await p.evaluate(() => document.body.innerText)).split('\n').map(s => s.trim()));
    const n = await p.$$eval('button', bs => bs.length);
    for (let i = 0; i < n; i++) {
      const btn = (await p.$$('button'))[i]; if (!btn || !(await btn.isVisible())) continue;
      const label = (await btn.innerText()).trim().replace(/\s+/g, ' ').slice(0, 60);
      if (!label || SKIP.test(label)) continue;
      try {
        await btn.scrollIntoViewIfNeeded(); await btn.click({ timeout: 3000, noWaitAfter: true }); await p.waitForTimeout(900);
        if (p.url().replace(/\/$/, '') !== u.replace(/\/$/, '')) { log += `\n[${label}] navigated to ${p.url()} -> back\n`; await p.goto(u, { waitUntil: 'networkidle' }); continue; }
        const t = (await p.evaluate(() => document.body.innerText)).split('\n').map(s => s.trim()).filter(s => s && !have.has(s));
        t.forEach(s => have.add(s));
        log += `\n--- after clicking [${label}] ---\n${t.join('\n')}\n`;
        await p.screenshot({ path: path.join(out, `${slug}__${String(i).padStart(2, '0')}.png`) });
        const imgs = await p.evaluate(() => [...document.images].filter(im => im.offsetParent && im.getBoundingClientRect().top < innerHeight && im.getBoundingClientRect().bottom > 0).map(im => im.currentSrc));
        log += `(visible images: ${imgs.join(' ')})\n`;
        await p.keyboard.press('Escape');
      } catch (e) { log += `\n[${label}] ERROR ${String(e).slice(0, 120)}\n`; }
    }
    fs.writeFileSync(path.join(out, slug + '.txt'), log); console.log(slug, log.length);
  }
  await b.close();
})();
