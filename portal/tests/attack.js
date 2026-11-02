// Attacker-view regression tests (run against a throw-away copy, never the live site).
// Run: PORTAL=http://127.0.0.1:8088 MEDIA=<dir with photo.png> NODE_PATH=$(npm root -g) node tests/attack.js
const { chromium, request } = require('playwright');
const path = require('path');
const fs = require('fs');
const os = require('os');

const BASE = process.env.PORTAL || 'http://127.0.0.1:8088';
const MEDIA = process.env.MEDIA;
let failures = 0;
function check(cond, msg) {
  console.log((cond ? 'PASS ' : 'FAIL ') + msg);
  if (!cond) failures++;
}
const XSS = '<img src=x onerror=alert(1)><script>alert(2)</script>"\'><svg onload=alert(3)>';

async function client(browser, email) {
  const ctx = await browser.newContext();
  await ctx.addInitScript(() => { try { sessionStorage.setItem('splashSkip', '1'); } catch (e) {} });
  const page = await ctx.newPage();
  let dialogs = 0;
  page.on('dialog', (d) => { dialogs++; d.dismiss(); });
  await page.goto(BASE + '/register');
  await page.fill('input[name=name]', XSS);
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'attackpass123');
  await page.click('button:has-text("Create account")');
  return { ctx, page, dialogs: () => dialogs };
}
async function csrf(page) {
  return page.evaluate(() => document.body.dataset.csrf);
}
async function api(page, url, opts) {
  return page.evaluate(async ([u, o]) => {
    const r = await fetch(u, o);
    return { status: r.status, text: await r.text(), ct: r.headers.get('content-type'), cd: r.headers.get('content-disposition'), nosniff: r.headers.get('x-content-type-options') };
  }, [BASE + url, opts]);
}

(async () => {
  const browser = await chromium.launch();
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'atk-'));

  // Outsider checks (no login).
  const anon = await request.newContext();
  const home = await anon.get(BASE + '/');
  const h = home.headers();
  check(/frame-ancestors 'none'/.test(h['content-security-policy'] || '') && h['x-frame-options'] === 'DENY', 'clickjacking blocked (CSP frame-ancestors + X-Frame-Options)');
  check(!/unsafe-inline/.test(h['content-security-policy'] || ''), 'CSP has no unsafe-inline scripts');
  check(h['x-content-type-options'] === 'nosniff', 'nosniff header');
  const cookie = (h['set-cookie'] || '');
  check(/HttpOnly/i.test(cookie) && /SameSite=Lax/i.test(cookie), 'session cookie HttpOnly + SameSite');
  for (const p of ['/../app/config.php', '/../config.php', '/../storage/install-key.txt', '/app/bootstrap.php', '/storage/', '/.htaccess', '/index.php/../../app/db.php']) {
    const r = await anon.get(BASE + p);
    check(r.status() >= 400 || !/<\?php|db_pass/.test(await r.text()), 'not served: ' + p + ' (' + r.status() + ')');
  }
  const sqli = await anon.get(BASE + '/login');
  const tok = (await sqli.text()).match(/name="_csrf" value="([a-f0-9]+)"/)[1];
  const s1 = await anon.post(BASE + '/login', { form: { _csrf: tok, email: "owner@example.com' OR '1'='1", password: "' OR '1'='1" }, maxRedirects: 0 });
  check(s1.status() === 200 && /Wrong email or password/.test(await s1.text()), 'SQL injection in login fails');
  const s2 = await anon.post(BASE + '/login', { form: { _csrf: tok, email: 'owner@example.com', password: 'wrong' }, maxRedirects: 0 });
  const s3 = await anon.post(BASE + '/login', { form: { _csrf: tok, email: 'nobody@example.com', password: 'wrong' }, maxRedirects: 0 });
  check((await s2.text()).includes('Wrong email or password') && (await s3.text()).includes('Wrong email or password'), 'same message for wrong password and unknown email');
  const resetBad = await anon.get(BASE + '/reset?token=../../config');
  check((await resetBad.text()).includes('wrong or expired'), 'bad reset token refused');
  const forgot = await anon.post(BASE + '/forgot', { form: { _csrf: tok, email: 'nobody@example.com' } });
  check((await forgot.text()).includes('If an account with that email exists'), 'forgot password does not reveal accounts');
  if (process.env.DIR) {
    // Host header poisoning: a forged Host must not end up in the reset link.
    const ev = await request.newContext({ extraHTTPHeaders: { Host: 'evil-attacker.example' } });
    const pg = await ev.get(BASE + '/forgot');
    const t2 = (await pg.text()).match(/name="_csrf" value="([a-f0-9]+)"/)[1];
    await ev.post(BASE + '/forgot', { form: { _csrf: t2, email: 'owner@example.com' } });
    const mails = fs.readFileSync(path.join(process.env.DIR, 'mail.log'), 'utf8').trim().split('\n').map(JSON.parse);
    const last = mails.reverse().find((x) => x.subject === 'Reset your password');
    check(last && last.body.includes(BASE + '/reset?token=') && !last.body.includes('evil-attacker'), 'forged Host header does not reach the reset email');
  }
  for (const p of ['/api/bridge/events', '/api/bridge/events?token=pb_testtoken', '/api/bridge/files/1']) {
    check((await anon.get(BASE + p)).status() === 401, 'bridge API refuses without Bearer token: ' + p);
  }
  const redir = await anon.get(BASE + '//evil.example.com/', { maxRedirects: 0 });
  check(!/evil\.example\.com/.test(redir.headers()['location'] || ''), 'no open redirect via //host');

  // Session fixation: a planted session id is not accepted / replaced at login.
  const fx = await browser.newContext();
  await fx.addCookies([{ name: 'portal_sid', value: 'attackerchosenid1234567890', url: BASE }]);
  const fp = await fx.newPage();
  await fp.goto(BASE + '/login');
  await fp.fill('input[name=email]', 'owner@example.com');
  await fp.fill('input[name=password]', 'ownerpass123');
  await fp.click('button:has-text("Log in")');
  const sid = (await fx.cookies()).find((c) => c.name === 'portal_sid');
  check(sid && sid.value !== 'attackerchosenid1234567890', 'session fixation: planted session id is replaced');
  await fx.close();

  // Two clients: A attacks B.
  const A = await client(browser, 'attacker@example.com');
  const B = await client(browser, 'victim@example.com');
  await B.page.click('button:has-text("New video order")');
  const bOrder = B.page.url().split('/').pop();
  await B.page.setInputFiles('#pick', [path.join(MEDIA, 'photo.png')]);
  await B.page.waitForSelector('[data-file-list] li.done', { timeout: 20000 });
  await B.page.reload();
  const bFile = await B.page.evaluate(() => document.querySelector('form[id^=del-]').id.slice(4));
  // B starts an upload; A tries to write into B's upload token.
  const bTok = JSON.parse((await api(B.page, '/upload/init', { method: 'POST', headers: { 'X-CSRF-Token': await csrf(B.page), 'Content-Type': 'application/json' },
    body: JSON.stringify({ order_id: Number(bOrder), name: 'b.txt', size: 10 }) })).text).token;
  await A.page.goto(BASE + '/orders');
  const aCsrf = await csrf(A.page);
  const idor = [
    await api(A.page, '/orders/' + bOrder, {}),
    await api(A.page, '/files/' + bFile, {}),
    await api(A.page, '/files/' + bFile + '/download', {}),
    await api(A.page, '/upload/chunk?token=' + bTok + '&offset=0', { method: 'POST', headers: { 'X-CSRF-Token': aCsrf, 'Content-Type': 'application/octet-stream' }, body: 'AAAAAAAAAA' }),
    await api(A.page, '/upload/init', { method: 'POST', headers: { 'X-CSRF-Token': aCsrf, 'Content-Type': 'application/json' }, body: JSON.stringify({ order_id: Number(bOrder), name: 'x.png', size: 10 }) }),
    await api(A.page, '/orders/' + bOrder + '/message', { method: 'POST', body: new URLSearchParams({ _csrf: aCsrf, body: 'hi' }).toString(), headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),
    await api(A.page, '/orders/' + bOrder + '/files/' + bFile + '/delete', { method: 'POST', body: new URLSearchParams({ _csrf: aCsrf }).toString(), headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),
  ];
  check(idor.every((r) => r.status === 404), "client A cannot read, write or delete client B's order, files, uploads or messages (" + idor.map((r) => r.status).join(',') + ')');
  const tokTrav = await api(A.page, '/upload/chunk?token=../../config&offset=0', { method: 'POST', headers: { 'X-CSRF-Token': aCsrf }, body: 'x' });
  check(tokTrav.status === 404, 'path traversal in upload token refused');

  // Client tries admin actions (privilege escalation / mass assignment).
  const esc = [
    await api(A.page, '/admin', {}),
    await api(A.page, '/admin/settings', { method: 'POST', body: new URLSearchParams({ _csrf: aCsrf, action: 'token' }).toString(), headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),
    await api(A.page, '/admin/clients/1', { method: 'POST', body: new URLSearchParams({ _csrf: aCsrf, status: 'active', rate_pkr: '0' }).toString(), headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }),
  ];
  check(esc.every((r) => r.status === 403), 'client cannot use admin pages or actions (' + esc.map((r) => r.status).join(',') + ')');
  await A.page.goto(BASE + '/orders');
  await A.page.click('button:has-text("New video order")');
  const aOrder = A.page.url().split('/').pop();
  const tamper = await api(A.page, '/orders/' + aOrder + '/save', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ _csrf: aCsrf, title: 'x', length_sec: '10', rate: '0', estimate: '0', status: 'approved', user_id: '1', action: 'save' }).toString() });
  await A.page.reload();
  check((await A.page.textContent('[data-estimate-value]')).trim() === 'PKR 500', 'price cannot be tampered from the form (rate/estimate fields ignored)');

  // Malicious uploads.
  const mk = (name, data) => { const p = path.join(tmp, name); fs.writeFileSync(p, data); return p; };
  const png = fs.readFileSync(path.join(MEDIA, 'photo.png'));
  const bad = [
    mk('page.html', '<html><script>alert(1)</script></html>'),
    mk('shell.php', '<?php system($_GET["c"]); ?>'),
    mk('fake.jpg', '<html><body><script>alert(1)</script></body></html>'),
    mk('vector.svg', '<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>'),
    mk('double.php.png', Buffer.concat([Buffer.from('<?php echo 1; ?>'), png])),
    mk('app.apk', Buffer.concat([Buffer.from('PK\x03\x04'), Buffer.alloc(100)])),
  ];
  // Owner (2026-10-29): any file type is accepted, so dangerous files are stored but must never run or render.
  await A.page.setInputFiles('#pick', bad);
  await A.page.waitForFunction((n) => document.querySelectorAll('[data-file-list] li.done').length >= n, bad.length, { timeout: 30000 });
  await A.page.reload();
  const badIds = await A.page.evaluate(() => [...document.querySelectorAll('form[id^=del-]')].map((f) => f.id.slice(4)));
  let safe = badIds.length === bad.length;
  for (const id of badIds) {
    const r = await api(A.page, '/files/' + id, {});
    if (!(r.ct === 'application/octet-stream' && /^attachment/.test(r.cd || '') && r.nosniff === 'nosniff')) safe = false;
  }
  check(safe, 'HTML, PHP, fake JPG, SVG, PHP+PNG and APK uploads are stored only as plain downloads (octet-stream, attachment, nosniff)');
  for (const id of badIds) {
    await api(A.page, '/orders/' + aOrder + '/files/' + id + '/delete', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({ _csrf: aCsrf }).toString() });
  }
  // A polyglot that really is a PNG is stored, but is only ever served as image/png with nosniff.
  await A.page.reload();
  await A.page.setInputFiles('#pick', [mk('poly.png', Buffer.concat([png, Buffer.from('<script>alert(1)</script>')]))]);
  await A.page.waitForSelector('[data-file-list] li.done', { timeout: 20000 });
  await A.page.reload();
  const polyId = await A.page.evaluate(() => document.querySelector('form[id^=del-]').id.slice(4));
  const poly = await api(A.page, '/files/' + polyId, {});
  check(poly.ct === 'image/png', 'polyglot PNG is served as image/png only');
  const range = await api(A.page, '/files/' + polyId, { headers: { Range: 'bytes=999999999-' } });
  check(range.status === 416, 'out-of-range Range header -> 416');
  const big = await api(A.page, '/upload/init', { method: 'POST', headers: { 'X-CSRF-Token': aCsrf, 'Content-Type': 'application/json' },
    body: JSON.stringify({ order_id: Number(aOrder), name: 'huge.mp4', size: 999 * 1024 ** 4 }) });
  check(big.status === 400, 'file bigger than the limit refused at start');

  // Stored XSS: payloads in name, title, ideas, message, file name must not run for the client or the admin.
  await A.page.goto(BASE + '/orders/' + aOrder);
  await A.page.fill('input[name=title]', XSS);
  await A.page.fill('textarea[name=ideas]', XSS);
  await A.page.fill('input[name="q[brand]"]', XSS);
  await A.page.click('button[name=action][value=save]');
  await A.page.goto(BASE + '/orders');
  const adm = await browser.newContext();
  const ap = await adm.newPage();
  let admDialogs = 0;
  ap.on('dialog', (d) => { admDialogs++; d.dismiss(); });
  await ap.goto(BASE + '/login');
  await ap.fill('input[name=email]', 'owner@example.com');
  await ap.fill('input[name=password]', 'ownerpass123');
  await ap.click('button:has-text("Log in")');
  for (const u of ['/admin', '/admin/clients', '/admin/orders/' + aOrder, '/admin?status=draft']) await ap.goto(BASE + u);
  await A.page.goto(BASE + '/orders/' + aOrder);
  check(A.dialogs() === 0 && admDialogs === 0, 'stored XSS payloads never run (client pages and admin pages)');
  const html = await ap.content();
  check(!html.includes('<script>alert(2)</script>'), 'payloads are HTML-escaped in admin pages');

  // CSRF from another site: no token -> 403.
  const evil = await api(ap, '/admin/settings', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: 'action=token' });
  check(evil.status === 403, 'admin action without CSRF token -> 403');

  // Header injection through an email field.
  await ap.goto(BASE + '/admin/settings');
  await ap.fill('input[name=owner_email]', 'a@example.com\r\nBcc: victim@example.com');
  await ap.click('button:has-text("Save settings")');
  await ap.goto(BASE + '/admin/settings');
  check((await ap.inputValue('input[name=owner_email]')) === '', 'email header injection refused (invalid address not saved)');

  await browser.close();
  console.log(failures ? `${failures} FAILED` : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); process.exit(2); });
