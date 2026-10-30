// Drives the real APK inside an Android emulator: WebView over Chrome DevTools (test build with WEBDEBUG=1),
// network switched off/on with adb, screenshots with adb screencap.
// Needs: emulator running, emulator test APK installed and open, portal on the host at :8088 (SITE_URL=http://10.0.2.2:8088).
// Run: MEDIA=<dir> SHOTS=<dir> PORTAL=http://127.0.0.1:8088 NODE_PATH=$(npm root -g) node tests/emulator_test.js
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ADB = '/home/user/tools/android-sdk/platform-tools/adb';
const BASE = process.env.PORTAL || 'http://127.0.0.1:8088';
const MEDIA = process.env.MEDIA;
const SHOTS = process.env.SHOTS || '/tmp';
const BRIDGE = path.join(__dirname, '..', 'bridge', 'portal_bridge.py');
const env = { ...process.env, PORTAL_URL: BASE, PORTAL_BRIDGE_TOKEN: 'pb_testtoken', NO_PROXY: '127.0.0.1,localhost', no_proxy: '127.0.0.1,localhost' };
let failures = 0;
function check(c, m) { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) failures++; }
function adb(...a) { return execFileSync(ADB, ['-s', 'emulator-5554', ...a], { encoding: 'utf8' }); }
function bridge(...a) { return JSON.parse(execFileSync('python3', [BRIDGE, ...a], { env, encoding: 'utf8' })); }
function screencap(name) { fs.writeFileSync(path.join(SHOTS, 'emu-' + name + '.png'), execFileSync(ADB, ['-s', 'emulator-5554', 'exec-out', 'screencap', '-p'], { maxBuffer: 64 << 20 })); }
function net(on) { adb('shell', 'svc', 'wifi', on ? 'enable' : 'disable'); adb('shell', 'svc', 'data', on ? 'enable' : 'disable'); }
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const file = (n, t) => ({ name: n, mimeType: t, buffer: fs.readFileSync(path.join(MEDIA, n)) });

(async () => {
  const pid = adb('shell', 'pidof', 'com.mrcopper804.portal').trim();
  check(!!pid, 'app process runs on Android (pid ' + pid + ')');
  execFileSync(ADB, ['-s', 'emulator-5554', 'forward', 'tcp:9333', 'localabstract:webview_devtools_remote_' + pid]);
  const browser = await chromium.connectOverCDP('http://127.0.0.1:9333', { timeout: 120000 });
  const page = browser.contexts()[0].pages().find((p) => /localhost/.test(p.url())) || browser.contexts()[0].pages()[0];
  page.setDefaultTimeout(120000);
  check(page.url().startsWith('https://localhost/'), 'screens load from inside the APK (' + page.url() + ')');
  check(await page.evaluate(() => !!(window.Capacitor && window.Capacitor.isNativePlatform())), 'Capacitor native bridge is active');
  const plugins = await page.evaluate(() => Object.keys(window.Capacitor.Plugins));
  check(['App', 'Network', 'CapacitorUpdater', 'SplashScreen'].every((p) => plugins.includes(p)), 'native plugins present: App, Network, CapacitorUpdater, SplashScreen');
  screencap('01-start');

  // Register.
  await page.evaluate(() => { location.hash = '#/register'; });
  await page.waitForSelector('input[name=name]');
  await page.fill('input[name=name]', 'Emulator Client');
  await page.fill('input[name=email]', 'emu' + Date.now() + '@example.com');
  await page.fill('input[name=password]', 'emupass1234');
  await page.click('button:has-text("Create account")');
  await page.waitForFunction(() => localStorage.getItem('token'));
  check(true, 'register on the phone works against the portal API');
  screencap('02-orders');

  // Order with files.
  await page.evaluate(() => { location.hash = '#/new'; });
  await page.waitForSelector('#pick', { state: 'attached' });
  await page.setInputFiles('#pick', [file('photo.png', 'image/png'), file('test.mp4', 'video/mp4')]);
  await page.waitForSelector('#files li >> nth=1');
  await page.fill('input[name=title]', 'Emulator order');
  await page.fill('#len', '20');
  for (const [k, v] of [['video_type', 'Promo / Ad'], ['platform', 'TikTok'], ['aspect', '9:16 vertical (phone)'], ['style', 'Cinematic'], ['sound', 'You decide']]) {
    await page.selectOption(`select[name="q.${k}"]`, v);
  }
  screencap('03-new-order');
  await page.click('button:has-text("Submit order")');
  let ev = null;
  for (let i = 0; i < 60 && !ev; i++) {
    await sleep(3000);
    ev = bridge('events').events.find((e) => e.order.title === 'Emulator order');
  }
  check(!!ev, 'order with photo + video uploaded from the phone and submitted');
  check(ev && ev.order.files.some((f) => f.size === fs.statSync(path.join(MEDIA, 'test.mp4')).size), 'video arrived byte-exact');

  // Delivery, watch, save offline.
  bridge('deliver', String(ev.order.id), path.join(MEDIA, 'test.mp4'), '--note', 'Version 1 for the phone.');
  await page.evaluate((id) => { location.hash = '#/order/' + id; }, ev.order.id);
  await page.waitForSelector('#player');
  await page.click('#save-off');
  await page.waitForSelector('text=Saved on this phone', { timeout: 180000 });
  check(true, 'video saved on the phone');
  screencap('04-version-saved');

  // Real offline: Wi-Fi and mobile data off.
  net(false);
  await sleep(8000);
  check(await page.evaluate(() => !document.getElementById('netbar').hidden), 'app notices it is offline (native Network plugin)');
  await page.evaluate(() => { location.hash = '#/orders'; });
  await sleep(1500);
  await page.evaluate((id) => { location.hash = '#/order/' + id; }, ev.order.id);
  await page.waitForSelector('#player');
  await sleep(1500);
  check((await page.getAttribute('#player', 'src')).startsWith('blob:'), 'offline: video plays from the phone');
  await page.fill('#fc textarea', 'Changed my mind offline: shorter intro.');
  await page.click('button:has-text("Send changes")');
  await sleep(1500);
  screencap('05-offline');
  check((await page.textContent('#main')).includes('will be sent when you are online'), 'offline: change request waits on the phone');

  net(true);
  let sent = false;
  for (let i = 0; i < 40 && !sent; i++) {
    await sleep(3000);
    sent = bridge('order', String(ev.order.id)).order.messages.some((m) => m.body.includes('shorter intro'));
  }
  check(sent, 'change request sent by itself when the network came back');
  screencap('06-back-online');

  // App restart keeps the login.
  adb('shell', 'am', 'force-stop', 'com.mrcopper804.portal');
  adb('shell', 'monkey', '-p', 'com.mrcopper804.portal', '-c', 'android.intent.category.LAUNCHER', '1');
  await sleep(20000);
  screencap('07-restart-splash');
  await browser.close().catch(() => {});
  console.log(failures ? `${failures} FAILED` : 'ALL PASSED');
  process.exit(failures ? 1 : 0);
})().catch((e) => { console.error(e); try { net(true); } catch (x) {} process.exit(2); });
