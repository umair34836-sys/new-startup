#!/usr/bin/env python3
"""Search the editing skills catalogue and print matching skills with their How lines.

  python3 library/tools/find_skill.py "speed ramp"            # all words must match (name, text, tags)
  python3 library/tools/find_skill.py "denoise" --tested      # only skills whose command was run here
  python3 library/tools/find_skill.py "#1234"                 # one skill by number
  python3 library/tools/find_skill.py --build                 # rebuild skills2/index.json from the .md files

Reads library/research/editing/skills2/*.md (#561+, with **How:**) and skills/*.md (#1-560).
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "library" / "research" / "editing"
DIRS = [ROOT / "skills2", ROOT / "skills"]
LINE = re.compile(r"^(\d+)\. \*\*(.+?)\*\*\s*[—-]+\s*(.*)$")
REF = re.compile(r"\[([^\[\]]*(?:https?://|repo:|ffmpeg docs|tested here)[^\[\]]*)\]")


def parse():
    out = []
    for d in DIRS:
        for f in sorted(d.glob("*.md")):
            cat = re.sub(r"^\d+-", "", f.stem)
            head = ""
            for line in f.read_text(encoding="utf-8").splitlines():
                if line.startswith("## "):
                    head = line[3:].strip()
                    continue
                m = LINE.match(line)
                if not m:
                    continue
                num, name, rest = m.groups()
                what, _, how = rest.partition("**How:**")
                if not how:
                    what, _, how = rest.partition("Here:")
                tags = sorted({w for w in re.findall(r"[a-z0-9]+", (cat + " " + head).lower()) if len(w) > 2})
                out.append({
                    "id": int(num), "name": name.strip(), "category": cat, "section": head, "tags": tags,
                    "file": str(f.relative_to(ROOT.parents[2])), "what": REF.sub("", what).strip(" .;"),
                    "how": REF.sub("", how).strip(), "tested": "tested here" in rest or "ran OK locally" in rest,
                    "refs": [r.strip() for r in REF.findall(rest)],
                })
    return sorted(out, key=lambda s: s["id"])


def main(argv):
    if "--build" in argv:
        skills = [s for s in parse() if s["file"].split("/")[-2] == "skills2"]
        dest = ROOT / "skills2" / "index.json"
        dest.write_text(json.dumps(skills, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(skills)} skills -> {dest}")
        return
    tested = "--tested" in argv
    words = [w.lower() for w in argv if not w.startswith("--")]
    if not words:
        print(__doc__)
        return
    q = " ".join(words)
    hits = []
    for s in parse():
        if tested and not s["tested"]:
            continue
        if q.startswith("#"):
            if str(s["id"]) == q[1:]:
                hits.append(s)
            continue
        hay = " ".join([s["name"], s["what"], s["how"], s["section"], " ".join(s["tags"])]).lower()
        if all(w in hay for w in words):
            hits.append(s)
    for s in hits[:60]:
        print(f"#{s['id']} {s['name']}  [{s['category']}{', tested' if s['tested'] else ''}]")
        print(f"   what: {s['what'][:300]}")
        if s["how"]:
            print(f"   how:  {s['how'][:600]}")
        print(f"   refs: {'; '.join(s['refs'])[:300]}")
    print(f"-- {len(hits)} match(es){' (first 60 shown)' if len(hits) > 60 else ''}")


if __name__ == "__main__":
    main(sys.argv[1:])
