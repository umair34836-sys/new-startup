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

## In-game demo recording (owner's Drive, watched here 2026-11-16)

Source: Drive folder `1tNTNi-0FwoKiZxipoxBHaxUojijYW_ZH` (owner's). Media is NOT in git; re-download by ID.
- Recording `1RfkohbEgSId_edoScEpohx1KnPs76mVN`: 1,555,393,200 bytes, 34 min 17.9 s, 1280x720, 60 fps, h264 + aac
  (ffprobe here 2026-11-16). Download: `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"`.
- Proof screenshot `1fsiit8tfHYwEvhH6pdUmUKHjR_9skAgj` (1280x768 PNG): Discord channel `smp-announcements`,
  bot post "PvP EVENT - Tomorrow 10:00 AM", 16 Nov 2026 12:56 PM. The embed text shows literal `\n\n` (not line breaks).

What the recording shows (read from frames every 6 s + full-size chat crops): the owner types a chat line that
starts with "server ...", a whisper answers "Sir I am working on it: ..." and later "Sir done: ...", and the
result is visible in the world. Times are in the source file.

| # | Clip (s in source) | Owner asked (short) | Reply read on screen |
|---|---|---|---|
| 01 | 0-96 | "server can you here me ?" | "Sir yes I can hear you, watcher is active and checking every minute." |
| 02 | 90-246 | tp to spawn, owner armour, status + players list | "Sir done: tp spawn done, owner netherite armour equipped. Status: TPS 20.0, 1/20 players online" |
| 03 | 240-672 | flatten this area to spawn level, look up Pakistan's best building and build it | "Sir done: area flattened to spawn surface + built Faisal Mosque-inspired monument ... 4 minarets" |
| 04 | 684-912 | video studio with a green screen area, full detailing | "Sir done: video studio built at your spot - green screen room ..., control room with observation window, camera tripod, director's chair, desk." |
| 05 | 908-1026 | more detailing and professionalism in the studio | "Sir done: studio detailing added - soundproof wall panels, dual monitors+jukebox mixer at desk, 2 director chairs, 3-point lighting rig in green room, floor mark, ON AIR sign+lamp, reception plants." |
| 06 | 1018-1130 | tp me to the player base that is the fullest | "Sir done: checked block counts - ... base has the most built (56065 blocks) ... TP'd you there." |
| 07 | 1090-1368 | Discord announcement for a PvP event tomorrow 10 am, schedule it in Discord and Minecraft, build the arena, report results | "Sir correction: DC announcement posted in smp-announcements (everyone pinged). PvP Arena built at 430,63,40. Event auto-runs tomorrow 10am PKT, results will be reported." |
| 08 | 1360-1416 | tp me to the PvP arena | "Sir done: tp'd to PvP arena (430,63,40)" |
| 09 | 1408-1756 | underground train tunnel spawn -> arena, arena details; protect arena from mobs | "Sir done: underground minecart metro spawn-to-arena (powered rails, lit tunnel) + arena detailed with cover pillars, torch-lit walls, center marker, minecarts at both stations." |
| 10 | 1640-1986 | move the tunnel entrance to a better place, make it beautiful | "Sir done: old entrance (on the road) removed, new METRO entrance built off to the side in a cherry-wood station house ... with glass windows, lanterns, sign." |
| 11 | 1958-2057.8 | undo the last 10 minutes of work | asks to confirm by typing "server haan"; the owner types it; the recording ends before the result |

Notes for the edit:
- Clips 09 and 10 overlap (the entrance request was typed while the tunnel job was still running).
- From about 19:20 the chat also shows a Discord member's messages (unban requests, another player's name) and
  clip 06's reply lists player names with block counts: mask or crop these before anything public.
- Server join lines show an account list line at 0:06-1:40 and 24:06-25:40: mask it.
- First reply to the event job (22:18) starts with a long mob list before the arena line; the clean one is the
  "Sir correction" whisper right after.
- A reconnect happens at 24:00 ("Connecting to the server...").

## How the system works (owner's own description, given in chat 2026-11-16; not re-tested here)

- Three parts: Minecraft plugin (the agent, inside the server), Copper Panel (PHP + SQLite on an Ubuntu VPS,
  https://plugin.firecraft.fun), and an LLM provider the panel calls.
- Plugin is outbound-only HTTPS: no port has to be opened on the game server. It polls the panel for jobs
  (`/agent/v1/poll`) and posts events (`POST /agent/v1/events`: chat lines, metrics).
- Watchers: the AI only gets chat lines that start with a set prefix (now `server `) AND come from an allowed
  player (now the owner). All other chat never leaves the server.
- Actions: in-game reply (`tellraw`), commands such as `tp` and status, and a Discord send tool (the panel calls
  the Discord bot API directly).
- Rules (prefix, allowed players) are changed in the panel and picked up by the plugin on the next poll, no restart.
- Security: one server key per server (`cwk_...`), sensitive commands such as `/stop` and `/op` are blocked for
  the AI, all traffic is HTTPS.
- New direction (owner, 2026-11-16): sell this to hosting companies so they can offer "AI-integrated servers";
  promo video for hosting owners is being planned, nothing built yet.
