# Client portal: architecture and the Claude bridge

## Pieces

```
Client (browser / Android app)
      │ HTTPS
      ▼
portal/public/index.php  ── PHP 8 + MySQL on the owner's cPanel (subdomain, document root = portal/public)
      │                     private files in portal/storage (outside the web root)
      │ /api/bridge/*  (Bearer token, only its sha256 is stored)
      ▼
Hub Claude session  ── scheduled task (hourly) runs portal_bridge.py events
      │ send_message / create_session
      ▼
Client's Claude session ── downloads inputs, edits with the repo skills, uploads the result with
                           portal_bridge.py deliver → the client sees the new version in the portal
```

- **Website + PWA**: one PHP app. `manifest.webmanifest` + `sw.js` make it installable; the service worker caches
  only CSS/JS/icons (fewer requests on a 20-connection host). Pages, files and the API are never cached.
- **Android APK**: a Trusted Web Activity built with Google's Bubblewrap core (`portal/apk/build_apk.js`). It opens
  the same website full screen, so website and app always have the same features. Full screen (no URL bar) needs
  `/.well-known/assetlinks.json` on the subdomain with the APK's signing fingerprint (the build script writes it).
  Why not Capacitor: its `server.url` (load a live site) is documented as "not intended for use in production"
  (library/research/client-portal-tools.md).

## Order life cycle

| Status (DB) | Client sees | Who moves it |
|---|---|---|
| draft | Draft | client fills the form, uploads files |
| submitted | Received | client presses Submit → event `order_submitted` |
| in_progress | In editing | bridge `take` on the event |
| delivered | Ready to review + "Koi changes chahiye?" | bridge `deliver` (or admin upload) → new version |
| revision | Changes requested | client sends changes → event `revision_requested` |
| approved | Approved | client presses "It's perfect" → event `approved` |

Every version (file), message and event is kept. Client messages on an open order create a `client_message` event.

## Uploads on a small shared host

The owner's host allows 2 MB per file / 8 MB per request in PHP forms, 20 connections and 1 GB RAM (owner,
2026-10-29). So files go in raw 1.5 MB chunks (`chunk_bytes()` = 75% of `post_max_size`, capped at 1.5 MB), one
chunk at a time, resumable (`offset` must match what the server has). On finish the server checks the real file
type with `finfo` against an extension allow-list, then moves it to `storage/files/<random name>`. Downloads go
through PHP after an ownership check and support HTTP Range (video seeking, resumable bridge downloads).

## The bridge (portal → Claude session)

A web server cannot start a Claude turn. What works with the tools this account has (claude-code-remote tool
descriptions, read 2026-10-29):

1. **Hub session** (this project session or the main session) owns a **scheduled task** (`create_trigger`, mode 1:
   fires into the hub session). The minimum interval is normally **hourly**, so a new order waits **up to ~1 hour**.
   The owner can say "portal check karo" to the hub session any time for an immediate run.
2. On each run the hub runs `PORTAL_URL=... PORTAL_BRIDGE_TOKEN=... python3 portal/bridge/portal_bridge.py events`.
   For each open event:
   - client has no linked session → `create_session` (new client session, repo + branch), then
     `portal_bridge.py link <client_id> <session_id>` so the portal remembers it (admin-only field);
   - `send_message` to that session with the order JSON (answers, script, ideas, file list, messages, versions);
   - `portal_bridge.py take <event_id>`.
3. The **client session** runs `portal_bridge.py download <order> <scratchpad dir>`, edits the video following
   CLAUDE.md (skills, edit log, no media in git), then `portal_bridge.py deliver <order> final.mp4 --note "..."`.
   Delivering closes the order's open events. For an `approved` event the session saves learnings and runs
   `portal_bridge.py done <event_id>`.
4. **White label**: the client only ever sees the brand name from Settings and "studio" messages. Session ids,
   event names and the bridge are visible only in the admin panel.

`watch_url` (instant webhook into a session) was ruled out: its signing secret is sealed for the artifact service
only, so PHP cannot sign a delivery.

## Secrets

- `config.php` (DB password) is written by the installer, chmod 600, git-ignored.
- Bridge token: made in Admin → Settings (shown once). The portal stores only `sha256(token)`. In Claude it goes into
  the cloud environment settings as the secret/env var `PORTAL_BRIDGE_TOKEN` (never in git, never in chat).
- APK signing key: `/home/user/tools/portal-signing/` (outside git). Keep a copy: every app update must be signed
  with the same key.

## Security checklist (tested in tests/e2e.js)

Passwords: Argon2id (bcrypt fallback), timing-safe login. Sessions: HttpOnly, SameSite=Lax, Secure on HTTPS,
regenerated on login. CSRF token on every POST (403 without). Rate limits: login 10 / 15 min / IP, signup 5 / h / IP,
bridge auth failures 20 / 15 min / IP. Strict CSP (no inline script), X-Frame-Options DENY, nosniff. Files: allow-list
+ content check, random stored names, outside web root, `Require all denied` in storage/ and app/, ownership check on
every download (another client gets 404). Admin pages need role admin (403). Prepared statements everywhere.
