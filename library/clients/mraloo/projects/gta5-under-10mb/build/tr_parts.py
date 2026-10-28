import whisper, sys, numpy as np
m = whisper.load_model("medium")
a = whisper.load_audio("vo_final.wav")
for lo, hi in [(187.0, 196.0), (246.0, 256.0)]:
    seg = a[int(lo*16000):int(hi*16000)]
    for lang in ("hi", "en"):
        r = m.transcribe(seg, language=lang, condition_on_previous_text=False, beam_size=5, temperature=0, word_timestamps=True)
        print(f"== {lo}-{hi} {lang}")
        for s in r["segments"]:
            print("  ", " ".join(f"{w['word'].strip()}@{lo+w['start']:.2f}" for w in s["words"]), flush=True)
