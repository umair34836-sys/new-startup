# word timestamps for every VO part -> words_vX.json  {line: [[word, start, end], ...]}
import sys, json, glob, whisper
V = sys.argv[1]
m = whisper.load_model("small")
out = {}
for i, f in enumerate(sorted(glob.glob(f"parts_{V}/0*.wav"))):
    r = m.transcribe(f, language="hi", word_timestamps=True, condition_on_previous_text=False, fp16=False)
    out[str(i + 1)] = [[w["word"].strip(), round(w["start"], 2), round(w["end"], 2)] for s in r["segments"] for w in s["words"]]
    print(i + 1, len(out[str(i + 1)]), flush=True)
json.dump(out, open(f"words_{V}.json", "w"), ensure_ascii=False, indent=0)
