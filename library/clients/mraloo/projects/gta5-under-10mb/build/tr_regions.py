import whisper, sys, json
m = whisper.load_model("medium")
a = whisper.load_audio(sys.argv[1])
R = json.loads(sys.argv[2])
for lo, hi in R:
    seg = a[int(lo*16000):int(hi*16000)]
    for lang in ("hi", "en"):
        r = m.transcribe(seg, language=lang, condition_on_previous_text=False, beam_size=5, temperature=0, word_timestamps=True)
        ws = [f"{x['word'].strip()}@{lo+x['start']:.2f}-{lo+x['end']:.2f}" for s in r["segments"] for x in s["words"]]
        print(f"== {lo}-{hi} {lang}: " + " ".join(ws[:60]), flush=True)
