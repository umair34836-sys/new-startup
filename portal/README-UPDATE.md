# README UPDATE: update the live portal (keep all data)

For a person or an AI browser agent. This zip holds only program files (`portal/app`, `portal/public`).
It does NOT contain `portal/config.php` or `portal/storage`, so the database, settings, clients, orders and uploaded
files stay as they are.

Live site: `https://editor.firecraft.fun` · server folder: `/home/talkembe/editor.firecraft.fun/`

## Rules
- Do not delete or change `portal/config.php`, `portal/storage/` or anything outside `editor.firecraft.fun/`.
- Never type or copy passwords or tokens into a chat. Stop and let the owner type them.

## Steps
1. cPanel → File Manager → open `/home/talkembe/editor.firecraft.fun/`.
2. Upload `portal-update.zip` there. Right-click → **Extract** into the same folder (`/home/talkembe/editor.firecraft.fun/`).
   If File Manager asks, allow it to **overwrite** existing files.
3. Delete the uploaded `portal-update.zip` and this `README-UPDATE.md` from the server.
4. Open `https://editor.firecraft.fun/` once. The database upgrades itself on this first visit (nothing to click).
5. Log in as admin → **Settings**. Check the new "Currencies and default rates" table: PKR and USD keep the old rates.
   Add currencies the owner wants (3-letter code + rate per second, e.g. INR, NPR) → **Save settings**.
6. **Clients** page: each client has "Currency" and "Special rate per second" (empty = the currency's default). Ask the owner for
   the values, then press **Save** on each client row.
7. App screens update (live update), only if `bundle-*.zip` is included in this delivery:
   Settings → "Live update bundle" → upload the `bundle-x.y.z.zip (now bundle-1.0.2.zip, version 1.0.2)` → set "Live update version" to the same `x.y.z` and
   "Bundle needs app version at least" = `3` → **Save settings**. Phones download it by themselves and use it on the next start.
