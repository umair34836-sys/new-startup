# Script -> spoken Hindi/Hinglish voiceover with ZERO music and every line present.
# ACE-Step 1.5 turbo (the same voice the owner loved in the song) speaks the script in several takes; for every line
# Whisper finds the take where that line is clearest (more takes if a line is still unclear); each line is cut out,
# the music is removed with BS-RoFormer vocal separation, and the lines are joined with short pauses.
# Run inside /home/user/tools/venv (setup-all.sh heavy). For a song WITH music use ai_song.py instead.
#
#   python ai_voice.py --script lines.txt --out /path/to/outdir [--voice "warm male"] [--gap 0.4]
#
# lines.txt: one spoken line per row, written in Devanagari (English words too: वीडियो, माइनक्राफ्ट), because
# the Whisper check compares Devanagari text. Blank rows and [tags] are ignored.
# Output: voice.wav (48 kHz, -16 LUFS), voice.mp3, report.json (per-line score, seed, transcript).
# Takes are cached in out/groups/, picks in out/lines/NN/, so a rerun resumes without regenerating.
import argparse, difflib, gc, json, os, re, shutil, subprocess, sys, time, wave
import numpy as np

os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("ACESTEP_GENERATION_TIMEOUT", "5400")

ap = argparse.ArgumentParser()
ap.add_argument("--script", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--voice", default="warm friendly male", help="voice words for the caption, e.g. 'warm male', 'soft female'")
ap.add_argument("--caption", default=None, help="full caption override")
ap.add_argument("--takes", type=int, default=3, help="takes generated per round")
ap.add_argument("--rounds", type=int, default=3, help="max rounds per group of lines before taking the best so far")
ap.add_argument("--group", type=int, default=6, help="lines spoken together in one take")
ap.add_argument("--duration", type=float, default=0, help="seconds per take (default: from the word count)")
ap.add_argument("--good", type=float, default=0.75, help="line similarity that ends the search early")
ap.add_argument("--gap", type=float, default=0.4, help="pause between lines (s)")
ap.add_argument("--bpm", type=int, default=90)
ap.add_argument("--lang", default="hi")
ap.add_argument("--whisper-model", default="small")
ap.add_argument("--sep-model", default="model_bs_roformer_ep_368_sdr_12.9628.ckpt")
ap.add_argument("--project-root", default="/home/user/tools/ACE-Step-1.5")
a = ap.parse_args()

SR = 48000
CAPTION = a.caption or (f"spoken word, {a.voice} narrator speaking hindi, youtube voiceover, a cappella, dry clean "
                        "vocal, no music, no instruments, no singing, clear hindi speech")
lines = [l.strip() for l in open(a.script) if l.strip() and not re.fullmatch(r"\[[^\]]*\]", l.strip())]
os.makedirs(a.out, exist_ok=True)
log = lambda m: print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)
clean = lambda s: re.sub(r"[\s\W_]+", "", s).lower()
sim = lambda x, y: difflib.SequenceMatcher(None, clean(x), clean(y)).ratio()

def read(path, ch=2):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", str(ch), "-ar", str(SR), "-f", "s16le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(pcm, dtype="<i2").astype(np.float64).reshape(-1, ch) / 32768

def write(path, y):
    with wave.open(path, "wb") as w:
        w.setnchannels(y.shape[1]); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())

_wh = None
def words_of(path):
    global _wh
    import whisper
    if _wh is None:
        _wh = whisper.load_model(a.whisper_model)
    r = _wh.transcribe(path, language=a.lang, fp16=False, word_timestamps=True)
    return [(w["start"], w["end"], w["word"]) for s in r["segments"] for w in s.get("words", [])]

def best_window(words, line):
    """The contiguous run of words that matches the line best (a take may repeat or pad the line)."""
    best = (0.0, 0, 0)
    for i in range(len(words)):
        for j in range(i + 1, min(len(words), i + 40) + 1):
            s = sim(line, "".join(w[2] for w in words[i:j]))
            if s > best[0] + 1e-9 or (abs(s - best[0]) < 1e-9 and j - i < best[2] - best[1]):
                best = (s, i, j)
    s, i, j = best
    return s, (words[i][0], words[j - 1][1], "".join(w[2] for w in words[i:j]).strip()) if j else None

# Stage 1: speak the script in groups of lines (a whole passage keeps the delivery natural; a lone short line
# comes out garbled). Each round makes --takes takes of the group; every line keeps its best-matching stretch from
# any take. Rounds stop once every line of the group reaches --good. Takes are cached for reruns.
dit = None
picks = {}
def generate(lyrics, seeds, duration, save_dir):
    global dit
    from acestep.inference import GenerationParams, GenerationConfig, generate_music
    if dit is None:
        from acestep.handler import AceStepHandler
        dit = AceStepHandler()
        status, ok = dit.initialize_service(project_root=a.project_root, config_path="acestep-v15-turbo",
                                            device="cpu", prefer_source="huggingface", quantization="int8_weight_only")
        if not ok:
            sys.exit(f"model init failed: {status}")
    params = GenerationParams(task_type="text2music", caption=CAPTION, lyrics=lyrics, vocal_language=a.lang,
                              duration=duration, bpm=a.bpm, inference_steps=8, seed=seeds[0], thinking=False,
                              use_cot_metas=False, use_cot_caption=False, use_cot_language=False)
    cfg = GenerationConfig(batch_size=len(seeds), use_random_seed=False, seeds=seeds, audio_format="flac")
    res = generate_music(dit, None, params, cfg, save_dir=save_dir)
    return [au["path"] for au in res.audios] if res.success else []

for g0 in range(0, len(lines), a.group):
    group = list(range(g0, min(len(lines), g0 + a.group)))
    gd = os.path.join(a.out, "groups", f"{g0:02d}")
    os.makedirs(gd, exist_ok=True)
    lyrics = "[Spoken Word]\n" + "\n".join(lines[i] for i in group)
    nwords = sum(len(lines[i].split()) for i in group)
    duration = a.duration or min(120, max(10, round(nwords * 0.65 + 4)))
    for rnd in range(a.rounds):
        seeds = [1000 * (g0 + 1) + 7 * (rnd * a.takes + k) + 21 for k in range(a.takes)]
        todo = [sd for sd in seeds if not os.path.exists(os.path.join(gd, f"{sd}.json"))]
        if todo:
            log(f"lines {group[0] + 1}-{group[-1] + 1}: round {rnd + 1}, {len(todo)} takes of {duration}s")
            for sd, path in zip(todo, generate(lyrics, todo, duration, os.path.join(gd, "tmp"))):
                shutil.move(path, os.path.join(gd, f"{sd}.flac"))
                json.dump(words_of(os.path.join(gd, f"{sd}.flac")), open(os.path.join(gd, f"{sd}.json"), "w"),
                          ensure_ascii=False)
            shutil.rmtree(os.path.join(gd, "tmp"), ignore_errors=True)
        for sd in seeds:
            if not os.path.exists(os.path.join(gd, f"{sd}.json")):
                continue
            words = [tuple(w) for w in json.load(open(os.path.join(gd, f"{sd}.json")))]
            for i in group:
                sc, win = best_window(words, lines[i])
                if win and sc > picks.get(i, {}).get("score", -1):
                    picks[i] = {"line": lines[i], "score": sc, "seed": sd, "heard": win[2], "start": win[0],
                                "end": win[1], "src": os.path.join(gd, f"{sd}.flac")}
        log("  " + "  ".join(f"L{i + 1} {picks[i]['score']:.0%}" if i in picks else f"L{i + 1} -" for i in group))
        if all(picks.get(i, {}).get("score", 0) >= a.good for i in group):
            break

report = []
for n, line in enumerate(lines):
    if n not in picks:
        sys.exit(f"line {n + 1} never heard in any take: rewrite it shorter or raise --rounds")
    d = os.path.join(a.out, "lines", f"{n:02d}")
    os.makedirs(d, exist_ok=True)
    pick = picks[n]
    old = json.load(open(os.path.join(d, "pick.json"))) if os.path.exists(os.path.join(d, "pick.json")) else None
    if old != pick:
        x = read(pick["src"])
        s0, s1 = max(0, int((pick["start"] - 0.12) * SR)), min(len(x), int((pick["end"] + 0.3) * SR))
        write(os.path.join(d, "take.wav"), x[s0:s1])
        json.dump(pick, open(os.path.join(d, "pick.json"), "w"), ensure_ascii=False, indent=1)
    report.append(pick)

if dit is not None:
    del dit
    gc.collect()

# Stage 2: remove the music from each cropped line (vocals stem only).
from audio_separator.separator import Separator
sep = None
for n in range(len(lines)):
    d = os.path.join(a.out, "lines", f"{n:02d}")
    voc = os.path.join(d, "voice.wav")
    if os.path.exists(voc) and os.path.getmtime(voc) > os.path.getmtime(os.path.join(d, "take.wav")):
        continue
    sep_dir = os.path.join(a.out, "sep")
    if sep is None:
        sep = Separator(model_file_dir="/home/user/tools/sep-models", output_dir=sep_dir, output_format="WAV",
                        output_single_stem="Vocals", sample_rate=SR)
        sep.load_model(model_filename=a.sep_model)
    out = sep.separate(os.path.join(d, "take.wav"))
    shutil.move(os.path.join(sep_dir, os.path.basename(out[0])), voc)
    log(f"line {n + 1}/{len(lines)}: music removed")

# Stage 3: join the lines with pauses, gently fade each edge, normalise.
fade = int(0.02 * SR)
ramp = np.linspace(0, 1, fade)[:, None]
parts = []
for n in range(len(lines)):
    y = read(os.path.join(a.out, "lines", f"{n:02d}", "voice.wav"))
    y[:fade] *= ramp
    y[-fade:] *= ramp[::-1]
    parts += [y, np.zeros((int(a.gap * SR), 2))]
tmp = os.path.join(a.out, "voice.raw.wav")
write(tmp, np.concatenate(parts[:-1]))
final = os.path.join(a.out, "voice.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR),
                final], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", final, "-c:a", "libmp3lame", "-b:a", "192k",
                os.path.join(a.out, "voice.mp3")], check=True)
os.remove(tmp)

# Stage 4: check the finished voiceover as a whole.
heard = "".join(w[2] for w in words_of(final))
total = sim("".join(lines), heard)
json.dump({"caption": CAPTION, "similarity": round(total, 3), "heard": heard.strip(), "lines": report},
          open(os.path.join(a.out, "report.json"), "w"), ensure_ascii=False, indent=1)
log(f"voice.wav done: {len(lines)} lines, overall similarity {total:.0%}, lowest line "
    f"{min(r['score'] for r in report):.0%}")
