# Fetch no-credit music (CC0 / public domain) from the Free Music Archive into library/music/cc0, licence-checked.
#
#   python3 library/tools/fetch_free_music.py "piano" --n 5 [--genre Ambient] [--min-sec 60 --max-sec 240]
#   python3 library/tools/fetch_free_music.py "upbeat" --n 3 --any-artist      # allow artists outside the trusted list
#   python3 library/tools/fetch_free_music.py "lofi" --dry-run                 # only list what would be fetched
#
# Rules (library/research/free-music-sources.md, owner: music must need NO credit):
# - search = FMA advanced search with the public-domain filter (it covers CC0 + the PD mark);
# - every track PAGE is read again and kept only if its licence links are CC0 1.0 / PD mark and NOT any
#   creativecommons.org/licenses/by* link;
# - the PD filter also lists mislabelled commercial uploads, so by default only artists who release everything CC0
#   are taken (TRUSTED below, from the 2026-10-24 crawl); --any-artist widens it and marks the entry "artist_unverified";
# - honest User-Agent, one request per second; files already in index.json (same source_file) are skipped.
# After fetching: python3 library/tools/music_catalogue.py --only <new id> measures them for find_music.py.
import argparse, datetime, html, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CC0 = os.path.join(ROOT, "library", "music", "cc0")
UA = "free-music-fetch/1.0 (CC0/public-domain music for video edits)"
TRUSTED = {"komiku", "holiznacc0", "monplaisir", "john bartmann", "trg banks", "loyalty freak music",
           "kimiko ishizaka", "daniel veesey", "alpha hydrae", "soundtrack 4 life"}
OK_LIC = ("creativecommons.org/publicdomain/zero/1.0", "creativecommons.org/publicdomain/mark/1.0",
          "creativecommons.org/licenses/publicdomain")

ap = argparse.ArgumentParser()
ap.add_argument("query", help="words to search on FMA (mood, genre, instrument)")
ap.add_argument("--n", type=int, default=5, help="how many new tracks to fetch")
ap.add_argument("--genre", help="keep only tracks whose FMA genre contains this (e.g. Ambient, Hip-Hop, Classical)")
# categories = music_catalogue.py's CAT table, so find_music.py can tag the new tracks (moods + video types)
_cat_src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "music_catalogue.py")).read()
_cat_src = _cat_src[_cat_src.index("CAT = {"):]
CATS = [c for c in re.findall(r'^    "([a-z-]+)":\s+\(', _cat_src[:_cat_src.index("\n}")], re.M)
        if c not in ("own", "owner-drive", "desi-vocal")]
ap.add_argument("--category", choices=CATS, help="catalogue category of what you fetch (sets its moods/video types)")
ap.add_argument("--min-sec", type=float, default=30)
ap.add_argument("--max-sec", type=float, default=420)
ap.add_argument("--any-artist", action="store_true", help="also take artists outside the trusted CC0 list")
ap.add_argument("--pages", type=int, default=3, help="search result pages to scan (20 tracks each)")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()


def get(url, binary=False):
    time.sleep(1.0)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=120).read()
    return data if binary else data.decode("utf-8", "replace")


def track_infos(page_html):
    return [json.loads(html.unescape(m)) for m in re.findall(r"data-track-info='([^']*)'", page_html)]


def slug(s):
    s = re.sub(r"\.(mp3|wav|flac|ogg)$", "", s.strip(), flags=re.I)  # some FMA titles end in ".mp3"
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


index_path = os.path.join(CC0, "index.json")
index = json.load(open(index_path))
have = {x.get("source_file") for x in index} | {x.get("page") for x in index}
category = a.category or slug(a.query.split()[0])
if category not in CATS:
    sys.exit(f"pick --category (one of: {', '.join(CATS)}) so find_music.py can tag the tracks")
today = datetime.date.today().isoformat()
got, seen = [], set()

for page in range(1, a.pages + 1):
    q = urllib.parse.urlencode({"adv": 1, "music-filter-public-domain": 1, "quicksearch": a.query,
                                "pageSize": 20, "page": page})
    results = track_infos(get("https://freemusicarchive.org/search/?" + q))
    if not results:
        break
    for r in results:
        if len(got) >= a.n:
            break
        if r["url"] in seen or r["url"] in have:
            continue
        seen.add(r["url"])
        artist = r.get("artistName", "")
        trusted = artist.lower() in TRUSTED
        if not trusted and not a.any_artist:
            print(f"skip (artist not in trusted CC0 list): {artist} - {r['title']}")
            continue
        p = get(r["url"])
        infos = [i for i in track_infos(p) if str(i.get("id")) == str(r["id"]) and i.get("fileUrl")]
        lic = sorted(set(re.findall(r"creativecommons\.org/[a-z]+/[a-z0-9/.-]*", p)))
        lic = [l for l in lic if not l.endswith(".png")]
        if not infos or not any(l.startswith(OK_LIC) for l in lic) or any("/licenses/by" in l for l in lic):
            print(f"skip (licence not CC0/PD on the page: {lic}): {artist} - {r['title']}")
            continue
        genres = re.findall(r"/genre/([A-Za-z0-9_-]+)/", p)
        if a.genre and not any(a.genre.lower() in g.lower() for g in genres):
            print(f"skip (genre {genres} has no {a.genre}): {artist} - {r['title']}")
            continue
        info = infos[0]
        if info["fileUrl"] in have:
            continue
        name = f"{category}--{slug(artist)}--{slug(r['title'])}.mp3"
        out = os.path.join(CC0, name)
        if a.dry_run:
            print(f"would fetch: {name}  ({', '.join(genres)})  {r['url']}")
            got.append(name)
            continue
        raw = out + ".src"
        open(raw, "wb").write(get(info["fileUrl"], binary=True))
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", raw],
                                   capture_output=True, text=True).stdout.strip() or 0)
        if not a.min_sec <= dur <= a.max_sec:
            os.remove(raw)
            print(f"skip (length {dur:.0f} s outside {a.min_sec:.0f}-{a.max_sec:.0f}): {artist} - {r['title']}")
            continue
        # same format as the rest of library/music/cc0 (160 kbps MP3)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-map", "0:a", "-c:a", "libmp3lame", "-b:a", "160k", out],
                       check=True)
        os.remove(raw)
        index.append({"file": name, "category": category, "title": r["title"], "author": artist,
                      "license": "CC0 1.0" if any("zero/1.0" in l for l in lic) else "Public Domain Mark",
                      "duration": round(dur), "page": r["url"], "source_file": info["fileUrl"],
                      "genres": genres, "licence_links": lic, "licence_checked": today,
                      **({} if trusted else {"artist_unverified": True})})
        have.add(info["fileUrl"])
        got.append(name)
        print(f"fetched {name}  {dur:.0f} s  {', '.join(genres)}  licence {lic}")
        json.dump(index, open(index_path, "w"), indent=1, ensure_ascii=False)
    if len(got) >= a.n:
        break

README_HEAD = ("\n## Fetched with tools/fetch_free_music.py\n\nEach row: FMA track page re-read on the date shown; its "
               "licence links were CC0 1.0 / PD mark only (no licenses/by). Artist marked * = outside the trusted CC0 "
               "list (--any-artist): check the artist before client use.\n\n| File | Category | Length | Title | Artist | "
               "Licence | Checked | Page |\n|---|---|---|---|---|---|---|---|\n")


def add_readme_rows(names):
    rp = os.path.join(CC0, "README.md")
    txt = open(rp).read()
    if "## Fetched with tools/fetch_free_music.py" not in txt:
        txt = txt.rstrip("\n") + "\n" + README_HEAD
    for x in index:
        if x["file"] in names and f"`{x['file']}`" not in txt:
            star = "*" if x.get("artist_unverified") else ""
            txt += (f"| `{x['file']}` | {x['category']} | {x['duration']}s | {x['title']} | {x['author']}{star} | "
                    f"{x['license']} | {x.get('licence_checked', '')} | {x['page']} |\n")
    open(rp, "w").write(txt)


print(f"{len(got)} track(s) {'found' if a.dry_run else 'added to library/music/cc0'}")
if got and not a.dry_run:
    add_readme_rows(set(got))
    print("listed in library/music/cc0/README.md; now measure them for find_music.py:")
    for g in got:
        print(f"  python3 library/tools/music_catalogue.py --only {g}")
