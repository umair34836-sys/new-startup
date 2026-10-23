# Lyric line times from the finished song: Whisper word timings, each line matched in order to its best stretch
# of words (monotonic); lines Whisper could not place are spread evenly between their placed neighbours.
#   /home/user/tools/venv/bin/python align.py SONG.wav LINES.tsv timing.json
import difflib, json, re, subprocess, sys
import whisper

song, tsv, out = sys.argv[1:4]
rows = [l.rstrip("\n").split("\t") for l in open(tsv) if l.strip() and not l.startswith("[")]
hi, ro = [r[0] for r in rows], [r[1] for r in rows]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", song],
                           capture_output=True, text=True).stdout)
r = whisper.load_model("small").transcribe(song, language="hi", fp16=False, word_timestamps=True, condition_on_previous_text=False)
W = [(w["start"], w["end"], w["word"]) for s in r["segments"] for w in s.get("words", [])]
json.dump(W, open(out + ".words.json", "w"), ensure_ascii=False)
clean = lambda s: re.sub(r"[\s\W_]+", "", s).lower()
sim = lambda a, b: difflib.SequenceMatcher(None, clean(a), clean(b)).ratio()

pos, res = 0, []
for k, line in enumerate(hi):
    best = (0.0, None, None)
    for i in range(pos, min(len(W), pos + 70)):
        for j in range(i + 1, min(len(W), i + 25) + 1):
            s = sim(line, "".join(w[2] for w in W[i:j]))
            if s > best[0]:
                best = (s, i, j)
    s, i, j = best
    if i is not None and s >= 0.38:
        res.append({"start": W[i][0], "end": W[j - 1][1], "score": round(s, 2), "heard": "".join(w[2] for w in W[i:j]).strip()})
        pos = j
    else:
        res.append(None)
# fill gaps: spread missing lines between placed neighbours, by text length
k = 0
while k < len(res):
    if res[k] is not None:
        k += 1
        continue
    a = k
    while k < len(res) and res[k] is None:
        k += 1
    t0 = res[a - 1]["end"] + 0.2 if a > 0 else 2.0
    t1 = res[k]["start"] - 0.2 if k < len(res) else dur - 3.0
    n = sum(len(hi[x]) for x in range(a, k))
    t = t0
    for x in range(a, k):
        d = (t1 - t0) * len(hi[x]) / n
        res[x] = {"start": t, "end": t + d * 0.9, "score": 0, "heard": "", "filled": True}
        t += d
lines = [dict(res[k], roman=ro[k]) for k in range(len(hi))]
json.dump({"duration": round(dur, 3), "lines": lines}, open(out, "w"), ensure_ascii=False, indent=1)
placed = sum(1 for x in lines if not x.get("filled"))
print(f"{placed}/{len(lines)} lines placed by Whisper; duration {dur:.1f}s")
for k, x in enumerate(lines):
    print(f"{k:2d} {x['start']:6.1f}-{x['end']:6.1f} {x['score']:.2f} {'FILL' if x.get('filled') else ''} {x['roman'][:40]} | {x['heard'][:40]}")
