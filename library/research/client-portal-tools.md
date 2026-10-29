# Client portal: tools and design research (2026-10-29)

Project: client portal (website + Android APK) on the owner's cPanel shared hosting, with a bridge to Claude
sessions. Branch `project-client-portal`, code in `portal/`.

## Owner's answers (AskUserQuestion, 2026-10-29)
- Hosting: cPanel shared (PHP + MySQL). Address: a subdomain. Storage / max upload size: "Pata nahi" (unknown).
- Payment methods: none shown. Owner: "yaha per serf paid clients honge inho ne pay ker diya hota hai"
  (only paid clients use it, they have already paid). So the portal shows a price estimate, no payment details.

## Tools the owner named
| Tool | Repo | Licence | Stars | Checked | Decision |
|---|---|---|---|---|---|
| UI UX Pro Max | github.com/nextlevelbuilder/ui-ux-pro-max-skill | MIT (LICENSE file, cloned 2026-10-29, head 28b3b8d 2026-10-26) | 140,410 (Exa search result 2026-10-29) | yes | USE: design rules/palettes for the portal UI. Skill = `.claude/skills/ui-ux-pro-max` (SKILL.md + data/ + scripts/search.py) |
| Agency Agents ("agent agency") | github.com/msitarzewski/agency-agents | MIT (LICENSE file, cloned 2026-10-29, head b37b5bb 2026-10-24) | not shown in the search result (unverified) | yes | USE a few personas as reference (engineering/, testing/, security/), not all |
| ECC, REA, Agent-Reach | already in repo (.claude/) | see tools-landscape.md | - | - | USE: security-review, e2e-testing, code-review, browser-qa |

Exa via agent-reach answered HTTP 429 (rate limit) after 2 searches on 2026-10-29.

## APK: TWA (Bubblewrap) chosen over Capacitor
- Capacitor `server.url` (load the live website in the app): its own config docs say "This is intended for use with
  live-reload servers. **This is not intended for use in production.**" (capacitorjs.com/docs/config, read with curl
  2026-10-29). A Capacitor app would need the whole UI bundled inside the APK and its own API client.
- Bubblewrap (github.com/GoogleChromeLabs/bubblewrap, Apache-2.0, README read 2026-10-29): "tools and libraries designed
  to help developers to create, build and update projects for Android Applications that launch Progressive Web App
  (PWA) using Trusted Web Activity (TWA)". Needs Node >= 18.
- So: one PHP website that is also a PWA (manifest + service worker), and a TWA APK that opens it. Same features in
  both, one codebase, updates on the site reach the app without a new APK.
- Local box (2026-10-29): PHP 8.3.6 with pdo_mysql, pdo_sqlite, fileinfo, mbstring; OpenJDK 21.0.12. No Android SDK yet.

## Bridge: portal -> Claude session (from the claude-code-remote tool descriptions, 2026-10-29)
- A web server cannot start a Claude turn by itself. `watch_url` webhooks are signed by a secret sealed for the
  artifact service only ("it cannot be read, used, or leaked from this conversation"), so PHP cannot call them.
- `create_trigger`: "Minimum interval is normally hourly (some projects allow shorter)". A scheduled task fires into
  a session; that session can curl the portal API (network is FULL) and forward orders with `send_message` to the
  client's session (`create_session` for a new client).
- So latency = up to the trigger interval (honest: up to ~1 hour), or immediately when the owner tells the hub
  session "portal check karo".
- API secret: stored as an environment variable in the cloud environment settings (read_documentation
  environment.secrets, 2026-10-29), never in git and never pasted in chat.

## Owner's hosting limits (owner message, 2026-10-29; not measured by us)
- Storage unlimited (6.5 GB used now); inodes and bandwidth unlimited.
- cPanel File Manager upload: no limit shown (a 49 MB file uploaded fine).
- Website forms (PHP): max 2 MB per file, 8 MB total per request.
- Real limits: 20 concurrent connections (entry processes; 11 in use when he checked), 1 GB RAM. The site's admin
  panel sometimes gave 503 because of the 20-connection limit.
- Design consequences: uploads go in 1.5 MB chunks (raw body, one chunk at a time per client), no long-polling,
  no websockets, static files cached by the PWA service worker, file downloads support HTTP Range.

## Native app (owner 2026-10-29: "web apk nhi real apk ... without internet bhi run")
- Capacitor 8.6.0 (@capacitor/core, cli, android: MIT; npm view 2026-10-29), plugins app 8.1.2, network 8.0.1,
  splash-screen 8.0.2, status-bar 8.0.4 (MIT). Live updates: @capgo/capacitor-updater 8.54.0 (MPL-2.0), manual mode
  (`autoUpdate: false`, `download()` + `next()`, `notifyAppReady()`), self-hosted bundle, `statsUrl: ""`.
- Generated project needs compileSdk 36 (installed platforms;android-36). Release APK 5.1 MB (measured 2026-10-29).
- Gradle: Maven Central (repo.maven.apache.org) answered 429 for netty jars (2026-10-29); an init script mapping it to
  maven-central.storage-download.googleapis.com fixed the build (portal/mobile/gradle-mirror.gradle).
- No /dev/kvm in this container (2026-10-29): the Android emulator runs only with `-accel off` (slow).
- Pentest (agency-penetration-tester agent, 2026-10-29, local copy): forged Host header reached password-reset emails
  (fixed: site_url from config); /register says "already exists" (account enumeration, low, rate-limited 5/h/IP, kept
  for usability). Everything else held (IDOR, CSRF, XSS, SQLi, uploads, Range, sessions, mass assignment).
