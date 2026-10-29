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
2. **Upload the files.** Make the upload zip here with `bash portal/make_zip.sh` (or download the release zip).
   cPanel → *File Manager* → your home folder (NOT inside `public_html`) → *Upload* `portal-upload.zip` →
   *Extract*. You now have `/home/<you>/portal/` with `app/`, `public/`, `storage/`.
   > Roman Urdu: zip ko public_html ke bahar upload kar ke extract karein, taake client files web se seedhi na khulein.
3. **Make the subdomain.** cPanel → *Domains* (or *Subdomains*) → create e.g. `portal.yourdomain.com` and set its
   **Document Root** to `portal/public`.
   > Roman Urdu: subdomain ka document root sirf `portal/public` hona chahiye.
4. **SSL.** cPanel → *SSL/TLS Status* → *Run AutoSSL* so the subdomain has https (the app needs it).
5. **PHP version.** cPanel → *Select PHP Version* (or *MultiPHP Manager*): PHP 8.1 or newer, with extensions
   `pdo_mysql`, `fileinfo`, `mbstring` ticked.
6. **Run the installer.** Open `https://portal.yourdomain.com/`. It asks for an *install key*: open
   `portal/storage/install-key.txt` in File Manager and copy the text. Fill in the database names, your admin email
   and password, and the brand name (e.g. MrCopper804). Press *Install*. It creates `portal/config.php` and the tables.
   > Roman Urdu: install key wali file sirf aap File Manager se dekh sakte hain, is liye koi aur install nahi kar sakta.
7. **Settings.** Log in → *Settings*: set PKR and USD rate per second, max file size. *Clients* page: special rate
   per client (empty = default rate).
8. **Bridge token.** *Settings* → *Make new token*. Copy it once. In Claude: cloud environment settings → add the
   secret / environment variable `PORTAL_BRIDGE_TOKEN` with that value and `PORTAL_URL=https://portal.yourdomain.com`.
   Never paste the token in chat or in git.
   > Roman Urdu: token sirf environment settings me daalein, chat me nahi.

## 2. Android app (APK)

The APK is a Trusted Web Activity: it opens the portal full screen, same features as the website.
Build (in a Claude session): `bash library/tools/setup-portal-dev.sh all`, then

```
node portal/apk/build_apk.js --manifest https://portal.yourdomain.com/manifest.webmanifest \
     --host portal.yourdomain.com --package com.mrcopper804.portal --version 1
```

It writes `portal/apk/build/<package>-v1.apk` and `portal/public/.well-known/assetlinks.json`. Upload that json to
`portal/public/.well-known/` on the host (it tells Android the app and site belong together; without it the app
shows a small address bar). Share the APK with clients (WhatsApp / your site). For a new version raise `--version`
and build with the same signing key (`/home/user/tools/portal-signing/`, keep a backup).

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
PORTAL=http://127.0.0.1:8088 MEDIA=<dir with test.mp4, fake.mp4, photo.png> SHOTS=<dir> NODE_PATH=$(npm root -g) node tests/e2e.js
```

`tests/e2e.js` runs the whole loop in Chromium plus the bridge CLI and the security checks (CSRF, other client's
files, admin role, bad token, storage not served, login rate limit).
