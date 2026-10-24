# Generate a pack of our own songs/instrumentals with ACE-Step 1.5 turbo in ONE model load (the first load + INT8
# quantisation is the slow part). Everything it makes is ours: no copyright claims, no credit needed.
#   cd /home/user/tools/ACE-Step-1.5 && ../venv/bin/python -u /home/user/new-startup/library/tools/music_pack.py SPEC.json OUTDIR
# SPEC.json: [{"name", "caption", "lyrics" ("[Instrumental]" for music only), "lang" ("ur", "hi", "en", "unknown"...),
#              "duration", "bpm", "seed"}]. Writes OUTDIR/<name>.mp3 (192k, normalised toward -14 LUFS; the 9 files in music/own measured -12.9 to -14.1); skips names already done.
import json, os, shutil, subprocess, sys, time
os.environ.setdefault("HF_HUB_DISABLE_XET", "1"); os.environ.setdefault("ACESTEP_GENERATION_TIMEOUT", "5400")
from acestep.handler import AceStepHandler
from acestep.inference import GenerationParams, GenerationConfig, generate_music

spec, out = json.load(open(sys.argv[1])), sys.argv[2]
os.makedirs(out, exist_ok=True)
log = lambda m: print(time.strftime("[%H:%M:%S] ") + m, flush=True)
dit = AceStepHandler()
st, ok = dit.initialize_service(project_root="/home/user/tools/ACE-Step-1.5", config_path="acestep-v15-turbo", device="cpu",
                                prefer_source="huggingface", quantization="int8_weight_only")
log(f"model ready {ok}")
for i, s in enumerate(spec):
    mp3 = os.path.join(out, s["name"] + ".mp3")
    if os.path.exists(mp3):
        continue
    log(f"{i + 1}/{len(spec)} {s['name']} ({s['duration']}s)")
    p = GenerationParams(task_type="text2music", caption=s["caption"], lyrics=s.get("lyrics", "[Instrumental]"),
                         vocal_language=s.get("lang", "unknown"), duration=s["duration"], bpm=s.get("bpm", 100),
                         inference_steps=8, seed=s.get("seed", 7), thinking=False, use_cot_metas=False,
                         use_cot_caption=False, use_cot_language=False)
    tmp = os.path.join(out, "tmp")
    r = generate_music(dit, None, p, GenerationConfig(batch_size=1, use_random_seed=False, seeds=[s.get("seed", 7)],
                                                       audio_format="flac"), save_dir=tmp)
    if not r.success:
        log(f"FAILED {s['name']}: {r.error}"); continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", r.audios[0]["path"], "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", mp3], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    log(f"done {mp3}")
log("ALLDONE")
