// Records the real aethelgrid.cloud pages + the public panel login page for the 9:16 AethelGrid reel (2026-10-28).
// 1080x1920 viewport with CSS zoom 1.4 (layout ~770 px wide, no horizontal overflow, measured 2026-10-28), cursor +
// ripple on every click. Only in-page toggles and "Copy" are clicked; Order Now / Login / Register are never pressed.
//   NODE_PATH="$(npm root -g)" node flow_aethelgrid.js <outdir> [shot ...]
const { Recorder } = require('/home/user/new-startup/library/tools/screen_recorder.js');
const out = process.argv[2];
const only = process.argv.slice(3);
const OPT = { width: 1080, height: 1920, zoom: 1.4, block: [/googletagmanager|google-analytics|doubleclick|recaptcha/] };
const hover = async (r, sel, ms = 700) => { const p = await r.target(sel); await r.moveTo(p.x, p.y, ms); await r.wait(350); };

const SHOTS = {
  async home(r) {      // hero cards -> features -> locations (lines 2-5)
    await r.goto('https://aethelgrid.cloud/', { wait: 3500 });
    for (const t of ['Instant Setup', 'DDoS Protection', '99.9% Uptime', '24/7 Support']) await hover(r, `h3:has-text("${t}"), :text-is("${t}")`);
    await r.mark('features'); await r.scrollTo('h2:has-text("Advanced")', { offset: 120, after: 1500 });
    for (const t of ['High Performance', 'Low Latency', 'Auto Recovery']) await hover(r, `:text-is("${t}")`);
    await r.mark('locations'); await r.scrollTo('h2:has-text("Global")', { offset: 120, after: 1500 });
    await hover(r, ':text-is("India")'); await hover(r, ':text-is("Germany")'); await r.wait(1200);
  },
  async minecraft(r) { // location toggle -> plans (lines 6-7)
    await r.goto('https://aethelgrid.cloud/minecraft', { wait: 2500 });
    await r.click('button:has-text("Germany")', { label: 'Germany' }); await r.wait(600);
    await r.click('button:has-text("India")', { label: 'India' });
    await r.mark('plans'); await r.scrollTo(':text("3. Choose Your Plan")', { offset: 60, after: 1500 });
    await hover(r, ':text("₹80.00")'); await hover(r, ':text("DDR4 ECC Memory") >> nth=0'); await hover(r, ':text("NVMe SSD Storage") >> nth=0');
    await hover(r, ':text("Premium Game Panel") >> nth=0'); await r.wait(800);
    await r.mark('more'); await r.scrollTo(':text("Gold Plan")', { offset: 200, after: 1800 }); await r.wait(800);
  },
  async vps(r) {       // processor toggle (line 8)
    await r.goto('https://aethelgrid.cloud/vps', { wait: 2500 });
    await r.click('button:has-text("AMD EPYC Premium")', { label: 'EPYC' }); await r.wait(900);
    await r.click('button:has-text("Intel Xeon Standard")', { label: 'Xeon' });
    await r.mark('plans'); await r.scrollTo(':text("3. Choose Your Plan")', { offset: 60, after: 1500 });
    await hover(r, ':text("₹285.00")'); await r.wait(1200);
  },
  async discord(r) {   // bot plans (line 9)
    await r.goto('https://aethelgrid.cloud/discord', { wait: 2500 });
    await r.scrollTo(':text("Lite Plan")', { offset: 300, after: 1500 });
    await hover(r, ':text("₹35.07")'); await r.mark('lavalink');
    await r.scrollTo(':text("LavaLink: V4")', { block: 'center', after: 1500 }); await hover(r, ':text("LavaLink: V4")'); await r.wait(1200);
  },
  async panel(r) {     // site's "Our Panel" tabs (line 10)
    await r.goto('https://aethelgrid.cloud/', { wait: 2000 });
    await r.scrollTo('h2:has-text("Experience Our")', { offset: 120, after: 1800 });
    for (const t of ['Main Dashboard', 'Server Dashboard', 'One-Click Plugin Installer', 'Version Changer'])
      await r.click(`button:has-text("${t}")`, { label: t, after: 1100 });
    await r.wait(800);
  },
  async login(r) {     // public panel login page (line 11): cursor only, nothing typed or clicked
    await r.goto('https://gp.aethelgrid.cloud/', { wait: 2500 });
    await hover(r, 'input >> nth=0', 900); await hover(r, 'input >> nth=1'); await hover(r, 'button:has-text("Login")'); await r.wait(1500);
  },
  async offer(r) {     // promo code card + real Copy click (line 12)
    await r.goto('https://aethelgrid.cloud/minecraft', { wait: 2500 });
    await hover(r, ':text("AETHEL25")', 900); await r.click('button:has-text("Copy")', { label: 'Copy', after: 1800 });
  },
};

(async () => {
  for (const [name, fn] of Object.entries(SHOTS)) {
    if (only.length && !only.includes(name)) continue;
    const r = await Recorder.launch({ out: `${out}/${name}`, ...OPT });
    try { await fn(r); } catch (e) { console.log(name, 'ERROR', String(e).slice(0, 200)); }
    const res = await r.finish(); console.log(name, res.duration.toFixed(1), 's', res.frames, 'frames');
  }
})();
