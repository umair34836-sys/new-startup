# Global, in-order matching of lyric lines to Whisper words (dynamic programming): each line either takes one
# stretch of words after the previous line's stretch, or is left unplaced. A line only counts if its match beats
# THRESH, so a weak match never drags the following lines out of place (the greedy version did).
#   python3 dp_align.py LINES.tsv OUT.json DURATION WORDS1.json [WORDS2.json ...]   (keeps the best word list)
import difflib, json, re, sys
from functools import lru_cache

tsv, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
rows = [l.rstrip("\n").split("\t") for l in open(tsv) if l.strip() and not l.startswith("[")]
hi, ro = [r[0] for r in rows], [r[1] for r in rows]
clean = lambda s: re.sub(r"[\s\W_]+", "", s).lower()
THRESH, MAXW = 0.42, 22
N = len(hi)


def align(W):
    M = len(W)
    cl = [clean(w[2]) for w in W]
    sc = {}
    for k in range(N):
        target = clean(hi[k])
        for i in range(M):
            acc = ""
            for j in range(i + 1, min(M, i + MAXW) + 1):
                acc += cl[j - 1]
                if len(acc) > 2.2 * len(target) + 6:
                    break
                s = difflib.SequenceMatcher(None, target, acc).ratio()
                if s >= THRESH and s > sc.get((k, i), (0, 0))[0]:
                    sc[(k, i)] = (s, j)
    sys.setrecursionlimit(100000)
    f = {}
    for k in range(N, -1, -1):
        for i in range(M, -1, -1):
            if k == N:
                f[(k, i)] = (0.0, None)
                continue
            best = (f[(k + 1, i)][0], ("skip",))
            if i < M and f[(k, i + 1)][0] > best[0]:
                best = (f[(k, i + 1)][0], ("word",))
            if (k, i) in sc:
                s, j = sc[(k, i)]
                v = (s - THRESH + 0.05) + f[(k + 1, j)][0]
                if v > best[0]:
                    best = (v, ("take", j, s))
            f[(k, i)] = best
    res, k, i = [None] * N, 0, 0
    while k < N:
        mv = f[(k, i)][1]
        if mv[0] == "skip":
            k += 1
        elif mv[0] == "word":
            i += 1
        else:
            j, s = mv[1], mv[2]
            res[k] = {"start": W[i][0], "end": W[j - 1][1], "score": round(s, 2),
                      "heard": "".join(w[2] for w in W[i:j]).strip()}
            k, i = k + 1, j
    return res


best = None
for path in sys.argv[4:]:
    W = [tuple(w) for w in json.load(open(path))]
    r = align(W)
    q = sum(x["score"] for x in r if x)
    print(f"{path.split('/')[-1]}: {sum(1 for x in r if x)}/{N} placed, total score {q:.2f}")
    if best is None or q > best[0]:
        best = (q, r, path)
_, res, path = best
print("using", path.split("/")[-1])
# Unplaced lines: spread between placed neighbours by text length; marked so captions can skip them.
k = 0
while k < N:
    if res[k] is not None:
        k += 1
        continue
    a = k
    while k < N and res[k] is None:
        k += 1
    t0 = res[a - 1]["end"] + 0.2 if a > 0 else 2.0
    t1 = res[k]["start"] - 0.2 if k < N else dur - 3.0
    n = sum(len(hi[x]) for x in range(a, k))
    t = t0
    for x in range(a, k):
        d = max(0.0, t1 - t0) * len(hi[x]) / n
        res[x] = {"start": t, "end": t + d * 0.9, "score": 0, "heard": "", "filled": True}
        t += d
lines = [dict(res[k], roman=ro[k]) for k in range(N)]
json.dump({"duration": dur, "lines": lines}, open(out, "w"), ensure_ascii=False, indent=1)
for k, x in enumerate(lines):
    print(f"{k:2d} {x['start']:6.1f}-{x['end']:6.1f} {x['score']:.2f} {'FILL' if x.get('filled') else '    '} {x['roman'][:38]:38s} | {x['heard'][:34]}")
