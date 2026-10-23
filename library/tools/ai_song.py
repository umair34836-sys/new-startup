# Lyrics -> song with vocals (ACE-Step 1.5 turbo, CPU), beats pulled back wherever words are sung, and a
# Whisper transcript check of the words. Run inside /home/user/tools/venv (setup-ai-song.sh).
#
#   python ai_song.py --lyrics song.txt --caption "romantic hindi pop ballad, piano, strings, male vocals" \
#       --duration 60 --bpm 80 --lang hi --out /path/to/outdir
#
# Stages (each one is skipped when its output already exists, so a rerun resumes):
#   1. raw.flac       turbo model, 8 steps, text2music with the lyrics (vocals + music in one take, ~5 min on CPU)
#   2. regions.json   Whisper word timings on raw.flac: where the words are sung
#   3. song.wav       inside those regions the bass/kick band and the hiss/cymbal band are lowered
#                     (--duck-low-db / --duck-high-db) and the voice band gets a little presence; -14 LUFS
#   4. report.json    Whisper transcript of song.wav vs the lyrics (similarity 0-1) + the word timings
# Note: the base model's "lego" task (add a vocals track over an instrumental) only re-made the instrumental
# on CPU (0.97 correlation, no words), so vocals come from text2music instead.
import argparse, difflib, json, os, re, shutil, subprocess, sys, time, wave
import numpy as np

# Big HF files: use the classic CDN path (us.aws.cdn.hf.co) rather than Xet.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
# ACE-Step aborts a generation after 600 s (sized for GPUs); CPU runs can need longer.
os.environ.setdefault("ACESTEP_GENERATION_TIMEOUT", "5400")

ap = argparse.ArgumentParser()
ap.add_argument("--lyrics", required=True)
ap.add_argument("--caption", required=True, help="style + voice, e.g. 'romantic hindi pop ballad, piano, strings, warm male vocals'")
ap.add_argument("--duration", type=float, default=60)
ap.add_argument("--bpm", type=int, default=80)
ap.add_argument("--lang", default="hi")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--steps", type=int, default=8)
ap.add_argument("--duck-low-db", type=float, default=-8, help="bass/kick band (<220 Hz) under the words")
ap.add_argument("--duck-high-db", type=float, default=-5, help="cymbal/hiss band (>7 kHz) under the words")
ap.add_argument("--presence-db", type=float, default=2, help="voice band (1.5-4 kHz) lift under the words")
ap.add_argument("--whisper-model", default="small")
ap.add_argument("--quantization", default="int8_weight_only", help="fp32 2B weights OOM a 15 GB box at VAE decode")
ap.add_argument("--out", required=True)
ap.add_argument("--project-root", default="/home/user/tools/ACE-Step-1.5")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
lyrics = open(a.lyrics).read()
SR = 48000
raw, regions_path, song = (os.path.join(a.out, f) for f in ("raw.flac", "regions.json", "song.wav"))

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def read(path):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(pcm, dtype="<i2").astype(np.float64).reshape(-1, 2) / 32768

_whisper = None
def transcribe(path):
    global _whisper
    import whisper
    if _whisper is None:
        _whisper = whisper.load_model(a.whisper_model)
    return _whisper.transcribe(path, language=a.lang, fp16=False, word_timestamps=True)

log("stage 1/4: song with vocals (turbo, text2music)")
if os.path.exists(raw):
    log("skip raw.flac (exists)")
else:
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationParams, GenerationConfig, generate_music
    t0 = time.time()
    dit = AceStepHandler()
    status, ok = dit.initialize_service(project_root=a.project_root, config_path="acestep-v15-turbo", device="cpu",
                                        prefer_source="huggingface",
                                        quantization=None if a.quantization == "none" else a.quantization)
    if not ok:
        sys.exit(f"model init failed: {status}")
    params = GenerationParams(task_type="text2music", caption=a.caption, lyrics=lyrics, vocal_language=a.lang,
                              duration=a.duration, bpm=a.bpm, inference_steps=a.steps, seed=a.seed,
                              thinking=False, use_cot_metas=False, use_cot_caption=False, use_cot_language=False)
    cfg = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[a.seed], audio_format="flac")
    res = generate_music(dit, None, params, cfg, save_dir=raw + ".d")
    if not res.success:
        sys.exit(f"generation failed: {res.error}")
    shutil.copy(res.audios[0]["path"], raw)
    shutil.rmtree(raw + ".d", ignore_errors=True)
    del dit, res
    import gc
    gc.collect()
    log(f"raw.flac done in {time.time() - t0:.0f}s")

log("stage 2/4: where are the words (Whisper word timings)")
if os.path.exists(regions_path):
    regions = json.load(open(regions_path))
else:
    r = transcribe(raw)
    words = [(w["start"], w["end"]) for s in r["segments"] for w in s.get("words", [])]
    regions = []
    for s0, s1 in words:  # merge words closer than 0.6 s into one sung phrase
        if regions and s0 - regions[-1][1] < 0.6:
            regions[-1][1] = s1
        else:
            regions.append([s0, s1])
    json.dump(regions, open(regions_path, "w"))
log(f"{len(regions)} sung phrases, {sum(e - s for s, e in regions):.1f}s of words")

log("stage 3/4: pull the beats back under the words")
from scipy.signal import butter, sosfiltfilt
x = read(raw)
n = len(x)
bands = {
    "low": sosfiltfilt(butter(4, 220, "low", fs=SR, output="sos"), x, axis=0),
    "high": sosfiltfilt(butter(4, 7000, "high", fs=SR, output="sos"), x, axis=0),
    "pres": sosfiltfilt(butter(2, [1500, 4000], "band", fs=SR, output="sos"), x, axis=0),
}
on = np.zeros(n)
for s0, s1 in regions:
    on[max(0, int((s0 - 0.08) * SR)):min(n, int((s1 + 0.15) * SR))] = 1.0
k = int(0.12 * SR)  # smooth the gate into ~120 ms ramps
env = np.convolve(on, np.ones(k) / k, mode="same")[:, None]
g = lambda db: 10 ** (db / 20) - 1  # extra gain added on top of the original band
y = x + bands["low"] * g(a.duck_low_db) * env + bands["high"] * g(a.duck_high_db) * env + bands["pres"] * g(a.presence_db) * env
y /= max(1.0, np.abs(y).max() / 0.95)
tmp = song + ".raw.wav"
with wave.open(tmp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((y * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), song], check=True)
os.remove(tmp)
log(f"song.wav written; words cover {on.mean():.0%} of the song")

log("stage 4/4: Whisper transcript check")
clean = lambda s: re.sub(r"[\s\W_]+", "", re.sub(r"\[[^\]]*\]", "", s)).lower()
r = transcribe(song)
sim = difflib.SequenceMatcher(None, clean(lyrics), clean(r["text"])).ratio()
report = {"lyrics": lyrics, "transcript": r["text"].strip(), "similarity": round(sim, 3), "regions": regions,
          "segments": [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()} for s in r["segments"]]}
json.dump(report, open(os.path.join(a.out, "report.json"), "w"), ensure_ascii=False, indent=1)
log(f"song: similarity {sim:.0%} :: {r['text'].strip()[:200]}")
log("done")
