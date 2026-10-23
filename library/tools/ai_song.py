# Lyrics -> song with vocals (ACE-Step 1.5, CPU), with the beats ducked under the voice and a
# Whisper transcript check of the words. Run inside /home/user/tools/venv (setup-ai-song.sh).
#
#   python ai_song.py --lyrics song.txt --caption "romantic hindi pop, piano, soft drums" \
#       --duration 60 --bpm 80 --lang hi --out /path/to/outdir
#
# Stages (each one is skipped when its output already exists, so a rerun resumes):
#   1. instrumental.flac  turbo model, 8 steps, "[Instrumental]"
#   2. vocals.flac        base model "lego" task: the vocals track generated over the instrumental
#   3. song.wav           instrumental ducked under the vocals (duck_db), vocals on top, -14 LUFS
#   4. report.json        Whisper transcript of the vocals and the song vs the lyrics (similarity 0-1)
import argparse, difflib, glob, json, os, re, shutil, subprocess, sys, time, wave
import numpy as np

# Xet's cas-server host isn't allowed here; the classic LFS path (cas-bridge) is.
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
# ACE-Step aborts a generation after 600 s (sized for GPUs); the base model on CPU needs longer.
os.environ.setdefault("ACESTEP_GENERATION_TIMEOUT", "5400")

ap = argparse.ArgumentParser()
ap.add_argument("--lyrics", required=True)
ap.add_argument("--caption", required=True, help="style of the music, e.g. 'romantic hindi pop ballad, piano, strings'")
ap.add_argument("--vocal-caption", default="warm male hindi vocals, romantic, clear diction")
ap.add_argument("--duration", type=float, default=60)
ap.add_argument("--bpm", type=int, default=80)
ap.add_argument("--lang", default="hi")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--duck-db", type=float, default=-9)
ap.add_argument("--base-steps", type=int, default=32)
ap.add_argument("--whisper-model", default="small")
ap.add_argument("--quantization", default="int8_weight_only", help="DiT weights; fp32 2B needs ~10 GB RAM and OOMs a 15 GB box at VAE decode")
ap.add_argument("--out", required=True)
ap.add_argument("--project-root", default="/home/user/tools/ACE-Step-1.5")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
lyrics = open(a.lyrics).read()
SR = 48000

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def generate(config_path, params_kwargs, dst):
    """Run one ACE-Step generation on CPU and copy its audio to dst."""
    if os.path.exists(dst):
        log(f"skip {os.path.basename(dst)} (exists)")
        return
    from acestep.handler import AceStepHandler
    from acestep.inference import GenerationParams, GenerationConfig, generate_music
    t0 = time.time()
    dit = AceStepHandler()
    status, ok = dit.initialize_service(project_root=a.project_root, config_path=config_path, device="cpu",
                                        prefer_source="huggingface",
                                        quantization=None if a.quantization == "none" else a.quantization)
    if not ok:
        sys.exit(f"model init failed ({config_path}): {status}")
    params = GenerationParams(thinking=False, use_cot_metas=False, use_cot_caption=False, use_cot_language=False,
                              seed=a.seed, **params_kwargs)
    cfg = GenerationConfig(batch_size=1, use_random_seed=False, seeds=[a.seed], audio_format="flac")
    tmp = dst + ".d"
    res = generate_music(dit, None, params, cfg, save_dir=tmp)
    if not res.success:
        sys.exit(f"generation failed: {res.error}")
    shutil.copy(res.audios[0]["path"], dst)
    shutil.rmtree(tmp, ignore_errors=True)
    del dit, res
    import gc, torch
    gc.collect()
    log(f"{os.path.basename(dst)} done in {time.time() - t0:.0f}s")

def read(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "s16le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype="<i2").astype(np.float64).reshape(-1, 2) / 32768

inst = os.path.join(a.out, "instrumental.flac")
voc = os.path.join(a.out, "vocals.flac")
song = os.path.join(a.out, "song.wav")

log("stage 1/4: instrumental (turbo)")
generate("acestep-v15-turbo", dict(task_type="text2music", caption=a.caption, lyrics="[Instrumental]",
                                   instrumental=True, duration=a.duration, bpm=a.bpm, inference_steps=8), inst)
log("stage 2/4: vocals over the instrumental (base, lego)")
generate("acestep-v15-base", dict(task_type="lego", src_audio=inst,
                                  instruction="Generate the vocals track based on the audio context:",
                                  caption=a.vocal_caption, lyrics=lyrics, vocal_language=a.lang,
                                  duration=a.duration, bpm=a.bpm, inference_steps=a.base_steps), voc)

log("stage 3/4: duck the beats under the voice and mix")
I, V = read(inst), read(voc)
n = min(len(I), len(V)); I, V = I[:n], V[:n]
win = int(0.05 * SR)
act = np.convolve(np.abs(V).mean(1), np.ones(win) / win, mode="same")
on = act > max(0.004, np.percentile(act, 60) * 0.5)
hold, last = int(0.5 * SR), -10**9
for i in range(n):  # hold through short gaps between words
    if on[i]: last = i
    elif i - last < hold: on[i] = True
duck = 10 ** (a.duck_db / 20)
env, g = np.empty(n), 1.0
for i in range(n):
    t = duck if on[i] else 1.0
    g += (t - g) * (6 / (0.2 * SR) if t < g else 6 / (0.7 * SR))
    env[i] = g
mix = I * env[:, None] + V * 1.15
mix /= max(1.0, np.abs(mix).max() / 0.95)
tmp = song + ".raw.wav"
with wave.open(tmp, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), song], check=True)
os.remove(tmp)
log(f"song.wav written; voice active {on.mean():.0%} of the time, beats ducked {a.duck_db} dB there")

log("stage 4/4: Whisper transcript check")
import whisper
model = whisper.load_model(a.whisper_model)
clean = lambda s: re.sub(r"[\s\W_]+", "", re.sub(r"\[[^\]]*\]", "", s)).lower()
target = clean(lyrics)
report = {"lyrics": lyrics}
for name, path in (("vocals", voc), ("song", song)):
    r = model.transcribe(path, language=a.lang, fp16=False)
    sim = difflib.SequenceMatcher(None, target, clean(r["text"])).ratio()
    report[name] = {"text": r["text"].strip(), "similarity": round(sim, 3),
                    "segments": [{"start": round(s["start"], 2), "end": round(s["end"], 2), "text": s["text"].strip()} for s in r["segments"]]}
    log(f"{name}: similarity {sim:.0%} :: {r['text'].strip()[:160]}")
json.dump(report, open(os.path.join(a.out, "report.json"), "w"), ensure_ascii=False, indent=1)
log("done")
