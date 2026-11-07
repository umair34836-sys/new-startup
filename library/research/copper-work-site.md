# copper_work (plugin.firecraft.fun): facts read from the site, 2026-11-07

Source: web_capture.py of https://plugin.firecraft.fun, /docs, /download, /signup, /login (read 2026-11-07), plus the
owner's demo panel (logged in with the owner's permission, read-only). The owner's own product.
- Tagline: "Your Minecraft servers, one panel, any AI." Outbound-only plugin, no open port (polls the panel over HTTPS).
- Free plan, no card: two servers per account, as many AI keys as you like; Discord bots and staff accounts included.
- Features (home page): Live console; Status and players (TPS, memory, who is online; message when offline / low TPS);
  Pictures of the world (camera shot or map from above of any loaded area, rendered on the server); Your own AI key
  (17 providers, many with a free tier; AI runs commands, manages Discord, answers players); One Claude connector;
  Discord bots and staff (chat relay, welcome messages, status card, staff roles).
- Safety (docs): risky commands wait for Confirm, blocked commands never run, every action in the audit log; two-factor
  login with 8 recovery codes, device list, new-login e-mail, JSON export, account deletion.
- Alerts by e-mail, Discord bot channel or webhook; scheduled tasks every N minutes / daily / weekly (UTC).
- Setup: Add server -> copy key; copper_work.jar in plugins/ + restart; `copper link <key>` -> Connected.
- Plugin v0.2.0 (15882 KB): Paper, Purpur or Spigot 1.20 - 26.x, Java 17+. Android app v0.1.0 (76.3 MB), Android 7+.
- Site CSS tokens (dark): bg #181818, panel #1f1f1f, text #f2efe8, muted #9a978f, copper #c9a35a, ok #4fd1a1;
  fonts Geist / Geist Mono (assets/fonts/geist*.woff2).
