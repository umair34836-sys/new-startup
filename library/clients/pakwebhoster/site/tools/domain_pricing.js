// Full TLD price table from the client area (the page shows 10 rows; pick "All" in the Show-entries select).
// usage: node domain_pricing.js <out.txt>
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto('https://user.pakwebhoster.com/index.php?rp=/domain/pricing', { waitUntil: 'networkidle', timeout: 60000 });
  await p.selectOption('select:has(option[value="-1"])', '-1'); await p.waitForTimeout(1500);
  const rows = await p.$$eval('table tr', trs => trs.map(tr => [...tr.querySelectorAll('th,td')].map(c => c.innerText.replace(/\s+/g, ' ').trim()).join(' | ')));
  fs.writeFileSync(process.argv[2], `URL: https://user.pakwebhoster.com/index.php?rp=/domain/pricing (Show entries = All)\nFETCHED: ${new Date().toISOString()}\n\n` + rows.join('\n') + '\n');
  console.log(rows.length); await b.close();
})();
