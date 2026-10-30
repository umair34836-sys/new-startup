// Tests the native app's screens (mobile/www) in Chromium against a local portal API, including offline work.
// Run: APPURL=http://127.0.0.1:8091 PORTAL=http://127.0.0.1:8088 MEDIA=<dir> SHOTS=<dir> NODE_PATH=$(npm root -g) node tests/app_e2e.js
const { chromium, request } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path');

const APP = process.env.APPURL || 'http://127.0.0.1:8091';
const BASE = process.env.PORTAL || 'http://127.0.0.1:8088';
const MEDIA = process.env.MEDIA;
const SHOTS = process.env.SHOTS || '/tmp';
const BRIDGE = path.join(__dirname, '..', 'bridge', 'portal_bridge.py');
const env = { ...process.env, PORTAL_URL: BASE, PORTAL_BRIDGE_TOKEN: process.env.BRIDGE_TOKEN || 'pb_testtoken', NO_PROXY: '127.0.0.1,localhost', no_proxy: '127.0.0.1,localhost' };
let failures = 0;
function check(c, m) { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) failures++; }
function bridge(...a) { return JSON.parse(execFileSync('python3', [BRIDGE, ...a], { env, encoding: 'utf8' })); }
async function shot(p, n) { await p.waitForTimeout(600); await p.screenshot({ path: path.join(SHOTS, 'app-' + n + '.png'), fullPage: true }); }

async function fillOrder(page, title) {
  await page.setInputFiles('#pick', [path.join(MEDIA, 'test.mp4'), path.join(MEDIA, 'photo.png')]);
  await page.waitForSelector('#files li >> nth=1');
  await page.fill('input[name=title]', title);
  await page.fill('#len', '30');
  await page.selectOption('select[name="q.video_type"]', 'Promo / Ad');
  await page.selectOption('select[name="q.platform"]', 'TikTok');
  await page.selectOption('select[name="q.aspect"]', '9:16 vertical (phone)');
  await page.selectOption('select[name="q.style"]', 'Cinematic');
  await page.selectOption('select[name="q.sound"]', 'Voice + music');
  await page.fill('textarea[name=ideas]', 'Made in the app.');
}
async function waitOrderListed(page, title, ms) {
  const end = Date.now() + ms;
  while (Date.now() < end) {
    await page.evaluate(() => { location.hash = '#/orders?' + Date.now(); location.hash = '#/orders'; });
    await page.waitForTimeout(1500);
    const t = await page.textContent('#main');
    if (t.includes(title) && /Received|In editing/.test(t)) return true;
  }
  return false;
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await ctx.addInitScript(() => { window.APP_SKIP_SPLASH = true; });
  const page = await ctx.newPage();
  const errs = [];
  page.on('pageerror', (e) => errs.push(e.message));
  page.on('dialog', (d) => d.accept());

  // Register inside the app.
  await page.goto(APP + '/');
  await page.waitForSelector('h1');
  check((await page.textContent('h1')) === 'Log in', 'app opens on its own login screen (UI is inside the app)');
  await page.click('text=Create an account');
  await page.fill('input[name=name]', 'App Client');
  await page.fill('input[name=email]', 'app1@example.com');
  await page.fill('input[name=password]', 'apppass1234');
  await page.click('button:has-text("Create account")');
  await page.waitForSelector('text=My videos');
  check(true, 'register in the app -> My videos');
  await page.waitForFunction(() => localStorage.getItem('token'), null, { timeout: 10000 });
  const token = await page.evaluate(() => JSON.parse(localStorage.getItem('token')));
  check(/^pa_[a-f0-9]{64}$/.test(token), 'app keeps a device token (no cookies)');

  // Online order.
  await page.click('text=+ New video order');
  await fillOrder(page, 'Online app order');
  const est = (await page.textContent('#est')).trim();
  check(est === 'PKR 1,500', 'live estimate in the app (30 s x 50) = ' + est);
  await shot(page, '01-new-order');
  await page.click('button:has-text("Submit order")');
  check(await waitOrderListed(page, 'Online app order', 40000), 'online order uploaded and sent (shows Received)');

  // Details-only order in the app (no files).
  await page.evaluate(() => { location.hash = '#/new'; });
  await page.waitForSelector('#pick', { state: 'attached' });
  await page.fill('input[name=title]', 'App details only');
  await page.fill('#len', '15');
  await page.click('button:has-text("Submit order")');
  await page.waitForSelector('.form-err');
  check(/Editing style|Details about the video/.test(await page.textContent('.form-err')), 'app blocks submit with missing required fields');
  for (const [k, v] of [['video_type', 'Explainer'], ['platform', 'YouTube'], ['aspect', '16:9 wide (YouTube)'], ['style', 'Cinematic'], ['sound', 'Only music / beats (no voice)']]) {
    await page.selectOption(`select[name="q.${k}"]`, v);
  }
  await page.fill('textarea[name=ideas]', 'No footage, please make it from stock clips and text.');
  await page.click('button:has-text("Submit order")');
  check(await waitOrderListed(page, 'App details only', 30000), 'app order with only details (no files) is sent');

  // Offline order: made with no internet, sent automatically later.
  await ctx.setOffline(true);
  await page.evaluate(() => window.dispatchEvent(new Event('offline')));
  check(await page.isVisible('#netbar'), 'offline bar shows');
  await page.evaluate(() => { location.hash = '#/new'; });
  await page.waitForSelector('#pick');
  await fillOrder(page, 'Offline app order');
  await page.click('button:has-text("Submit order")');
  await page.waitForSelector('text=Waiting to send');
  check(true, 'offline order is kept on the phone ("Waiting to send")');
  await shot(page, '02-offline-waiting');
  await ctx.setOffline(false);
  await page.evaluate(() => window.dispatchEvent(new Event('online')));
  check(await waitOrderListed(page, 'Offline app order', 60000), 'offline order sent by itself when the internet came back');
  const evs = bridge('events', '--full').events.filter((e) => e.event.type === 'order_submitted' && e.order.client.email === 'app1@example.com');
  check(evs.length === 3, 'bridge sees all three app orders (' + evs.length + ')');
  const onlineId = evs.find((e) => e.order.title === 'Online app order').order.id;
  check(evs.filter((e) => e.order.files.length).every((e) => e.order.files.length === 2 && e.order.files.some((f) => f.size === 4487461)), 'all files arrived byte-exact (video 4487461 bytes)');

  // Studio delivers; client watches, saves offline, works offline.
  bridge('deliver', String(onlineId), path.join(MEDIA, 'test.mp4'), '--note', 'Version 1 from the studio.');
  await page.evaluate((id) => { location.hash = '#/order/' + id; }, onlineId);
  await page.waitForSelector('#player');
  await page.waitForTimeout(1000);
  check(/\/api\/v1\/files\/\d+\?u=\d+&exp=\d+&sig=[a-f0-9]{64}/.test(await page.getAttribute('#player', 'src')), 'video plays from a signed link');
  await shot(page, '03-version');
  await page.click('#save-off');
  await page.waitForSelector('text=Saved on this phone', { timeout: 30000 });
  check(true, 'video saved on the phone for offline');
  await ctx.setOffline(true);
  await page.evaluate(() => window.dispatchEvent(new Event('offline')));
  await page.evaluate(() => { location.hash = '#/orders'; });
  await page.waitForTimeout(500);
  await page.evaluate((id) => { location.hash = '#/order/' + id; }, onlineId);
  await page.waitForSelector('#player');
  await page.waitForTimeout(800);
  check((await page.getAttribute('#player', 'src')).startsWith('blob:'), 'offline: video plays from the phone');
  check((await page.textContent('#main')).includes('copy saved on this phone'), 'offline: order details from the phone');
  await page.fill('#fc textarea', 'Offline change: louder music.');
  await page.click('button:has-text("Send changes")');
  await page.waitForTimeout(500);
  check((await page.textContent('#main')).includes('will be sent when you are online'), 'offline: change request waits in the outbox');
  await shot(page, '04-offline-changes');
  await ctx.setOffline(false);
  await page.evaluate(() => window.dispatchEvent(new Event('online')));
  let ok = false;
  for (let i = 0; i < 20 && !ok; i++) {
    await page.waitForTimeout(1000);
    ok = bridge('events', '--full').events.some((e) => e.order.id === onlineId && e.event.type === 'revision_requested' && e.order.messages.some((m) => m.body.includes('Offline change')));
  }
  check(ok, 'change request sent by itself when online again');

  // Approve.
  bridge('deliver', String(onlineId), path.join(MEDIA, 'test.mp4'), '--note', 'Version 2.');
  await page.evaluate(() => { location.hash = '#/orders'; });
  await page.waitForTimeout(500);
  await page.evaluate((id) => { location.hash = '#/order/' + id; }, onlineId);
  await page.waitForSelector('text=Version 2');
  await page.click('button:has-text("approve")');
  await page.waitForTimeout(1500);
  await page.evaluate((id) => { location.hash = '#/orders'; location.hash = '#/order/' + id; }, onlineId);
  await page.waitForTimeout(1500);
  check((await page.textContent('#main')).includes('Approved'), 'approve from the app');

  // API security for the app.
  const r = await request.newContext();
  const noTok = await r.get(BASE + '/api/v1/orders');
  check(noTok.status() === 401, 'app API without token -> 401');
  const bad = await r.get(BASE + '/api/v1/orders', { headers: { Authorization: 'Bearer pa_' + '0'.repeat(64) } });
  check(bad.status() === 401, 'app API with a fake token -> 401');
  const other = await r.post(BASE + '/api/v1/register', { data: { name: 'Other', email: 'app2@example.com', password: 'otherpass123' } });
  const oTok = (await other.json()).token;
  const steal = await r.get(BASE + '/api/v1/orders/' + onlineId, { headers: { Authorization: 'Bearer ' + oTok } });
  check(steal.status() === 404, "another app user cannot read this order (404)");
  const det = await (await r.get(BASE + '/api/v1/orders/' + onlineId, { headers: { Authorization: 'Bearer ' + token } })).json();
  const url = det.order.versions[0].url;
  check((await r.get(url)).status() === 200, 'signed link works');
  check((await r.get(url.replace(/sig=[a-f0-9]{8}/, 'sig=00000000'))).status() === 403, 'tampered signature -> 403');
  check((await r.get(url.replace(/u=\d+/, 'u=999'))).status() === 403, 'signed link for another user id -> 403');
  check((await r.get(url.replace(/exp=\d+/, 'exp=1000'))).status() === 403, 'expired link -> 403');
  const cors = await r.fetch(BASE + '/api/v1/login', { method: 'OPTIONS', headers: { Origin: 'https://evil.example.com', 'Access-Control-Request-Method': 'POST' } });
  check(!cors.headers()['access-control-allow-origin'], 'CORS: other websites are not allowed');

  // Logout.
  await page.evaluate(() => { location.hash = '#/account'; });
  await page.waitForSelector('#out');
  await shot(page, '05-account');
  await page.click('#out');
  await page.waitForSelector('text=Log in');
  const after = await r.get(BASE + '/api/v1/orders', { headers: { Authorization: 'Bearer ' + token } });
  check(after.status() === 401, 'logout kills the device token');
  check(errs.length === 0, 'no JavaScript errors (' + errs.join(' | ').slice(0, 200) + ')');
  await browser.close();
  console.log(failures ? `${failures} FAILED` : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
