#!/usr/bin/env python3
"""Search the no-credit media library by words: b-roll clips, Mixkit links, sound effects, LUTs.

    python3 library/tools/find_stock.py "rain night"            # b-roll in library/stock + Mixkit links
    python3 library/tools/find_stock.py --sfx "whoosh"           # library/sfx
    python3 library/tools/find_stock.py --lut "wedding warm"     # library/luts
    python3 library/tools/find_stock.py --all "fire"             # everything
    python3 library/tools/find_stock.py "office" --vertical      # only 9:16 clips
    python3 library/tools/find_stock.py --fetch-mixkit 4809 out.mp4   # download ONE Mixkit clip for a project

Scores every entry by how many query words appear in its name, category, tags and description.
Mixkit clips are links only (not in the repo): their licence forbids re-sharing them as a stock collection,
so --fetch-mixkit downloads a single clip into a project when a video needs it.
"""
import argparse
import json
import os
import re
import urllib.request

LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def load(rel, key=None):
    p = os.path.join(LIB, rel)
    if not os.path.exists(p):
        return []
    d = json.load(open(p))
    return d.get(key, []) if isinstance(d, dict) else d


def text(e):
    parts = [str(e.get(k, "")) for k in ("file", "name", "id", "title", "category", "description", "notes", "orientation")]
    parts += e.get("tags", [])
    return set(re.split(r"[^a-z0-9]+", " ".join(parts).lower()))


def search(entries, words):
    out = []
    for e in entries:
        t = text(e)
        s = sum(any(x == w or (len(w) > 3 and x.startswith(w)) for x in t) for w in words)
        if s:
            out.append((s, e))
    return [e for s, e in sorted(out, key=lambda x: -x[0])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="*")
    ap.add_argument("--sfx", action="store_true")
    ap.add_argument("--lut", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--vertical", action="store_true")
    ap.add_argument("--limit", type=int, default=15)
    ap.add_argument("--fetch-mixkit", nargs=2, metavar=("ID", "DST"))
    a = ap.parse_args()
    if a.fetch_mixkit:
        vid, dst = a.fetch_mixkit
        m = [e for e in load("stock/mixkit-links.json", "clips") if e["id"] == vid]
        if not m:
            raise SystemExit(f"{vid} is not in stock/mixkit-links.json (only videoFree items are listed)")
        req = urllib.request.Request(m[0]["file_1080"], headers={"User-Agent": "Mozilla/5.0"})
        try:
            data = urllib.request.urlopen(req, timeout=300).read()
        except Exception:
            req = urllib.request.Request(m[0]["file_720"], headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=300).read()
        open(dst, "wb").write(data)
        print(f"saved {dst} ({len(data) / 1e6:.1f} MB) - {m[0]['title']} - Mixkit Stock Video Free License, no credit needed")
        return
    words = [w.lower() for w in " ".join(a.query).replace("-", " ").split()]
    if not words:
        ap.error("give a query")
    groups = []
    if a.all or not (a.sfx or a.lut):
        clips = load("stock/index.json", "clips")
        if a.vertical:
            clips = [c for c in clips if c.get("orientation") == "vertical"]
        groups.append(("b-roll (library/stock)", clips, lambda e: f"{e['file']}  {e['orientation']} {e['width']}x{e['height']} {e['duration_s']}s  [{'own' if e['licence'].startswith('Own') else e['licence']}{' DOUBT' if e.get('licence_doubt') else ''}]  {e.get('description', '')}"))
        if not a.vertical:
            groups.append(("Mixkit links (not downloaded; --fetch-mixkit ID DST)", load("stock/mixkit-links.json", "clips"),
                           lambda e: f"{e['id']}  {e['duration_s']}s  {e['title']}  {e['page']}"))
    if a.all or a.sfx:
        groups.append(("sound effects (library/sfx)", load("sfx/index.json", "files"),
                       lambda e: f"{e['file']}  {e['length_s']}s hit {e['hit_s']}s  {e['description']}"))
    if a.all or a.lut:
        groups.append(("LUTs (library/luts)", load("luts/index.json", "luts"),
                       lambda e: f"{e['file']}  {e['description']}"))
    for title, entries, fmt in groups:
        hits = search(entries, words)[: a.limit]
        print(f"## {title}: {len(hits)} shown")
        for e in hits:
            print("  " + fmt(e))


if __name__ == "__main__":
    main()
