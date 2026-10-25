const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('https://pakwebhoster.com/', { waitUntil: 'networkidle', timeout: 60000 });
  const r = await p.evaluate(() => {
    const bg = {}, fg = {}, fonts = {};
    document.querySelectorAll('body *').forEach(e => { const s = getComputedStyle(e); const a = e.getBoundingClientRect().width * e.getBoundingClientRect().height;
      if (s.backgroundColor !== 'rgba(0, 0, 0, 0)') bg[s.backgroundColor] = (bg[s.backgroundColor] || 0) + a;
      if (e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) { fg[s.color] = (fg[s.color] || 0) + 1; fonts[s.fontFamily] = (fonts[s.fontFamily] || 0) + 1; } });
    const top = o => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, 10);
    return { bg: top(bg), fg: top(fg), fonts: top(fonts), loaded: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight) };
  });
  console.log(JSON.stringify(r, null, 1)); await b.close();
})();
