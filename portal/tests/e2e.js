// End-to-end test of the whole loop in a real browser (Playwright, preinstalled) plus the bridge CLI.
// Run: PORTAL=http://127.0.0.1:8088 MEDIA=<dir with test.mp4, fake.mp4, photo.png> SHOTS=<dir> node tests/e2e.js
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const BASE = process.env.PORTAL || 'http://127.0.0.1:8088';
const MEDIA = process.env.MEDIA;
const SHOTS = process.env.SHOTS || '/tmp';
const BRIDGE = path.join(__dirname, '..', 'bridge', 'portal_bridge.py');
const env = { ...process.env, PORTAL_URL: BASE, PORTAL_BRIDGE_TOKEN: process.env.BRIDGE_TOKEN || 'pb_testtoken', NO_PROXY: '127.0.0.1,localhost', no_proxy: '127.0.0.1,localhost' };
let failures = 0;

function check(cond, msg) {
  console.log((cond ? 'PASS ' : 'FAIL ') + msg);
  if (!cond) failures++;
}
function bridge(...args) {
  return JSON.parse(execFileSync('python3', [BRIDGE, ...args], { env, encoding: 'utf8' }));
}
async function shot(page, name) {
  await page.waitForTimeout(700);
  await page.screenshot({ path: path.join(SHOTS, name + '.png'), fullPage: true });
}

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  const consoleErrors = [];
  page.on('console', (m) => { if (m.type() === 'error' && !/icons|favicon|404|status of 40[039]/.test(m.text())) consoleErrors.push(m.text()); });

  // 1. Client signs up.
  await page.goto(BASE + '/');
  await shot(page, '01-home');
  await page.click('text=Create account');
  await page.fill('input[name=name]', 'Test Client');
  await page.fill('input[name=email]', 'client1@example.com');
  await page.fill('input[name=phone]', '0300 0000000');
  await page.fill('input[name=password]', 'clientpass123');
  await page.click('button:has-text("Create account")');
  check(page.url().endsWith('/login') && (await page.textContent('.notice')).includes('approve'), 'register -> waits for approval');
  await page.fill('input[name=email]', 'client1@example.com');
  await page.fill('input[name=password]', 'clientpass123');
  await page.click('button:has-text("Log in")');
  check((await page.textContent('.notice')).includes('waiting for approval'), 'pending account cannot log in yet');

  // Owner approves the new client.
  const pa = await (await browser.newContext({ viewport: { width: 1280, height: 900 } })).newPage();
  await pa.goto(BASE + '/login');
  await pa.fill('input[name=email]', 'owner@example.com');
  await pa.fill('input[name=password]', 'ownerpass123');
  await pa.click('button:has-text("Log in")');
  check(pa.url().endsWith('/admin'), 'admin lands on admin orders');
  check((await pa.textContent('.notice')).includes('waiting for your approval'), 'admin sees the waiting account');
  async function approve(email) {
    await pa.goto(BASE + '/admin/clients');
    const r = pa.locator('form.client-row', { hasText: email });
    await r.locator('select[name=status]').selectOption('active');
    await r.locator('button:has-text("Save")').click();
  }
  await approve('client1@example.com');
  await page.fill('input[name=email]', 'client1@example.com');
  await page.fill('input[name=password]', 'clientpass123');
  await page.click('button:has-text("Log in")');
  check(page.url().endsWith('/orders'), 'approved client logs in -> orders page');

  // 2. New order with uploads and questionnaire.
  await page.click('button:has-text("New video order")');
  check(/\/orders\/\d+$/.test(page.url()), 'draft order created');
  const orderId = page.url().split('/').pop();
  await page.setInputFiles('#pick', [path.join(MEDIA, 'test.mp4'), path.join(MEDIA, 'photo.png')]);
  await page.waitForSelector('[data-file-list] li.done >> nth=1', { timeout: 60000 });
  check(true, 'two files uploaded in chunks (test.mp4 is bigger than one 1.5 MB chunk)');
  await page.setInputFiles('#pick', [path.join(MEDIA, 'fake.mp4')]);
  await page.waitForSelector('[data-file-list] li.failed', { timeout: 20000 });
  const failText = await page.textContent('[data-file-list] li.failed');
  check(/does not match/.test(failText), 'text file renamed .mp4 is rejected: ' + failText.trim().slice(0, 80));
  await page.fill('input[name=title]', 'Shop opening reel');
  await page.fill('input[name=length_sec]', '45');
  const est = await page.textContent('[data-estimate-value]');
  check(est.replace(/\s+/g, ' ').trim() === 'PKR 2,250', 'live estimate 45 s x 50 PKR = ' + est.trim());
  await page.selectOption('select[name="q[video_type]"]', 'Reel / Short / TikTok');
  await page.selectOption('select[name="q[platform]"]', 'Instagram / Facebook');
  await page.selectOption('select[name="q[aspect]"]', '9:16 vertical (phone)');
  await page.selectOption('select[name="q[style]"]', 'Energetic / fast cuts');
  await page.selectOption('select[name="q[music]"]', 'Upbeat');
  await page.fill('textarea[name=ideas]', 'Start with the shop sign, end with our phone number.');
  await shot(page, '02-order-form');
  await page.click('button[data-submit]');
  check((await page.textContent('.notice')).includes('Order sent'), 'order submitted');
  await shot(page, '03-order-received');

  // 3. Bridge picks it up, downloads, delivers version 1.
  let ev = bridge('events').events.filter((e) => String(e.order.id) === orderId);
  check(ev.length === 1 && ev[0].event.type === 'order_submitted', 'bridge sees order_submitted');
  check(ev[0].order.answers['Editing style'] === 'Energetic / fast cuts', 'bridge gets questionnaire answers with labels');
  bridge('take', String(ev[0].event.id));
  const dl = bridge('download', orderId, path.join(SHOTS, 'dl'));
  const orig = fs.statSync(path.join(MEDIA, 'test.mp4')).size;
  check(dl.files.some((f) => f.size === orig), 'bridge downloaded the raw video byte-exact size ' + orig);
  const d1 = bridge('deliver', orderId, path.join(MEDIA, 'test.mp4'), '--note', 'Version 1: first cut.');
  check(d1.ok === true, 'bridge delivered version 1');

  // 4. Client sees it and asks for changes.
  await page.goto(BASE + '/orders/' + orderId);
  check(await page.isVisible('video.player'), 'client sees the video player');
  const range = await page.evaluate(async (u) => { const r = await fetch(u, { headers: { Range: 'bytes=0-99' } }); return [r.status, (await r.arrayBuffer()).byteLength]; },
    BASE + (await page.getAttribute('video.player', 'src')));
  check(range[0] === 206 && range[1] === 100, 'video file supports Range (206, 100 bytes)');
  await shot(page, '04-version-ready');
  await page.fill('.review textarea[name=body]', 'Make the music louder and add our logo at the end.');
  await page.click('button:has-text("Send changes")');
  check((await page.textContent('.badge')).includes('Changes requested'), 'status = Changes requested');

  ev = bridge('events').events.filter((e) => String(e.order.id) === orderId);
  check(ev.some((e) => e.event.type === 'revision_requested'), 'bridge sees revision_requested');
  check(ev[0].order.messages.some((m) => m.kind === 'revision' && m.body.includes('music louder')), 'revision text reaches the bridge');
  bridge('deliver', orderId, path.join(MEDIA, 'test.mp4'), '--note', 'Version 2: music louder, logo added.');

  // 5. Client approves.
  await page.goto(BASE + '/orders/' + orderId);
  check((await page.textContent('.card h2')).includes('Version 2'), 'client sees Version 2');
  page.once('dialog', (d) => d.accept());
  await page.click('button:has-text("approve")');
  check((await page.textContent('.badge')).includes('Approved'), 'order approved');
  await shot(page, '05-approved');
  check(bridge('events').events.some((e) => String(e.order.id) === orderId && e.event.type === 'approved'), 'bridge sees approved');

  // 6. Security checks.
  const noCsrf = await page.evaluate(async (u) => (await fetch(u, { method: 'POST', body: new URLSearchParams({ body: 'x' }) })).status, BASE + '/orders/' + orderId + '/message');
  check(noCsrf === 403, 'POST without CSRF token -> 403');
  const ctx2 = await browser.newContext();
  const p2 = await ctx2.newPage();
  await p2.goto(BASE + '/register');
  await p2.fill('input[name=name]', 'Other Client');
  await p2.fill('input[name=email]', 'client2@example.com');
  await p2.fill('input[name=password]', 'clientpass456');
  await p2.click('button:has-text("Create account")');
  await approve('client2@example.com');
  await p2.fill('input[name=email]', 'client2@example.com');
  await p2.fill('input[name=password]', 'clientpass456');
  await p2.click('button:has-text("Log in")');
  const other = await p2.goto(BASE + '/orders/' + orderId);
  check(other.status() === 404, "another client cannot open this order (404)");
  const fileId = dl.files[0].id;
  const otherFile = await p2.goto(BASE + '/files/' + fileId);
  check(otherFile.status() === 404, "another client cannot download this order's file (404)");
  const anon = await (await browser.newContext()).request.get(BASE + '/files/' + fileId, { maxRedirects: 0 });
  check(anon.status() === 303, 'logged-out visitor is sent to login (303)');
  const badTok = await p2.request.get(BASE + '/api/bridge/events', { headers: { Authorization: 'Bearer wrong' } });
  check(badTok.status() === 401, 'bridge API with wrong token -> 401');
  const adminPage = await p2.goto(BASE + '/admin');
  check(adminPage.status() === 403, 'client cannot open admin (403)');
  const storage = await p2.request.get(BASE + '/../storage/install-key.txt');
  check(storage.status() === 404, 'storage folder is not served (404)');

  // Parallel chunks at the same offset: only one may be written (file must not grow past its size).
  const race = await page.evaluate(async ([base]) => {
    const csrf = document.body.dataset.csrf;
    const h = { 'X-CSRF-Token': csrf };
    const nr = await fetch(base + '/orders/new', { method: 'POST', body: new URLSearchParams({ _csrf: csrf }) });
    const oid = Number(nr.url.split('/').pop());
    const init = await (await fetch(base + '/upload/init', { method: 'POST', headers: { ...h, 'Content-Type': 'application/json' },
      body: JSON.stringify({ order_id: oid, name: 'race.txt', size: 1000 }) })).json();
    const body = new Uint8Array(1000).fill(65);
    const rs = await Promise.all([0, 1, 2, 3, 4].map(() => fetch(base + '/upload/chunk?token=' + init.token + '&offset=0',
      { method: 'POST', headers: { ...h, 'Content-Type': 'application/octet-stream' }, body }).then((r) => r.json())));
    return rs.map((r) => r.received);
  }, [BASE]);
  check(race.every((r) => r === 1000), 'parallel chunk race: file stays exactly 1000 bytes (' + race.join(',') + ')');

  // 7. Admin sets a client rate.
  await pa.goto(BASE + '/admin');
  await shot(pa, '06-admin-orders');
  await pa.goto(BASE + '/admin/clients');
  const row = pa.locator('form.client-row', { hasText: 'client1@example.com' });
  await row.locator('input[name=rate_pkr]').fill('80');
  await row.locator('button:has-text("Save")').click();
  await shot(pa, '07-admin-clients');
  await page.goto(BASE + '/orders');
  await page.click('button:has-text("New video order")');
  await page.fill('input[name=length_sec]', '10');
  check((await page.textContent('[data-estimate-value]')).trim() === 'PKR 800', 'per-client rate 80 PKR/s used: 10 s = PKR 800');
  await pa.goto(BASE + '/admin/orders/' + orderId);
  await shot(pa, '08-admin-order');
  await pa.goto(BASE + '/admin/settings');
  await shot(pa, '09-admin-settings');

  // 8. Login rate limit.
  const p3 = await (await browser.newContext()).newPage();
  await p3.goto(BASE + '/login');
  const tok = await p3.inputValue('input[name=_csrf]');
  const statuses = [];
  for (let i = 0; i < 11; i++) {
    const r = await p3.request.post(BASE + '/login', { form: { email: 'x@example.com', password: 'nope', _csrf: tok } });
    statuses.push(r.status());
  }
  check(statuses[0] === 200 && statuses[10] === 429, 'login rate limit: 10 tries allowed, 11th -> 429 (' + statuses.join(',') + ')');

  check(consoleErrors.length === 0, 'no console errors (' + consoleErrors.join(' | ').slice(0, 200) + ')');
  await browser.close();
  console.log(failures ? `${failures} FAILED` : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
