// Sharp element screenshots of hostlixo.in for videos (2x device scale). Saves PNGs into <outdir> (scratchpad only:
// never commit them). Read-only: clicks only the Monthly/Annual toggle is NOT done; nothing is submitted.
// usage: node shots.js <outdir>
const { chromium } = require('playwright');
const path = require('path');
const out = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 2 });
  const shot = async (url, find, name, pad = 0) => {
    await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 80)); } window.scrollTo(0, 0); });
    const box = await p.evaluate(([f, pad]) => {
      const el = [...document.querySelectorAll('h1,h2,h3,div,section')].find(e => e.innerText && e.innerText.trim().startsWith(f.text) && (!f.minH || e.getBoundingClientRect().height >= f.minH));
      if (!el) return null; let t = el; for (let i = 0; i < (f.up || 0); i++) t = t.parentElement;
      t.scrollIntoView({ block: 'center' }); const r = t.getBoundingClientRect();
      return { x: Math.max(0, r.x - pad), y: Math.max(0, r.y - pad), width: r.width + 2 * pad, height: r.height + 2 * pad };
    }, [find, pad]);
    if (!box) { console.log('NOT FOUND', name); return; }
    await p.waitForTimeout(600);
    await p.screenshot({ path: path.join(out, name + '.png'), clip: box });
    console.log(name, JSON.stringify(box));
  };
  // hero viewport of home + minecraft page top
  for (const [u, n] of [['https://hostlixo.in/', 'home-hero'], ['https://hostlixo.in/minecraft.html', 'mc-top'], ['https://hostlixo.in/terms.html', 'terms-top']]) {
    await p.goto(u, { waitUntil: 'networkidle', timeout: 60000 }); await p.waitForTimeout(800);
    await p.screenshot({ path: path.join(out, n + '.png') }); console.log(n);
  }
  await shot('https://hostlixo.in/minecraft.html', { text: 'AMD EPYC™ • 100% CPU', up: 1, minH: 300 }, 'plans-grid', 16);
  await shot('https://hostlixo.in/minecraft.html', { text: 'RECOMMENDED', up: 0, minH: 300 }, 'plan-8gb', 16);
  await shot('https://hostlixo.in/terms.html', { text: '24-HOUR MONEY-BACK GUARANTEE', up: 0, minH: 150 }, 'refund-card', 16);
  await b.close();
})();
