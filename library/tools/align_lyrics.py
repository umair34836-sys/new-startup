# Where is each lyric line sung? Global in-order alignment of the lyric text against Whisper's word timings
# (character-level difflib on space-free text, so one weak line can't push the later ones out of place).
#
#   python3 align_lyrics.py lyrics.txt words.json out.json
#
# lyrics.txt: one line per sung line ([Verse]-style tags and blank lines are skipped).
# words.json: [[start, end, "word"], ...] (e.g. ai_song.py report.json "words", or Whisper word_timestamps).
# out.json:   [[start, end], ...] per lyric line; lines with no matched characters are interpolated.
import difflib, json, re, sys


def norm(s):
    return re.sub(r"[\s\.,!?\-।]", "", s.lower())


lines = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip() and not l.strip().startswith("[")]
words = json.load(open(sys.argv[2]))
tchars, towner = [], []
for wi, (_, _, w) in enumerate(words):
    for ch in norm(w):
        tchars.append(ch); towner.append(wi)
lchars, lowner = [], []
for li, l in enumerate(lines):
    for ch in norm(l):
        lchars.append(ch); lowner.append(li)
hits = {}
for a, b, n in difflib.SequenceMatcher(None, "".join(lchars), "".join(tchars), autojunk=False).get_matching_blocks():
    for k in range(n):
        hits.setdefault(lowner[a + k], []).append(towner[b + k])
spans = []
for li in range(len(lines)):
    ws = hits.get(li, [])
    spans.append([words[min(ws)][0], words[max(ws)][1]] if len(ws) >= 3 else None)
for li, s in enumerate(spans):  # interpolate gaps between known neighbours
    if s is None:
        prev = next((spans[j][1] for j in range(li - 1, -1, -1) if spans[j]), 0.0)
        nxt = next((spans[j][0] for j in range(li + 1, len(spans)) if spans[j]), prev + 3.0)
        spans[li] = [prev, nxt]
        print(f"line {li + 1}: not heard, interpolated {prev:.2f}-{nxt:.2f}")
json.dump([[round(a, 2), round(b, 2)] for a, b in spans], open(sys.argv[3], "w"))
for l, (a, b) in zip(lines, spans):
    print(f"{a:6.2f}-{b:6.2f}  {l}")
