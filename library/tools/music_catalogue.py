#!/home/user/tools/perc-venv/bin/python
# Usage: /home/user/tools/perc-venv/bin/python library/tools/music_catalogue.py [--only SUBSTR] [--owner-drive DIR] [--rebuild]
# Builds library/music/catalogue.json + catalogue.md: every track the repo can use, measured with listen.py
# (--no-words), plus ending/drop/intro numbers computed here from the 100 ms RMS envelope and the downbeat grid.
# Runs listen.py ONE track at a time (4-core box) and saves after every track, so a restart resumes.
# Raw listen.py reports are cached in /home/user/tools/music-reports/ (not in git: beat lists are large).
# Licence, title, category and vocal facts come from the folders' own README/index.json (never guessed here).
# Tag rules (energy bands, video types) are listed in RULES below and in catalogue.md; sources:
# library/research/music-for-video.md.
import argparse, json, os, re, subprocess, sys, time
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MUS = os.path.join(ROOT, "library", "music")
LISTEN = os.path.join(ROOT, "library", "tools", "listen.py")
PY = "/home/user/tools/perc-venv/bin/python"
CACHE = "/home/user/tools/music-reports"
OUT_JSON = os.path.join(MUS, "catalogue.json")
OUT_MD = os.path.join(MUS, "catalogue.md")

ap = argparse.ArgumentParser()
ap.add_argument("--only", help="measure only tracks whose id contains this")
ap.add_argument("--owner-drive", help="folder with the owner's Drive tracks (gdown --folder output) to measure too")
ap.add_argument("--rebuild", action="store_true", help="recompute derived fields from cached reports (no listen.py)")
ap.add_argument("--md-only", action="store_true", help="only rewrite catalogue.md from catalogue.json")
a = ap.parse_args()
os.makedirs(CACHE, exist_ok=True)

# ---------------- category -> moods / video types (metadata-driven, see catalogue.md "Tag rules") ----------------
# moods come from the folder README category + the track title; video types follow the type table in
# library/research/music-for-video.md section 2.
CAT = {
    "background":        (["light", "playful", "game-like"], ["tutorial", "explainer", "kids-funny", "gaming"]),
    "cinematic":         (["epic", "dramatic", "intense"], ["gaming", "brand-reveal", "announcement", "showreel", "promo"]),
    "desi-eastern":      (["desi", "eastern", "festive"], ["wedding-desi", "food", "promo", "story"]),
    "piano":             (["piano", "moody"], ["emotional-story", "explainer"]),
    "classical-piano":   (["classical", "elegant", "calm"], ["luxury", "emotional-story", "wedding-desi"]),
    "emotional-piano":   (["sad", "emotional", "reflective"], ["emotional-story"]),
    "electronic":        (["electronic", "modern", "tech"], ["hosting-tech", "promo", "showreel", "brand-reveal"]),
    "upbeat-electronic": (["upbeat", "electronic", "energetic"], ["promo", "hosting-tech", "showreel", "gaming"]),
    "happy-upbeat":      (["happy", "upbeat", "positive"], ["promo", "food", "kids-funny", "tutorial"]),
    "happy-world":       (["happy", "world", "warm"], ["food", "kids-funny", "story"]),
    "world-african":     (["world", "african", "rhythmic"], ["food", "promo"]),
    "game-adventure":    (["adventure", "game", "playful"], ["gaming", "kids-funny"]),
    "kids-cute":         (["cute", "kids", "playful"], ["kids-funny"]),
    "lofi-chill":        (["lofi", "chill", "relaxed"], ["tutorial", "explainer", "food"]),
    "lofi-indie":        (["lofi", "indie", "laid-back"], ["tutorial", "explainer", "food", "story"]),
    "quirky":            (["quirky", "odd", "playful"], ["kids-funny"]),
    "travel-ambient":    (["ambient", "travel", "calm"], ["story", "explainer", "luxury"]),
    "desi-vocal":        (["vintage", "desi", "vocal", "heritage"], ["wedding-desi", "story"]),
    "own":               (["own (ACE-Step/synth)"], []),
    "owner-drive":       ([], []),
}
# owner-drive folder names -> category-like moods (folder names are the owner's own sorting)
DRIVE = {
    "lofi": (["lofi", "chill"], ["tutorial", "explainer"]),
    "mixkit": (["mixed"], ["promo"]),
    "suspense": (["suspense", "dark", "tense"], ["gaming", "announcement", "showreel"]),
    "upbeat": (["upbeat", "energetic"], ["promo", "gaming", "showreel"]),
    "promo": (["promo", "energetic"], ["promo", "gaming"]),
    "desi": (["desi", "dhol"], ["wedding-desi", "food", "promo"]),
    "emotional": (["emotional"], ["emotional-story"]),
    "funny": (["funny", "comic"], ["kids-funny"]),
    "happy": (["happy", "positive"], ["food", "kids-funny", "promo"]),
    "sting": (["sting", "short"], ["brand-reveal", "intro"]),
    "tutorial": (["neutral", "background"], ["tutorial", "explainer"]),
}
RULES = {
    "energy": "low: bpm < 90 or onsets/s < 1.5; high: bpm >= 120 and onsets/s >= 3.0; else mid "
              "(tempo bands: RFTracks + Lumira, library/research/music-for-video.md 1)",
    "bpm_used_for_energy": "listen.py bpm; when listen.py marks the tempo octave-ambiguous, the value in 80-160 is used",
    "vocals": "desi-vocal index has_vocals; library/music/vocal-scan.md (Whisper, middle 30 s); "
              "listen.py Silero speech_fraction > 0.15 marked 'vocal_suspected' only",
    "first_full_s": "first downbeat whose bar RMS is within 4 dB of the 80th-percentile bar RMS (the music is 'in')",
    "main_drop_s": "downbeat with the largest rise of mean RMS (next 2 bars minus previous 2 bars), only if the rise >= 3 dB",
    "ending": "natural = the file ends below -45 dBFS and falls from body level to that in <= 6 s; "
              "fade-out = the last 10 s fall steadily (> 6 s of decline); abrupt = last 0.3 s within 8 dB of the body level; "
              "soft-tail = ends quieter than the body but not silent (a quiet outro cut off: music_fit treats it like abrupt)",
    "ending_from_s": "last downbeat at or before the last moment the RMS is within 6 dB of the body (median bar) level: "
                     "the start of the final bar/button",
    "client_ok": "true only for CC0 1.0 / public domain tracks made by others (CLAUDE.md owner rule); "
                 "own tracks need the owner's request; YouTube Audio Library = YouTube only; Mixkit is not CC0/PD",
}


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from music_analysis import derive  # noqa: E402  (shared with music_fit.py)


def energy(bpm, alt, ops):
    b = bpm or 0
    if alt and not (80 <= b <= 160) and 80 <= alt <= 160:
        b = alt
    if b < 90 or ops < 1.5:
        return "low", b
    if b >= 120 and ops >= 3.0:
        return "high", b
    return "mid", b


def load_vocal_scan():
    hits = set()
    p = os.path.join(MUS, "vocal-scan.md")
    for line in open(p):
        m = re.match(r"\| `([^`]+)` \|", line)
        if m:
            hits.add(m.group(1))
    return hits


def tracks():
    T = []
    for x in json.load(open(os.path.join(MUS, "cc0", "index.json"))):
        T.append({"id": "cc0/" + x["file"], "path": os.path.join(MUS, "cc0", x["file"]), "folder": "cc0",
                  "title": x["title"], "author": x.get("author"), "category": x["category"],
                  "license": x["license"], "source": x.get("page"),
                  "licence_proof": "library/music/cc0/README.md (page licence audit 2026-10-24)"})
    for x in json.load(open(os.path.join(MUS, "desi-vocal", "index.json"))):
        T.append({"id": "desi-vocal/" + x["file"], "path": os.path.join(MUS, "desi-vocal", x["file"]),
                  "folder": "desi-vocal", "title": x["title"], "author": x.get("author"), "category": "desi-vocal",
                  "language": x.get("language"), "genre": x.get("genre"), "year": x.get("recorded_or_released"),
                  "license": x["license"], "source": x.get("page"), "has_vocals_meta": x.get("has_vocals"),
                  "licence_proof": "library/music/desi-vocal/README.md (India/Pakistan/US terms, 2026-10-24)"})
    own = [("romance-bollywood-72bpm.wav", "Romance Bollywood 72 BPM (Magenta + FluidSynth)"),
           ("romance-bollywood-72bpm-vocal-bed.wav", "Romance Bollywood 72 BPM, vocal bed"),
           ("romance-piano-72bpm.wav", "Romance piano 72 BPM (romance_synth.py)"),
           ("baarish-ki-pehli-shaam-ai-song.mp3", "Baarish ki pehli shaam (ACE-Step song, vocals)"),
           ("talkember-studio-promo-song.mp3", "TalkEmber Studio promo song (ACE-Step, vocals)")]
    for f, t in own:
        T.append({"id": f, "path": os.path.join(MUS, f), "folder": "root", "title": t, "author": "made here",
                  "category": "own", "license": "own (made here, no credit)", "source": "library/README.md Music",
                  "licence_proof": "library/README.md 'Music (music/)'"})
    for f in sorted(os.listdir(os.path.join(MUS, "own"))):
        if f.endswith(".mp3"):
            T.append({"id": "own/" + f, "path": os.path.join(MUS, "own", f), "folder": "own", "title": f[:-4],
                      "author": "made here (ACE-Step)", "category": "own", "license": "own (made here, no credit)",
                      "source": "library/music/own/README.md", "licence_proof": "library/music/own/README.md"})
    if a.owner_drive:
        rows = drive_rows()
        for root, _, files in os.walk(a.owner_drive):
            for f in sorted(files):
                if not f.lower().endswith((".mp3", ".wav", ".m4a", ".ogg")):
                    continue
                stem = os.path.splitext(f)[0]
                row = rows.get(norm(stem))
                if not row:
                    continue
                T.append({"id": "owner-drive/" + row["folder"] + "/" + stem, "path": os.path.join(root, f),
                          "folder": "owner-drive", "title": stem, "author": stem.split(" - ")[-1] if " - " in stem else None,
                          "category": "owner-drive", "drive_folder": row["folder"], "license": row["licence"],
                          "source": "owner's Google Drive (library/music/owner-drive/README.md)",
                          "licence_proof": "owner Drive music/CREDITS.md via library/music/owner-drive/README.md"})
    return T


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def drive_rows():
    rows = {}
    for line in open(os.path.join(MUS, "owner-drive", "README.md")):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 7 and c[2] in ("YT-ALib", "Mixkit", "Eleven"):
            rows[norm(c[1])] = {"folder": c[0], "licence": c[2]}
    return rows


def platforms_and_client(t):
    lic = t["license"]
    if t["category"] == "own":
        return ["any (owner must ask for own music)"], False, "OWN: CLAUDE.md owner rule, use only when the owner asks"
    if lic == "YT-ALib":
        return ["youtube"], False, "YouTube Audio Library: YouTube videos only (owner-drive/README.md)"
    if lic == "Mixkit":
        return ["any"], False, "Mixkit Free License: no credit, but not CC0/PD -> not for client work per owner rule"
    if lic == "Eleven":
        return ["owner's channel"], False, "owner's ElevenLabs intro sting (owner's own channel)"
    if lic.startswith("CC0") or "ublic domain" in lic or lic == "Public Domain":
        return ["any"], True, "CC0 / public domain, no credit"
    return [], False, "licence unclear: not for client work"


def build_entry(t, rep, d, vscan):
    rh, ld, km = rep.get("rhythm", {}), rep.get("loudness", {}), rep.get("key_and_mood", {})
    ops = rep.get("onsets", {}).get("per_second") or 0
    en, bpm_e = energy(rh.get("bpm"), rh.get("bpm_alternative"), ops)
    sf = (rep.get("voice_activity") or {}).get("speech_fraction")
    rel = t["id"].split("/", 1)[-1] if t["folder"] not in ("root",) else t["id"]
    scan_key = t["id"] if t["folder"] != "cc0" else t["id"]
    if t.get("has_vocals_meta") is not None:
        voc, vsrc = bool(t["has_vocals_meta"]), "desi-vocal/index.json"
    elif scan_key in vscan or t["id"].replace("cc0/", "cc0/") in vscan:
        voc, vsrc = True, "vocal-scan.md (Whisper heard words)"
    elif t["folder"] in ("cc0", "own", "root") and t["id"] not in vscan:
        voc, vsrc = False, "vocal-scan.md (no words in the middle 30 s)"
    else:
        voc, vsrc = None, "not checked"
    if "song" in t["id"] and t["category"] == "own":
        voc, vsrc = True, "own song with vocals (library/music/own/README.md / library/README.md)"
    field = "field recording" in (t["title"] or "").lower()
    if t["folder"] == "owner-drive":
        moods, types = DRIVE.get(t.get("drive_folder", "").split("/")[-1], ([], []))
    else:
        moods, types = CAT.get(t["category"], ([], []))
    moods = list(moods)
    sc = (km.get("key_best") or "")
    if sc.endswith("minor"):
        moods.append("minor-key")
    elif sc.endswith("major"):
        moods.append("major-key")
    if km.get("mood_heuristic"):
        moods.append(km["mood_heuristic"].split(",")[0])
    plats, client, why = platforms_and_client(t)
    secs = [{"start": s["start"], "end": s["end"], "energy": s["energy"], "label": s["label_guess"]}
            for s in rep.get("sections", [])]
    e = {
        "id": t["id"], "file": os.path.relpath(t["path"], ROOT) if t["folder"] != "owner-drive" else None,
        "title": t["title"], "author": t.get("author"), "folder": t["folder"], "category": t["category"],
        "drive_folder": t.get("drive_folder"), "language": t.get("language"), "genre": t.get("genre"),
        "duration_s": rep.get("duration_s"),
        "bpm": rh.get("bpm"), "bpm_alternative": rh.get("bpm_alternative"), "bpm_essentia_conf": rh.get("essentia_confidence"),
        "bar_s": rh.get("bar_s_4_4"), "beat_cv": rh.get("beat_interval_cv"),
        "downbeat_clarity": rh.get("downbeat_phase_clarity"),
        "first_downbeat_s": (rh.get("downbeats_s_estimated") or [None])[0],
        "downbeats_s": [round(x, 2) for x in (rh.get("downbeats_s_estimated") or [])],
        "key": km.get("key_best"), "lufs": ld.get("integrated_lufs"), "lra_lu": ld.get("loudness_range_lu_approx"),
        "true_peak_dbtp": ld.get("true_peak_dbtp_est"), "onsets_per_s": ops,
        "centroid_hz": km.get("spectral_centroid_hz"), "danceability": km.get("danceability_essentia_0_3"),
        "sections": secs, **d,
        "speech_fraction_vad": sf, "vocals": voc, "vocals_source": vsrc,
        "vocal_suspected_vad": bool(sf is not None and sf > 0.15),
        "field_recording": field,
        "energy": en, "bpm_for_energy": bpm_e, "moods": moods, "video_types": list(types),
        "platforms": plats, "client_ok": client, "licence": t["license"], "licence_note": why,
        "licence_proof": t["licence_proof"], "source": t.get("source"),
        "content_type_guess": rep.get("content_type_guess"),
        "measured": f"listen.py --no-words, {time.strftime('%Y-%m-%d')}",
    }
    if voc:
        e["video_types"] = [v for v in e["video_types"] if v not in ("tutorial", "explainer", "hosting-tech")]
        e["no_vo"] = True  # sung words fight a voice-over (music-for-video.md 4)
    return e


def write_md(cat):
    L = ["# Music catalogue (generated by library/tools/music_catalogue.py)", "",
         f"{len(cat)} tracks. Numbers measured here with `listen.py --no-words` (date per entry in catalogue.json "
         "`measured`). Licence facts are copied from each folder's README/index.json. Search with "
         "`python3 library/tools/find_music.py \"<video type / mood>\"`; cut with `library/tools/music_fit.py`.", "",
         "## Tag rules", ""]
    L += [f"- **{k}**: {v}" for k, v in RULES.items()]
    L += ["- **moods / video_types**: from the folder README category (or the owner's Drive folder name) via the CAT table "
          "in music_catalogue.py, plus the measured key mode and listen.py's mood heuristic. Tracks with vocals lose the "
          "tutorial/explainer/hosting-tech types and get `no_vo` (never under a voice-over).", "",
          "Columns: BPM (alt) | key | LUFS | energy | first full bar s | main drop s | ending (from s) | vocals | client OK.", ""]
    groups = {}
    for e in cat:
        groups.setdefault(e["folder"] + (" / " + (e["drive_folder"] or "") if e["folder"] == "owner-drive" else ""), []).append(e)
    for g in sorted(groups):
        L += [f"## {g} ({len(groups[g])})", "", "| Track | Len s | BPM (alt) | Key | LUFS | Energy | Full at | Drop at | Ending (from) | Vocals | Client | Types |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for e in sorted(groups[g], key=lambda z: z["id"]):
            bpm = f"{e['bpm']}" + (f" ({e['bpm_alternative']})" if e.get("bpm_alternative") else "")
            end = f"{e.get('ending')} ({e.get('ending_from_s')})"
            v = {True: "YES", False: "no", None: "?"}[e["vocals"]] + (" (VAD?)" if e["vocal_suspected_vad"] and not e["vocals"] else "")
            name = e["id"].split("/", 1)[-1] if "/" in e["id"] else e["id"]
            L.append(f"| `{name}` | {e['duration_s']:.0f} | {bpm} | {e['key']} | {e['lufs']} | {e['energy']} | "
                     f"{e.get('first_full_s')} | {e.get('main_drop_s')} | {end} | {v} | {'yes' if e['client_ok'] else 'NO'} | "
                     f"{', '.join(e['video_types'])} |")
        L.append("")
    open(OUT_MD, "w").write("\n".join(L) + "\n")


cat = json.load(open(OUT_JSON)) if os.path.exists(OUT_JSON) else []
if a.md_only:
    write_md(cat); sys.exit()
done = {e["id"]: e for e in cat}
vscan = load_vocal_scan()
T = tracks()
for i, t in enumerate(T):
    if a.only and a.only not in t["id"]:
        continue
    if t["id"] in done and not a.rebuild:
        continue
    cpath = os.path.join(CACHE, re.sub(r"[^A-Za-z0-9._-]", "_", t["id"]) + ".json")
    t0 = time.time()
    if not os.path.exists(cpath):
        if a.rebuild:
            continue
        p = subprocess.run([PY, LISTEN, t["path"], "--no-words", "--out", cpath], capture_output=True, text=True)
        if p.returncode != 0 or not os.path.exists(cpath):
            print(f"[{i + 1}/{len(T)}] FAIL {t['id']}: {p.stderr[-300:]}", flush=True)
            continue
    rep = json.load(open(cpath))
    d = derive(t["path"], rep)
    done[t["id"]] = build_entry(t, rep, d, vscan)
    cat = [done[k] for k in sorted(done)]
    with open(OUT_JSON + ".tmp", "w") as fh:  # atomic write: a crash never leaves a half file
        json.dump(cat, fh, ensure_ascii=False, indent=0, default=float)
    os.replace(OUT_JSON + ".tmp", OUT_JSON)
    print(f"[{i + 1}/{len(T)}] {t['id']}: {rep.get('duration_s')} s, {done[t['id']]['bpm']} BPM, "
          f"{done[t['id']]['lufs']} LUFS, end {d.get('ending')} ({time.time() - t0:.0f} s)", flush=True)
write_md([done[k] for k in sorted(done)])
print("catalogue:", len(done), "tracks ->", OUT_JSON)
