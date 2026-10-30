// Builds the Android app (Trusted Web Activity) that opens the portal website, with Google's Bubblewrap core.
// Needs: bash library/tools/setup-portal-dev.sh all  (Android SDK + JDK)  and  npm i @bubblewrap/core in /home/user/tools/bubblewrap
//
//   node portal/apk/build_apk.js --manifest http://127.0.0.1:8088/manifest.webmanifest \
//        --host portal.example.com --package com.example.portal [--version 1]
//
// --manifest: any running copy of the portal (icons are read from it); --host: the real subdomain the app opens.
// The signing key lives OUTSIDE git in /home/user/tools/portal-signing (keep a copy: every app update must use it).
// Output: portal/apk/build/<package>-v<version>.apk and portal/public/.well-known/assetlinks.json.
const path = require('path');
const fs = require('fs');
const { execFileSync } = require('child_process');
const crypto = require('crypto');

const BW = process.env.BUBBLEWRAP_DIR || '/home/user/tools/bubblewrap';
const { TwaManifest, TwaGenerator, ConsoleLog } = require(path.join(BW, 'node_modules/@bubblewrap/core'));

const SDK = process.env.ANDROID_HOME || '/home/user/tools/android-sdk';
const BT = path.join(SDK, 'build-tools/35.0.0');
const KEYDIR = process.env.PORTAL_SIGNING_DIR || '/home/user/tools/portal-signing';
const OUT = path.join(__dirname, 'build');

function arg(name, def) {
  const i = process.argv.indexOf('--' + name);
  return i > -1 ? process.argv[i + 1] : def;
}
function run(cmd, args, opts = {}) {
  console.log('$ ' + cmd + ' ' + args.join(' ').replace(/(pass:|-storepass |-keypass )\S+/g, '$1***'));
  return execFileSync(cmd, args, { stdio: 'inherit', ...opts });
}

(async () => {
  const manifestUrl = arg('manifest');
  const host = arg('host');
  const pkg = arg('package');
  const version = parseInt(arg('version', '1'), 10);
  if (!manifestUrl || !host || !pkg) throw new Error('Need --manifest, --host and --package');

  // 1. Signing key (created once, reused for every update).
  fs.mkdirSync(KEYDIR, { recursive: true, mode: 0o700 });
  const ks = path.join(KEYDIR, 'portal.jks');
  const passFile = path.join(KEYDIR, 'portal.pass');
  if (!fs.existsSync(passFile)) fs.writeFileSync(passFile, crypto.randomBytes(18).toString('base64url'), { mode: 0o600 });
  const pass = fs.readFileSync(passFile, 'utf8').trim();
  if (!fs.existsSync(ks)) {
    run('keytool', ['-genkeypair', '-keystore', ks, '-alias', 'portal', '-keyalg', 'RSA', '-keysize', '2048', '-validity', '10000',
      '-storepass', pass, '-keypass', pass, '-dname', 'CN=Portal App']);
  }
  const certInfo = execFileSync('keytool', ['-list', '-v', '-keystore', ks, '-alias', 'portal', '-storepass', pass], { encoding: 'utf8' });
  const sha256 = (certInfo.match(/SHA256:\s*([0-9A-F:]+)/) || [])[1];

  // 2. TWA project from the portal's web manifest (Bubblewrap template).
  const twa = await TwaManifest.fromWebManifest(manifestUrl);
  twa.host = host;
  twa.packageId = pkg;
  twa.startUrl = '/orders?src=twa&v=' + version; // the site remembers the installed version for the update bar
  twa.appVersionCode = version;
  twa.appVersionName = String(version);
  twa.signingKey = { path: ks, alias: 'portal' };
  twa.fallbackType = 'customtabs';
  twa.minSdkVersion = 24; // androidbrowserhelper 2.7.4 declares minSdk 24 (Gradle manifest merger error, 2026-10-29)
  twa.enableNotifications = false;
  const proj = path.join(OUT, 'project');
  fs.rmSync(proj, { recursive: true, force: true });
  fs.mkdirSync(proj, { recursive: true });
  await new TwaGenerator().createTwaProject(proj, twa, new ConsoleLog('bubblewrap'));
  fs.writeFileSync(path.join(proj, 'local.properties'), 'sdk.dir=' + SDK + '\n');
  // The template still lists jcenter() (shut down); Maven Central answered 429 from this container (2026-10-29).
  // Google's Maven Central mirror answered 200, so use it instead.
  const bg = path.join(proj, 'build.gradle');
  fs.writeFileSync(bg, fs.readFileSync(bg, 'utf8').replace(/jcenter\(\)/g,
    "maven { url 'https://maven-central.storage-download.googleapis.com/maven2/' }"));

  // 3. Build, align, sign.
  run('bash', ['./gradlew', '--no-daemon', '-q', 'assembleRelease'], { cwd: proj, env: { ...process.env, ANDROID_HOME: SDK } });
  const unsigned = path.join(proj, 'app/build/outputs/apk/release/app-release-unsigned.apk');
  const aligned = path.join(OUT, 'aligned.apk');
  const apk = path.join(OUT, `${pkg}-v${version}.apk`);
  run(path.join(BT, 'zipalign'), ['-f', '-p', '4', unsigned, aligned]);
  run(path.join(BT, 'apksigner'), ['sign', '--ks', ks, '--ks-key-alias', 'portal', '--ks-pass', 'pass:' + pass, '--key-pass', 'pass:' + pass, '--out', apk, aligned]);
  run(path.join(BT, 'apksigner'), ['verify', apk]);
  fs.rmSync(aligned);

  // 4. Digital Asset Links: lets Android open the site full screen (no URL bar) inside the app.
  const wk = path.join(__dirname, '..', 'public', '.well-known');
  fs.mkdirSync(wk, { recursive: true });
  fs.writeFileSync(path.join(wk, 'assetlinks.json'), JSON.stringify([{
    relation: ['delegate_permission/common.handle_all_urls'],
    target: { namespace: 'android_app', package_name: pkg, sha256_cert_fingerprints: [sha256] },
  }], null, 2) + '\n');
  console.log('APK: ' + apk + '\nSHA256: ' + sha256);
})().catch((e) => { console.error(e); process.exit(1); });
