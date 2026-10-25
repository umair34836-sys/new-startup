# FireCraft SMP: verified public facts

Use for promos/launch videos. Re-check before a new video (the site changes). Audit re-check 2026-10-24: every line
below was re-read on that date from the source named in brackets.
Sources: [home] https://www.firecraft.fun/ , [guide] https://www.firecraft.fun/blog/custom-powers-guide/ (dated Oct 8 2026),
[features] https://www.firecraft.fun/features/ , [companions] https://www.firecraft.fun/blog/mob-companions-guide/ ,
[join] https://www.firecraft.fun/join/ , [admin] FireCraft admin MCP list_announcements + get_settings (read-only).

- Private, whitelist-only Lifesteal SMP, "APPLY FREE" [home]. Java `play.firecraft.fun:20011`; Bedrock address
  `play.firecraft.fun`, port `20011` [join, admin]. Discord: discord.gg/k3wmWeBsmD [home]. Theme colour #ff8fe3 and
  hero image /images/hero/hero-bg.jpg appear in the home page HTML [home].
- Slots: "20 slots" (old note) is UNVERIFIED: not on the site; the server was offline on 2026-10-24 (api.mcsrvstat.us
  returned online=false), so the player limit could not be read.
- Headline: "11 Custom Elemental Powers • 63 Tameable Mobs • 5 Armor Sets" [home]; the page also counts Legendary
  Weapons and has the text "3 legendary weapons" [home].
- Season 2 launch (announcement "SEASON 2 — 3 DIN BAAKI", created 2026-10-16) [admin]: Sun 25 Oct, 2:00 PM PKT, everyone
  spawns together, first hour PvP off, weekly events from the second week. Server status message on 2026-10-24:
  "Maintenance • Season 2 coming soon" [admin].
- Lifesteal: start with 10 hearts; kill a player = +1 max heart, die to a player = -1 max heart; 0 hearts = eliminated
  for the season; Heart Crystal = revive yourself [home].
- Powers [guide]: active = SNEAK + RIGHT CLICK, plus a permanent passive; the power lives in a Shard item; kill a player
  in PvP -> you take their Shard; die to a mob/environment -> Shard comes back on respawn.
  Spin-wheel powers (the guide's heading says "10 POWERS" but lists 9):
  Fire (Blaze Rod: fireball / melee sets on fire), Dark (Echo Shard: Shadow Clone / hostile mobs ignore you),
  Wind (Feather: Air Dash / Slow Fall), Ice (Prismarine Shard: Ice Ray / nearby enemies weakened),
  Lightning (Glowstone Dust: Chain Lightning / Haste I), Trader (Emerald: invisibility a few seconds / 1-emerald trades),
  Rift (Rabbit Foot: Blink 30 blocks / Speed I), Warden (Sculk Shrieker, Rare: Sonic Boom 25-block beam, bypasses armor,
  14 damage, 10 s CD), Wither (Nether Star, Rare: Wither Barrage 3 rays x 8 damage + Wither II, 9 s CD).
  Craft-only legendary (2): Dragon (Dragon's Breath, hardest: 8 s transformation with 3x melee + knockback immunity;
  2nd active Dimensional Collapse on Q; craft = all 9 shard materials -> Super Energy Crystal -> Dragon Shard),
  Gravity (Heavy Core: summon 5 meteors / 3x melee + Slowness).
  (Corrected 2026-10-24: Warden is a Rare spin power, not craft-only.)
- Armor counters [guide quick-reference table]: Ember Guard (Fire 50%), Frost Plate (Ice, Wind 50%), Void Weave
  (Dark, Rift 50%), Warden Carapace (Warden 60%), Dragon Scale (Lightning, Trader, Wither, Dragon, Gravity: 40% + 15 cap).
  The home page cards instead say "No armor counter" for Lightning, Trader, Wither and Gravity, and "Counters ALL powers
  (40% reduction)" for Dragon: the site contradicts itself; ask the owner before putting counters in a video.
- Companions: up to 3 at once, level 1-100 [companions], loyalty 0-100 [features].
- Weapons [features]: Void Blade (netherite sword, Soul Slash), Thunder Axe (netherite axe, Ground Slam), Ancient Pickaxe
  (netherite pickaxe: Tunnel, Vein Mine, Auto Smelt).
- Join: 3 steps (read rules, submit application of 8 short questions, staff review in 24-48 h) [home].

## Re-check 2026-10-25 (typewriter video)
Re-read on 2026-10-25: [home] curl of https://www.firecraft.fun/ (text after stripping tags) and [admin] list_announcements +
get_settings (read-only).
- [home] still has: "PRIVATE LIFESTEAL SMP — APPLY FREE"; "11 Custom Elemental Powers • 63 Tameable Mobs • 5 Armor Sets";
  "3 legendary weapons"; "You Start with 10 Hearts"; "Kill a player and steal their heart. Die and lose one.";
  "0 Hearts = Eliminated"; "Craft Heart Crystals before it's too late."; "Spin the Power Wheel on first login.";
  "Level them up to 100 and bring up to 3 into battle."; "100% FREE — NO PAYMENT EVER";
  "Staff reviews within 24–48 hours. Check My Status to see your whitelist result and the server IP."
- Power icon images: /images/powers/{fire,ice,wind,dark,lightning,trader,rift,warden,wither,dragon,gravity}.jpg (200x200 JPEG).
- [admin] announcement "⏳ SEASON 2 — 3 DIN BAAKI" (enabled) still says "Sun 25 Oct, 2:00 PM PKT — sab ek saath spawn pe",
  "Pehla 1 ghanta PvP off", "Doosre hafte se weekly events". Server message still "Maintenance • Season 2 coming soon",
  website banner "⚔ Season 2 is coming soon — server maintenance pe hai."
- The whitelist form now has 12 fields (see firecraft-whitelist-flow.md), so the old "8 short questions" note above is out of date.
- "Season 2 applications are open" (seen on /leaderboard/ in a browser on 2026-10-24) is rendered by JavaScript: plain curl does
  not contain it.
