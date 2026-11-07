// Records plugin.firecraft.fun (copper_work) for the promo: public site pages + the owner's demo panel (logged-in state
// file made once with a Playwright login, kept in the scratchpad, never committed). 2026-11-07.
// A privacy mask runs in every page: IPv4 addresses, e-mail addresses, server keys (cwk_...) and UUIDs are replaced
// before they can be drawn. Only harmless things are really clicked: the console runs `list` (read-only), the AI chat
// opens an existing conversation, tabs/selects change view only. Add server / Save / Remove are never pressed.
//   NODE_PATH="$(npm root -g)" node flow_copperwork.js <outdir> <state.json> <16x9|9x16> [shot ...]
const { Recorder } = require('/home/user/new-startup/library/tools/screen_recorder.js');
const [out, state, fmt, ...only] = process.argv.slice(2);
const WIDE = fmt !== '9x16';
const OPT = { width: WIDE ? 1920 : 1080, height: WIDE ? 1080 : 1920, zoom: 1.4, storageState: state };
const MASK = `(() => {
  const RE = [[/\\b\\d{1,3}(\\.\\d{1,3}){3}(:\\d+)?\\b/g, '•••.•••.•••.•••'], [/[\\w.+-]+@[\\w-]+\\.[\\w.]+/g, 'you@email.com'],
              [/cwk_[A-Za-z0-9]+/g, 'cwk_••••••'], [/\\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\\b/gi, '••••-••••'],
              [/(\\[\\d\\d:\\d\\d:\\d\\d\\] )[^\\n]*(Async Chat|DiscordSRV|Chat Thread)[^\\n]*/g, '$1[chat] •••'],
              [/(of player |client |player )[A-Za-z0-9_]{3,16}/g, '$1Player'], [/\\b[A-Za-z0-9_]{3,16}(?= \\(\\/| joined the game| left the game|\\[\\/| logged in| lost connection)/g, 'Player']];
  const fix = n => { if (n.nodeType === 3) { let t = n.nodeValue, o = t; for (const [r, s] of RE) t = t.replace(r, s); if (t !== o) n.nodeValue = t; }
                     else if (n.childNodes) n.childNodes.forEach(fix);
                     if (n.tagName === 'INPUT' && n.value) for (const [r, s] of RE) n.value = n.value.replace(r, s); };
  const go = () => { fix(document.body); new MutationObserver(ms => ms.forEach(m => { m.addedNodes.forEach(fix); if (m.type === 'characterData') fix(m.target); }))
                     .observe(document.body, { childList: true, subtree: true, characterData: true }); };
  document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', go) : go();
})();`;
const scroll = async (r, sel, { offset = 120, after = 1400 } = {}) => {
  await r.page.locator(sel).first().evaluate((el, off) => window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - off, behavior: 'smooth' }), offset);
  await r.wait(after);
};
const hover = async (r, sel, ms = 650) => { const p = await r.target(sel); await r.moveTo(p.x, p.y, ms); await r.wait(350); };
const U = 'https://plugin.firecraft.fun';

const SHOTS = {
  async home(r) {      // hook + outbound only (lines 1-2)
    await r.goto(U + '/', { wait: 2500 });
    await hover(r, ':text("Outbound only plugin")'); await hover(r, 'h1'); await r.mark('feat');
    await scroll(r, ':text-is("Live console")', { offset: 200 });
    for (const t of ['Live console', 'Status and players', 'Pictures of the world', 'Your own AI key']) await hover(r, `:text-is("${t}")`);
    await r.mark('faq'); await scroll(r, ':text("Does the plugin open a port")', { offset: 200 });
    await hover(r, ':text("Does the plugin open a port")', 800); await r.wait(1500);
  },
  async dash(r) {      // servers connected + overview (line 4)
    await r.goto(U + '/dashboard', { wait: 2500 });
    await hover(r, ':text("FireCraft SMP") >> nth=0'); await hover(r, ':text("Connected") >> nth=0');
    await r.click('a:has-text("Open") >> nth=0', { label: 'Open', after: 2500 });
    for (const t of ['TPS', 'MSPT', 'RAM']) await hover(r, `:text-is("${t}")`);
    await hover(r, ':text("Worlds")'); await r.wait(1200);
  },
  async console(r) {   // live console, real `list` (line 3)
    await r.goto(U + '/s/1/console', { wait: 3000 });
    await r.type('input[placeholder*="console"], input[name=command]', 'list', { label: 'command' });
    await r.click('button:has-text("Run")', { label: 'Run', after: 3500 });
    await r.wait(1500);
  },
  async alerts(r) {    // offline / low TPS alerts (line 4 end)
    await r.goto(U + '/s/1/settings', { wait: 2500 });
    await scroll(r, ':text-is("Alerts")', { offset: 150 });
    await hover(r, ':text("Offline after")'); await hover(r, ':text("TPS below")'); await r.mark('tasks');
    await scroll(r, ':text-is("Scheduled tasks")', { offset: 150 }); await hover(r, ':text-is("Scheduled tasks")'); await r.wait(1200);
  },
  async pictures(r) {  // take-a-picture form (line 5)
    await r.goto(U + '/s/1', { wait: 2500 });
    await scroll(r, ':text("Take a picture")', { offset: 150 });
    await r.select('select >> nth=0', 'top').catch(() => {}); await r.wait(500);
    await hover(r, ':text("World") >> nth=0'); await hover(r, 'button:has-text("Take picture")', 800); await r.wait(1200);
  },
  async ai(r) {        // keys, providers, a real past chat (line 6)
    await r.goto(U + '/ai', { wait: 2500 });
    await hover(r, ':text("Your keys")'); await hover(r, ':text("free tier") >> nth=0');
    await hover(r, 'select >> nth=0', 800); await r.wait(600); await r.mark('chat');
    await r.click(':text("Who is online right now")', { label: 'chat', after: 3500 });
    await r.wait(2500);
  },
  async audit(r) {     // audit log (line 7)
    await r.goto(U + '/audit', { wait: 2500 });
    await hover(r, ':text("action.discord.create_channel") >> nth=0', 900); await hover(r, ':text("ai.failover") >> nth=0'); await r.wait(1500);
  },
  async discord(r) {   // bots + live features (line 8)
    await r.goto(U + '/discord', { wait: 2500 });
    await hover(r, ':text("Your bots")'); await r.mark('live');
    await scroll(r, ':text("Live features")', { offset: 150 });
    for (const t of ['Chat relay', 'Welcome new members', 'Auto-replies', 'Live status card']) await hover(r, `:text("${t}")`);
    await r.wait(1000);
  },
  async connect(r) {   // Claude connector + app (line 9)
    await r.goto(U + '/connect', { wait: 2500 });
    await hover(r, ':text("Claude app")'); await r.click('button:has-text("Copy") >> nth=0', { label: 'Copy', after: 1200 });
    await r.goto(U + '/download', { wait: 2000 }); await r.mark('app');
    await scroll(r, ':text("Android app")', { offset: 200 }); await hover(r, ':text("Android app") >> nth=1'); await r.wait(1200);
  },
  async steps(r) {     // three steps + versions (lines 10-11)
    await r.goto(U + '/', { wait: 2000 });
    await scroll(r, ':text("Three steps")', { offset: 200 });
    for (const t of ['Add a server', 'Drop the jar', 'Connected.']) await hover(r, `:text("${t}")`, 800);
    await r.goto(U + '/download', { wait: 2000 }); await r.mark('versions');
    await hover(r, ':text("Paper, Purpur or Spigot")', 900); await hover(r, 'a:has-text("copper_work.jar")'); await r.wait(1500);
  },
  async cta(r) {       // sign-up (line 12): cursor only
    await r.goto(U + '/', { wait: 2000 });
    await hover(r, 'a:has-text("Create a free account") >> nth=0', 900);
    await r.fakeClick('a:has-text("Create a free account") >> nth=0', { label: 'signup' }); await r.wait(1500);
  },
};

(async () => {
  for (const [name, fn] of Object.entries(SHOTS)) {
    if (only.length && !only.includes(name)) continue;
    // the public site looks different when logged in, so its shots run without the login state
    const pub = ['home', 'steps', 'cta'].includes(name);
    const r = await Recorder.launch({ out: `${out}/${name}`, ...OPT, storageState: pub ? undefined : state, initScripts: [MASK] });
    try { await fn(r); } catch (e) { console.log(name, 'ERROR', String(e).slice(0, 300)); }
    const res = await r.finish(); console.log(name, res.duration.toFixed(1), 's', res.frames, 'frames');
  }
})();
