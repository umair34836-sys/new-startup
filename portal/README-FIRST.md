# README FIRST: install the MrCopper804 client portal on cPanel

This zip holds the client portal (website + admin panel + the API used by the Android app).
These steps are written so that a person or an AI browser agent (for example a Chrome-extension agent) can follow
them one by one in cPanel. Do them in order. Each step says what to check before going on.

> Roman Urdu: ye file zip ke saath hai. Isme cPanel par upload aur uske baad ka poora setup step by step likha hai.

## Facts you need

| Item | Value |
|---|---|
| Website address | `https://editor.firecraft.fun` (a subdomain of firecraft.fun) |
| Folder to create on the server | `portal` in the cPanel **home folder**, NOT inside `public_html` |
| Document root of the subdomain | `portal/public` |
| Database | MySQL / MariaDB, created in cPanel |
| PHP | 8.1 or newer, with `pdo_mysql`, `fileinfo`, `mbstring` |
| Brand name | `MrCopper804` |

## Rules for the agent (safety)

- Do NOT change, move or delete anything that already exists (the FireCraft site in `public_html`, other domains,
  databases, emails). Only create the new things listed here.
- Do NOT upload this zip into `public_html`. Client files must stay outside the public web folder.
- Passwords: the owner types them or chooses them; write them only into the cPanel/installer fields that ask for them.
  Never paste a password, the install key or the bridge token into a chat, a ticket or any other website.
- If a screen looks different from these steps (cPanel themes differ a little between hosts), stop and ask the owner
  instead of guessing.

## Step 1: Make the database (cPanel → "MySQL Database Wizard")

1. Database name: `portal` (cPanel shows it as `<cpaneluser>_portal`). Next.
2. Database user: `portal` (shown as `<cpaneluser>_portal`), a strong password (use the password generator; the owner
   saves it). Next.
3. Privileges: tick **ALL PRIVILEGES**. Next.
4. Write down the full names exactly as cPanel shows them: database name, user name. Password: the owner keeps it.

Check: cPanel → "MySQL Databases" lists the new database with the user under "Privileged Users".

## Step 2: Upload and extract (cPanel → "File Manager")

1. Open File Manager in the **home folder** (`/home/<cpaneluser>`; the folder that contains `public_html`).
2. Upload `portal-upload.zip` (it is small, well under the host's upload limit).
3. Right-click the zip → **Extract** → into the home folder. This creates `/home/<cpaneluser>/portal/` with the
   folders `app`, `public`, `storage`, and the files `README.md`, `ARCHITECTURE.md`, `config.example.php`.
4. Delete the uploaded zip file (only the zip).
5. File Manager → Settings → tick "Show Hidden Files (dotfiles)". Check that `portal/public/.htaccess`,
   `portal/app/.htaccess`, `portal/storage/.htaccess`, `portal/.htaccess` and `portal/public/.well-known/` exist.
6. Permissions: `portal/storage` (and its subfolders) must be writable by PHP: 755 for folders is normal on
   cPanel (PHP runs as your user). The `portal` folder itself must also be writable (the installer creates
   `portal/config.php` there).

## Step 3: Make the subdomain (cPanel → "Domains" or "Subdomains")

1. Create the domain/subdomain `editor.firecraft.fun`.
2. If there is a "Share document root" option, turn it **off**.
3. Document root: `portal/public` (full path `/home/<cpaneluser>/portal/public`).
4. Save. Check: the domain list shows `editor.firecraft.fun` with document root `/portal/public`.

If firecraft.fun's DNS is not managed by this cPanel, the owner must add an A record for `editor` pointing to this
server's IP (cPanel → "Zone Editor" if it is managed here; it usually is created automatically).

## Step 4: HTTPS (cPanel → "SSL/TLS Status")

Tick `editor.firecraft.fun` → **Run AutoSSL**. Wait until it shows a valid certificate (can take a few minutes
after the subdomain is created). The app and the login need https.

## Step 5: PHP version and extensions

- cPanel → "MultiPHP Manager": set `editor.firecraft.fun` to PHP **8.1, 8.2 or 8.3**.
- cPanel → "Select PHP Version" (if the host has it): make sure `pdo_mysql`, `fileinfo`, `mbstring` are ticked.

## Step 6: Run the installer (browser)

1. Open `https://editor.firecraft.fun/`. The "Install the portal" page shows green ticks for PHP and folders.
   If a tick is red, fix that first (PHP version, extension, or folder permission).
2. Install key: File Manager → open `portal/storage/install-key.txt` → copy the text into the "Install key" field.
3. Fill in:
   - Host: `localhost`; database name, database user, password from Step 1;
   - Admin name, admin email and admin password (the owner chooses them);
   - Brand name: `MrCopper804`;
   - Site address: `https://editor.firecraft.fun`.
4. Press **Install**. Expected: "Done. The portal is installed." The installer writes `portal/config.php`
   (permissions 600) and deletes the install key file.

Check: `https://editor.firecraft.fun/` now shows the home page with the MrCopper804 splash and "Create account".

## Step 7: First settings (log in → "Settings")

Log in at `https://editor.firecraft.fun/login` with the admin account, open **Settings**:
1. **Rates:** PKR per second and USD per second (the owner gives the numbers). Save.
2. **Emails:** first create a mailbox in cPanel → "Email Accounts", e.g. `no-reply@firecraft.fun` (any strong password,
   nobody needs to log in to it). Then in Settings: "Send emails from" = `no-reply@firecraft.fun`,
   "Your email for new-order alerts" = the owner's email. Save.
3. **Android app:** "Published app version" = `3` (the APK in this zip is version 3). Save.
   Check: `https://editor.firecraft.fun/app/download` downloads `MrCopper804-v3.apk`, and the home page shows
   "Get the Android app".
4. Leave "New accounts" on "Open for everyone" (owner's choice) unless the owner says otherwise.

## Step 8: Cron job (cPanel → "Cron Jobs")

Common setting: **Once Per Hour**. Command (replace `<cpaneluser>`):

```
php /home/<cpaneluser>/portal/app/cron.php >/dev/null 2>&1
```

It cleans unfinished uploads, old rate-limit rows, expired reset links and old sessions.

## Step 9: Quick test (browser)

1. Open `https://editor.firecraft.fun/` in a private window → Create account (a test client) → New video order →
   upload one small photo → fill the form → Submit. Expected: "Order sent!".
2. As admin: Orders shows the test order. Open it, check the file downloads.
3. Forgot password with the test client's email: an email arrives (check spam the first time).
4. On an Android phone: open `https://editor.firecraft.fun/app/download`, install the app, log in with the test
   client, open the order.

## Step 10: Connect Claude (the owner does this, not the browser agent)

1. Admin → Settings → "Claude bridge token" → **Make new token**. It is shown once.
2. The owner puts it into the Claude cloud environment settings as the secret / environment variable
   `PORTAL_BRIDGE_TOKEN`, plus `PORTAL_URL=https://editor.firecraft.fun`. Never paste it into a chat.
3. Then tell Claude "portal ready hai": Claude sets up the hourly order check (see portal/ARCHITECTURE.md).

## Step 11: Clean up (after everything works)

The guides describe how the work behind the portal is organised. Clients can never open them (they are outside the
public folder), but keep the server clean anyway: File Manager → delete `README-FIRST.md` (home folder),
`portal/README.md`, `portal/ARCHITECTURE.md` and `portal/config.example.php`. Keep a copy of this zip on the
owner's computer.

> Roman Urdu: setup ke baad ye guide files server se hata dein; client ko sirf ye dikhta hai ke MrCopper804 khud haath se edit karta hai.

## If something goes wrong

| Symptom | Fix |
|---|---|
| Installer shows a red tick for "portal folder is writable" | File Manager → `portal` → Permissions 755 (owner must be your cPanel user) |
| "500 Internal Server Error" | MultiPHP Manager: PHP 8.1+; check cPanel → "Errors" for the exact message |
| Home page shows a file list or "Index of" | Document root is wrong: it must be `portal/public`, not `portal` |
| Pages other than the home page give 404 | `portal/public/.htaccess` is missing (dotfiles hidden during upload): re-extract the zip |
| No emails arrive | Settings → "Send emails from" must be a real mailbox of firecraft.fun (Step 7.2); check spam |
| Big video uploads stop | Normal uploads go in 1.5 MB parts and resume by themselves; check the internet, then retry |
| Admin panel slow / 503 at busy times | The plan allows 20 connections at once; uploads already go one part at a time |

More detail: `portal/README.md` (all features), `portal/ARCHITECTURE.md` (how orders reach Claude, security).
