# Client portal (website + Android app)

Clients make an account, upload raw videos / images / script, answer a short questionnaire, add their ideas and
submit. The finished video appears in their account; they can ask for changes until they press "It's perfect".
The owner sets per-second rates (PKR / USD, also per client) in the admin panel. Orders reach Claude sessions
through the bridge (see ARCHITECTURE.md). Stack: PHP 8.1+ and MySQL, no Composer, made for cPanel shared hosting.

> Roman Urdu: ye portal aap ki cPanel hosting par chalta hai. Neeche wale steps ek dafa karne hain.

## 1. Install on cPanel (once)

1. **Make the database.** cPanel → *MySQL Databases*: create a database, a user with a strong password, and add the
   user to the database with *ALL PRIVILEGES*. Note the three names (cPanel adds your username in front).
   > Roman Urdu: database, user aur password bana kar likh lein.
2. **Upload the files.** Make the upload zip here with `bash portal/make_zip.sh` (it puts README-FIRST.md, the step-by-step cPanel guide, at the top of the zip, and the latest APK in storage/app).
   cPanel → *File Manager* → your home folder (NOT inside `public_html`) → *Upload* `portal-upload.zip` →
   *Extract*. You now have `/home/<you>/portal/` with `app/`, `public/`, `storage/`.
   > Roman Urdu: zip ko public_html ke bahar upload kar ke extract karein, taake client files web se seedhi na khulein.
3. **Make the subdomain.** cPanel → *Domains* (or *Subdomains*) → create e.g. `editor.firecraft.fun` and set its
   **Document Root** to `portal/public`.
   > Roman Urdu: subdomain ka document root sirf `portal/public` hona chahiye.
4. **SSL.** cPanel → *SSL/TLS Status* → *Run AutoSSL* so the subdomain has https (the app needs it).
5. **PHP version.** cPanel → *Select PHP Version* (or *MultiPHP Manager*): PHP 8.1 or newer, with extensions
   `pdo_mysql`, `fileinfo`, `mbstring` ticked.
6. **Run the installer.** Open `https://editor.firecraft.fun/`. It asks for an *install key*: open
   `portal/storage/install-key.txt` in File Manager and copy the text. Fill in the database names, your admin email
   and password, the brand name (MrCopper804) and the *Site address* (`https://editor.firecraft.fun`, used in email
   links). Press *Install*. It creates `portal/config.php` and the tables.
   > Roman Urdu: install key wali file sirf aap File Manager se dekh sakte hain, is liye koi aur install nahi kar sakta.
7. **Settings.** Log in → *Settings*: set PKR and USD rate per second, max file size and storage per client.
   *Clients* page: special rate per client (empty = default rate). Signup is open; *New accounts* can be switched to
   "Wait for my approval".
8. **Emails** (password reset, "your video is ready", new-order alerts to you): cPanel → *Email Accounts* → create
   e.g. `no-reply@firecraft.fun`. Put it in Settings → *Send emails from*, and your own address in *Your email for
   new-order alerts*. Empty = no emails (password reset then needs you).
   > Roman Urdu: email ke liye cPanel me ek no-reply email bana kar Settings me daal dein.
9. **Cron job** (cleanup): cPanel → *Cron Jobs* → *Once Per Hour* → command
   `php /home/<you>/portal/app/cron.php >/dev/null 2>&1`.
10. **Bridge token.** *Settings* → *Make new token*. Copy it once. In Claude: cloud environment settings → add the
   secret / environment variable `PORTAL_BRIDGE_TOKEN` with that value and `PORTAL_URL=https://editor.firecraft.fun`.
   Never paste the token in chat or in git.
   > Roman Urdu: token sirf environment settings me daalein, chat me nahi.

## 2. Android app (native, works offline)

The app in `portal/mobile/` is a real Android app (Capacitor 8): all its screens are inside the APK, and it only
talks to the portal for data (`/api/v1`). Without internet it still opens and works:
- login is remembered, orders, messages and versions open from the phone's copy;
- videos saved with "Save for offline" play from the phone;
- new orders (with their files), change requests and messages are kept on the phone and sent by themselves when
  the internet is back (while the app is open).
Uploading and receiving videos itself needs internet (the files live on your hosting).

Build (in a Claude session, after `bash library/tools/setup-portal-dev.sh all`):

```
CODE=2 NAME=2.0 API=https://editor.firecraft.fun bash portal/mobile/build_apk.sh
```

It signs with the same key as before (`/home/user/tools/portal-signing/`, keep the owner's backup), so it installs
as an update over older versions. Share the APK with clients, or upload it in Admin → Settings → *App file (APK)*
(public link `https://editor.firecraft.fun/app/download`, also shown on the home page).

**Updates without reinstalling (live update / OTA):**
- New screens or features (anything in `portal/mobile/src`): `VERSION=1.0.1 bash portal/mobile/build_bundle.sh`,
  then Admin → Settings → *Live update bundle* → upload `bundle-1.0.1.zip`, set *Live update version* = `1.0.1`,
  save. Every app downloads it by itself (checksum checked) and uses it on the next start.
- Native changes only (icon, app name, new plugins): build a new APK with a higher `CODE`, upload it and raise
  *Published app version*: apps show "New app version · Update".
> Roman Urdu: screens/features ki tabdeeli "live update" se khud phones tak pahunch jati hai; sirf icon/naam/plugin
> badalne par nayi APK chahiye.

The older TWA build (`portal/apk/build_apk.js`, opens the website inside the app) is kept as a fallback.

## Updating the live site

`bash portal/make_update_zip.sh` makes `portal-update.zip`: program files only (no config.php, no storage) with
`README-UPDATE.md` (steps for a person or an AI browser agent). Extract it over `/home/talkembe/editor.firecraft.fun/`;
the database upgrades itself on the next page load (`upgrade_db()`, schema version in Settings).

## Currencies and rates

Settings → "Currencies and default rates": any 3-letter code (PKR, INR, NPR, USD, AED, ...) with a default rate per
second. Clients page: each client's currency and an optional special rate in that currency. Orders keep the
currency and rate they were made with.

## 3. Daily use

- Client: *Create account* → *New video order* → upload → answers → *Submit*. Later: watch, *Send changes* or
  *It's perfect, approve*.
- Owner: *Orders* (filter by status), open an order to see files, answers, messages, bridge events; upload a
  finished file yourself and press *Send to client as new version*; set the final price.
- Claude: see ARCHITECTURE.md "The bridge". New orders reach the client's session within about an hour, or right
  away when you tell the hub session "portal check karo".

## 4. Develop and test here

```
DIR=/tmp/portal-test tests/dev_server.sh            # SQLite copy on http://127.0.0.1:8088 (owner@example.com / ownerpass123)
DIR=/tmp/portal-test APK=portal/apk/build/<apk> PORTAL=http://127.0.0.1:8088 MEDIA=<dir with test.mp4, fake.mp4, photo.png> SHOTS=<dir> NODE_PATH=$(npm root -g) node tests/e2e.js
PORTAL=http://127.0.0.1:8088 MEDIA=<dir> NODE_PATH=$(npm root -g) node tests/attack.js   # on a fresh copy
```

`tests/app_e2e.js` tests the native app's screens in Chromium (serve `portal/mobile/www` built with
`API=http://127.0.0.1:8088 bash portal/mobile/build_www.sh` on port 8091), including offline orders, offline video
and offline change requests.
`tests/attack.js` runs attacker-view checks (SQLi, stored XSS, IDOR between clients, privilege escalation, CSRF,
malicious uploads, session fixation, header injection, security headers). Run it on a fresh copy (login limits).
`tests/e2e.js` runs the whole loop in Chromium plus the bridge CLI and the security checks (CSRF, other client's
files, admin role, bad token, storage not served, login rate limit).
