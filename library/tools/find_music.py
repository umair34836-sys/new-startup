#!/usr/bin/env python3
# Usage: python3 library/tools/find_music.py "<video type / mood words>" [--length 30] [--bpm 100-130] [--client]
#        [--vo | --no-vo] [--platform youtube|instagram|tiktok|any] [--drop] [--top 8] [--own] [--json]
# Ranks the tracks in library/music/catalogue.json for a video and says WHY each fits (and what to watch out for).
# Profiles per video type (energy, BPM band, moods) follow library/research/music-for-video.md section 2;
# tempo bands: 60-90 slow/emotional, 90-120 talking head/tutorial/corporate, 120-150 ads/montage/short-form
# (RFTracks + Lumira, skills #356). Hard rules (CLAUDE.md): own ACE-Step/synth tracks only with --own; --client keeps
# CC0/PD only; YouTube Audio Library tracks only for --platform youtube; songs with vocals never under a voice-over.
import argparse, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CAT = os.path.join(ROOT, "library", "music", "catalogue.json")

# type -> (energy preference order, bpm band, mood words that help, needs_drop, vo_default)
PROFILES = {
    "promo":           (["high", "mid"], (110, 140), ["upbeat", "energetic", "happy", "positive", "electronic"], False, True),
    "hosting-tech":    (["mid", "high"], (100, 130), ["electronic", "modern", "tech", "upbeat"], False, True),
    "food":            (["mid", "high"], (95, 125), ["happy", "warm", "lofi", "upbeat", "world", "desi"], False, True),
    "tutorial":        (["low", "mid"], (85, 115), ["lofi", "chill", "relaxed", "light", "laid-back"], False, True),
    "explainer":       (["low", "mid"], (85, 115), ["lofi", "light", "calm", "laid-back", "electronic"], False, True),
    "gaming":          (["high", "mid"], (115, 160), ["epic", "intense", "adventure", "game", "energetic", "dramatic"], False, False),
    "emotional-story": (["low", "mid"], (60, 95), ["sad", "emotional", "reflective", "piano", "calm"], False, True),
    "wedding-desi":    (["mid", "low"], (70, 120), ["desi", "festive", "elegant", "vintage", "eastern"], False, False),
    "kids-funny":      (["mid", "high"], (100, 140), ["cute", "playful", "quirky", "happy", "kids", "funny"], False, False),
    "luxury":          (["low", "mid"], (60, 100), ["elegant", "classical", "calm", "ambient", "piano"], False, True),
    "announcement":    (["mid", "high"], (100, 130), ["epic", "dramatic", "electronic", "upbeat", "suspense"], False, True),
    "brand-reveal":    (["high", "mid"], (100, 140), ["epic", "electronic", "dramatic", "modern", "intense"], True, False),
    "showreel":        (["high", "mid"], (115, 140), ["energetic", "electronic", "upbeat", "epic"], False, False),
}
SYN = {
    "promo": ["promo", "ad", "advert", "sale", "offer", "reel", "marketing", "commercial", "product"],
    "hosting-tech": ["hosting", "host", "tech", "saas", "server", "vps", "software", "website", "app", "cloud", "rdp"],
    "food": ["food", "restaurant", "pizza", "cafe", "menu", "burger", "cooking", "recipe", "korba", "dish"],
    "tutorial": ["tutorial", "how", "guide", "screen", "walkthrough", "setup", "steps", "whitelist"],
    "explainer": ["explainer", "explain", "info", "warning", "awareness", "faq"],
    "gaming": ["gaming", "game", "minecraft", "smp", "lifesteal", "pvp", "esports", "montage"],
    "emotional-story": ["emotional", "sad", "story", "charity", "memory", "tribute", "family", "heart"],
    "wedding-desi": ["wedding", "shaadi", "mehndi", "baraat", "nikah", "eid", "desi", "dholki", "heritage"],
    "kids-funny": ["kids", "funny", "comedy", "meme", "cartoon", "cute", "birthday", "baby"],
    "luxury": ["luxury", "premium", "elegant", "fashion", "jewellery", "jewelry", "perfume", "real", "estate"],
    "announcement": ["news", "announcement", "launch", "update", "season", "notice", "breaking"],
    "brand-reveal": ["reveal", "logo", "brand", "identity", "intro", "sting", "opener"],
    "showreel": ["showreel", "portfolio", "highlights", "recap", "aftermovie"],
}

ap = argparse.ArgumentParser()
ap.add_argument("query")
ap.add_argument("--length", type=float)
ap.add_argument("--bpm", help="e.g. 100-130 (overrides the type's band)")
ap.add_argument("--client", action="store_true", help="client job: CC0/public domain only")
ap.add_argument("--vo", dest="vo", action="store_true", default=None, help="a voice-over plays over the music")
ap.add_argument("--no-vo", dest="vo", action="store_false")
ap.add_argument("--platform", default="any")
ap.add_argument("--drop", action="store_true", help="the edit needs a drop/hit for a reveal")
ap.add_argument("--own", action="store_true", help="the owner asked for our own (ACE-Step/synth) music")
ap.add_argument("--top", type=int, default=8)
ap.add_argument("--json", action="store_true")
a = ap.parse_args()

cat = json.load(open(CAT))
words = re.findall(r"[a-z0-9-]+", a.query.lower())
types = [t for t, syn in SYN.items() if any(w in syn or w == t for w in words)]
# the generic type 'promo' goes last so a specific one ('hosting-tech', 'food') sets the profile
types.sort(key=lambda t: t == "promo")
if not types:
    types = ["promo"]
    print("note: no video type recognised in the query; using 'promo'. Types:", ", ".join(PROFILES))
prof = [PROFILES[t] for t in types]
energy_pref = prof[0][0]
lo, hi = prof[0][1]
if a.bpm:
    lo, hi = [float(v) for v in a.bpm.split("-")]
need_drop = a.drop or any(p[3] for p in prof)
vo = a.vo if a.vo is not None else any(p[4] for p in prof)
mood_words = set(w for p in prof for w in p[2]) | set(words)


def bpm_fit(e):
    """distance of the track tempo (or its half/double) from the band"""
    best = None
    for b in [e.get("bpm"), e.get("bpm_alternative"), (e.get("bpm") or 0) / 2, (e.get("bpm") or 0) * 2]:
        if not b:
            continue
        d = 0 if lo <= b <= hi else min(abs(b - lo), abs(b - hi))
        if best is None or d < best[0]:
            best = (d, b)
    return best or (999, None)


rows = []
for e in cat:
    why, warn, s = [], [], 0.0
    # ---- hard filters ----
    if e["category"] == "own" and not a.own:
        continue
    if a.client and not e["client_ok"]:
        continue
    plats = e.get("platforms") or []
    if "youtube" in plats and a.platform not in ("youtube",):
        continue  # YouTube Audio Library: YouTube videos only
    if vo and e.get("vocals"):
        continue  # sung words fight the voice-over
    if not e.get("bpm") or not e.get("downbeats_s"):
        continue
    # ---- type / mood ----
    tmatch = [t for t in types if t in e.get("video_types", [])]
    if tmatch:
        s += 4 if tmatch[0] == types[0] else 2
        s += 1 * (len(tmatch) - 1); why.append("type: " + ", ".join(tmatch) + f" (folder category '{e.get('drive_folder') or e['category']}')")
    else:
        s -= 3; warn.append(f"category '{e.get('drive_folder') or e['category']}' is not tagged for {types[0]}")
    title = (e.get("title") or "").lower()
    mm = sorted(set(m for m in e.get("moods", []) if any(m.startswith(w) or w in m for w in mood_words)))
    tw = [w for w in words if len(w) > 3 and w in title]
    if mm:
        s += 1.5 * min(3, len(mm)); why.append("mood: " + ", ".join(mm[:4]))
    if tw:
        s += 2; why.append("title has: " + ", ".join(tw))
    # ---- energy ----
    if e["energy"] == energy_pref[0]:
        s += 3; why.append(f"energy {e['energy']} (wanted {energy_pref[0]})")
    elif e["energy"] in energy_pref:
        s += 1.5; why.append(f"energy {e['energy']} (ok; best {energy_pref[0]})")
    else:
        s -= 2; warn.append(f"energy {e['energy']} (wanted {'/'.join(energy_pref)})")
    # ---- tempo ----
    d, b = bpm_fit(e)
    if d == 0:
        s += 2.5; why.append(f"{b:.0f} BPM in the {lo:.0f}-{hi:.0f} band" + (" (half/double time)" if b != e["bpm"] else ""))
    elif d <= 10:
        s += 1; why.append(f"{b:.0f} BPM near the {lo:.0f}-{hi:.0f} band")
    else:
        s -= 1; warn.append(f"{e['bpm']} BPM is outside {lo:.0f}-{hi:.0f}")
    if (e.get("bpm_essentia_conf") or 0) >= 1.5 and (e.get("beat_cv") or 1) < 0.05:
        s += 1; why.append(f"steady beat grid (CV {e['beat_cv']}) -> clean bar cuts")
    elif (e.get("beat_cv") or 1) >= 0.1:
        s -= 1.5; warn.append(f"loose beat grid (CV {e.get('beat_cv')}): bar cuts may not be clean")
    # ---- structure for the edit ----
    if e.get("ending") == "natural":
        s += 1.5; why.append(f"real ending from {e.get('ending_from_s')} s -> music_fit --end resolve")
    elif e.get("ending") in ("abrupt",):
        warn.append("loop-style abrupt end: music_fit will end on a downbeat hit + ring-out")
    elif e.get("ending") == "fade-out":
        warn.append("ends in a fade-out: no button; music_fit ends on a downbeat hit + ring-out")
    if need_drop:
        if e.get("main_drop_s"):
            s += 3; why.append(f"drop at {e['main_drop_s']} s (+{e.get('main_drop_rise_db')} dB) for the reveal")
        else:
            s -= 2; warn.append("no measured drop (energy rise >= 3 dB)")
    ff = e.get("first_full_s")
    if ff is not None and ff <= 2.0:
        s += 1; why.append(f"full sound by {ff} s (hook in the first seconds)")
    elif ff is not None and ff > 6:
        warn.append(f"slow intro: full sound only at {ff} s (start later or put the drop early)")
    if a.length:
        if e["duration_s"] >= a.length + 5:
            s += 1
        elif e["duration_s"] < a.length:
            warn.append(f"{e['duration_s']:.0f} s < {a.length:.0f} s: music_fit will loop phrases")
    # ---- under a voice-over ----
    if vo:
        lra = e.get("lra_lu")
        if lra is not None and lra <= 6:
            s += 1; why.append(f"steady level (LRA ~{lra} LU) under a voice")
        if e.get("vocal_suspected_vad"):
            s -= 3; warn.append("voice-like sound detected (VAD): listen before using under VO")
        if (e.get("centroid_hz") or 0) > 3000:
            s -= 0.5; warn.append(f"bright mix (centroid {e['centroid_hz']:.0f} Hz) competes with speech: EQ or duck more")
    if e.get("field_recording"):
        s -= 3; warn.append("field recording (crowd/voices): atmosphere only")
    if e.get("vocals") is None:
        warn.append("vocals not checked")
    if not e["client_ok"]:
        warn.append("NOT for client work: " + e["licence_note"])
    rows.append((s, e, why, warn))

rows.sort(key=lambda r: -r[0])
out = []
print(f"query: {a.query!r} -> types {types}; energy {energy_pref}; BPM {lo:.0f}-{hi:.0f}; VO {'yes' if vo else 'no'};"
      f" drop {'needed' if need_drop else 'not needed'}; client-only {a.client}; platform {a.platform}")
for k, (s, e, why, warn) in enumerate(rows[: a.top], 1):
    out.append({"rank": k, "score": round(s, 1), "id": e["id"], "file": e.get("file"), "why": why, "watch": warn})
    if not a.json:
        print(f"\n{k}. {e['id']}  (score {s:.1f})  {e['duration_s']:.0f} s, {e['bpm']} BPM, {e['key']}, {e['lufs']} LUFS, "
              f"licence: {e['licence']}")
        for w in why:
            print("   + " + w)
        for w in warn:
            print("   ! " + w)
if a.json:
    print(json.dumps(out, ensure_ascii=False, indent=1))
print(f"\n{len(rows)} tracks passed the filters. Next: listen.py on the top 2-3, then music_fit.py.")
