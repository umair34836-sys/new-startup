// Brand facts of hostlixo.in from the rendered page: most-used colours (by area / text count), fonts, CSS custom
// properties, and every image the pages load (img src, CSS backgrounds, inline SVG count). Read-only.
// usage: node brand.js [url ...] > brand.json
const { chromium } = require('playwright');
(async () => {
  const urls = process.argv.slice(2).length ? process.argv.slice(2) : ['https://hostlixo.in/', 'https://hostlixo.in/minecraft.html'];
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  const out = {};
  for (const u of urls) {
    await p.goto(u, { waitUntil: 'networkidle', timeout: 60000 });
    await p.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } });
    out[u] = await p.evaluate(() => {
      const bg = {}, fg = {}, fonts = {}, imgs = new Set();
      document.querySelectorAll('body *').forEach(e => { const s = getComputedStyle(e); const r = e.getBoundingClientRect(); const a = r.width * r.height;
        if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') bg[s.backgroundColor] = (bg[s.backgroundColor] || 0) + a;
        if (s.backgroundImage && s.backgroundImage !== 'none') (s.backgroundImage.match(/url\("?([^")]+)"?\)/g) || []).forEach(m => imgs.add(m.replace(/^url\("?|"?\)$/g, '')));
        if ([...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) { fg[s.color] = (fg[s.color] || 0) + 1; fonts[s.fontFamily] = (fonts[s.fontFamily] || 0) + 1; } });
      document.querySelectorAll('img').forEach(i => imgs.add(i.currentSrc || i.src));
      document.querySelectorAll('link[rel*="icon"]').forEach(l => imgs.add(l.href));
      const vars = {}; for (const sh of document.styleSheets) { try { for (const r of sh.cssRules) if (r.selectorText === ':root') for (const k of r.style) if (k.startsWith('--')) vars[k] = r.style.getPropertyValue(k).trim(); } catch (e) {} }
      const top = o => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, 12);
      return { bg: top(bg), fg: top(fg), fonts: top(fonts), cssVars: vars, images: [...imgs], inlineSvgs: document.querySelectorAll('svg').length,
        loadedFonts: [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight))] };
    });
  }
  console.log(JSON.stringify(out, null, 1)); await b.close();
})();
